import schedule
import time
import requests
import zipfile
import psycopg2
import pandas as pd
import os
from configparser import ConfigParser

def config(filename='../src/config/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

def test_connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
	    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def load_datos_nomivac_covid19(name):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        tablename = name
        csvname = tablename+".csv"
        f2_name = tablename+"temp.csv"
        f1 = open(csvname, 'r')
        f2 = open(f2_name, 'w')
        for line in f1:
            f2.write(line.replace('\"S.I.\"', ''))
        f1.close()
        f2.close()
        cur.execute("DROP TABLE IF EXISTS " +tablename +";")
        cur.execute("CREATE TABLE " +tablename +"(\
            sexo varchar,\
            grupo_etario text,\
            jurisdiccion_residencia text,\
            jurisdiccion_residencia_id integer,\
            depto_residencia text,\
            depto_residencia_id integer,\
            jurisdiccion_aplicacion text,\
            jurisdiccion_aplicacion_id integer,\
            depto_aplicacion text,\
            depto_aplicacion_id integer,\
            fecha_aplicacion date,\
            vacuna text,\
            condicion_aplicacion text,\
            orden_dosis integer,\
            lote_vacuna text);")
        cur.execute("COPY " +tablename +" FROM '" +os.getcwd()+"/"+f2_name +"' DELIMITER ',' NULL AS '' CSV HEADER")
        conn.commit()
        cur.close()
        os.remove(f2_name)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def load_vacunas_agrupadas(name):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        tablename = name
        csvname = tablename+".csv"
        cur.execute("DROP TABLE IF EXISTS " +tablename +";")
        cur.execute("CREATE TABLE " +tablename +"(\
            jurisdiccion_codigo_indec integer,\
            jurisdiccion_nombre text,\
            vacuna_nombre text,\
            primera_dosis_cantidad integer,\
            segunda_dosis_cantidad integer\
            );")
        cur.execute("COPY " +tablename +" FROM '" +os.getcwd()+"/"+csvname +"' DELIMITER ',' CSV HEADER")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def download_datasets():
    sets = [{"url": "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/datos_nomivac_covid19.zip", "name": "datos_nomivac_covid19", "function": load_datos_nomivac_covid19},
            {"url": "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19VacunasAgrupadas.csv.zip", "name": "Covid19VacunasAgrupadas", "function": load_vacunas_agrupadas}]
    for x in sets:
        download(x)
        x["function"](x["name"])
        print("Table " +x["name"] +" updated")
    print("DB FULLY UPDATED! See you in 24 hours!")

def download(dataset):
    filename = dataset["name"] +".zip"
    csvname = dataset["name"] +".csv"
    r = requests.get(dataset["url"], allow_redirects=True)
    open(filename, 'wb').write(r.content)
    time.sleep(1)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(".")
    print("Dataset " +dataset["name"] +" downloaded and extracted!")
    os.remove(filename)

# Task scheduling
schedule.every(24).hours.do(download_datasets)

# Loop so that the scheduling task keeps on running all time.
os.chdir("../../data")
download_datasets()
while True:
    # Checks whether a scheduled task is pending to run or not
    schedule.run_pending()
    time.sleep(1)
