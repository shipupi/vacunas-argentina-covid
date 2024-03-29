import schedule
import time
import requests
import zipfile
import psycopg2
from datetime import datetime
from openpyxl import load_workbook
from lxml import html
import pandas as pd
import os
import re
from configparser import ConfigParser
from dotenv import dotenv_values


# Dataset departamentos:
# https://www.ign.gob.ar/NuestrasActividades/InformacionGeoespacial/CapasSIG

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.abspath(os.path.join(DIR_PATH, "../../"))

OUTDATED_ETAG = "OUTDATED_ETAG"
VACCINE_NAMES = [   {"nomivac_name": "Sputnik", "actas_de_recepcion_name": "LIMITED LIABILITY COMPANY HUMAN VACCINE"},
                    {"nomivac_name": "COVISHIELD", "actas_de_recepcion_name": "SERUM LIFE SCIENCES LTD"},
                    {"nomivac_name": "AstraZeneca", "actas_de_recepcion_name": "ASTRAZENECA (Mecanismo COVAX)"},
                    {"nomivac_name": "Sinopharm", "actas_de_recepcion_name": "SINOPHARM INTERNATIONAL HONG KONG LIMITED"}
                ]

def config():
    conf = dotenv_values(os.path.abspath(os.path.join(BASE_PATH, ".env")))
    if "database" not in conf:
        raise Exception('Invalid .env file')
    return conf
def test_connect():
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

def load_populations():
    print("Starting population load")
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        tablename = "population"
        csvname = "population.csv"
        cur.execute("DROP TABLE IF EXISTS " +tablename +";")
        cur.execute("CREATE TABLE " +tablename +"(\
            provincia text,\
            provinciaID varchar(2),\
            departamento text,\
            departamentoID varchar(5),\
            pop2010 integer,\
            pop2021 integer\
            );")
        cur.execute("COPY " +tablename +" FROM '" +os.getcwd()+"/"+csvname +"' DELIMITER ',' CSV HEADER")
        conn.commit()
        cur.close()
        print("Population loaded successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def load_vaccine_names(tablename, vaccine_names):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS " +tablename +";")
        cur.execute("CREATE TABLE " +tablename +"(\
            vaccine_id SERIAL PRIMARY KEY,\
            nomivac_name TEXT,\
            actas_de_recepcion_name TEXT\
            );")
        for vaccine in vaccine_names:
            cur.execute("INSERT INTO " +tablename +"(nomivac_name, actas_de_recepcion_name) VALUES(\'" +vaccine["nomivac_name"] +"\', \'" +vaccine["actas_de_recepcion_name"] +"\');")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def load_datos_nomivac_covid19(dataset):
    name = dataset["name"]
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
            f2.write(line.replace('\"S.I.\"', '')
                        .replace('\"COMUNA 1\",\"001\"', '\"COMUNA 1\",\"007\"')
                        .replace('\"COMUNA 2\",\"002\"', '\"COMUNA 2\",\"014\"')
                        .replace('\"COMUNA 3\",\"003\"', '\"COMUNA 3\",\"021\"')
                        .replace('\"COMUNA 4\",\"004\"', '\"COMUNA 4\",\"028\"')
                        .replace('\"COMUNA 5\",\"005\"', '\"COMUNA 5\",\"035\"')
                        .replace('\"COMUNA 6\",\"006\"', '\"COMUNA 6\",\"042\"')
                        .replace('\"COMUNA 7\",\"007\"', '\"COMUNA 7\",\"049\"')
                        .replace('\"COMUNA 8\",\"008\"', '\"COMUNA 8\",\"056\"')
                        .replace('\"COMUNA 9\",\"009\"', '\"COMUNA 9\",\"063\"')
                        .replace('\"COMUNA 10\",\"010\"', '\"COMUNA 10\",\"070\"')
                        .replace('\"COMUNA 11\",\"011\"', '\"COMUNA 11\",\"077\"')
                        .replace('\"COMUNA 12\",\"012\"', '\"COMUNA 12\",\"084\"')
                        .replace('\"COMUNA 13\",\"013\"', '\"COMUNA 13\",\"091\"')
                        .replace('\"COMUNA 14\",\"014\"', '\"COMUNA 14\",\"098\"')
                        .replace('\"COMUNA 15\",\"015\"', '\"COMUNA 15\",\"105\"')
            )
        f1.close()
        f2.close()
        cur.execute("DROP TABLE IF EXISTS " +tablename +" CASCADE;")
        cur.execute("CREATE TABLE " +tablename +"(\
            sexo varchar,\
            grupo_etario text,\
            jurisdiccion_residencia text,\
            jurisdiccion_residencia_id varchar(2),\
            depto_residencia text,\
            depto_residencia_id varchar(5),\
            jurisdiccion_aplicacion text,\
            jurisdiccion_aplicacion_id varchar(5),\
            depto_aplicacion text,\
            depto_aplicacion_id varchar(5),\
            fecha_aplicacion date,\
            vacuna text,\
            condicion_aplicacion text,\
            orden_dosis integer,\
            lote_vacuna text);")
        cur.execute("COPY " +tablename +" FROM '" +os.getcwd()+"/"+f2_name +"' DELIMITER ',' NULL AS '' CSV HEADER")
        print("-Creating views for table " +tablename)
        cur.execute("CREATE MATERIALIZED VIEW timeline AS\
                    SELECT jurisdiccion_residencia, jurisdiccion_residencia_id, depto_residencia, depto_residencia_id, fecha_aplicacion, vacuna, orden_dosis, \
                            concat(jurisdiccion_residencia_id, depto_residencia_id) AS codigo_indec, count(*) AS cantidad\
                    FROM " +tablename +"\
                    GROUP BY jurisdiccion_residencia, jurisdiccion_residencia_id, depto_residencia, depto_residencia_id, fecha_aplicacion, vacuna, orden_dosis\
                    ORDER BY fecha_aplicacion, jurisdiccion_residencia_id, depto_residencia_id, vacuna, orden_dosis;")
        cur.execute("CREATE MATERIALIZED VIEW dosis_por_distrito AS\
                    SELECT jurisdiccion_residencia, jurisdiccion_residencia_id, depto_residencia, depto_residencia_id, vacuna, orden_dosis,\
                            concat(jurisdiccion_residencia_id, depto_residencia_id) AS codigo_indec, count(*) AS cantidad\
                    FROM " +tablename +"\
                    GROUP BY jurisdiccion_residencia, jurisdiccion_residencia_id, depto_residencia, depto_residencia_id, vacuna, orden_dosis\
                    ORDER BY jurisdiccion_residencia_id, depto_residencia_id, vacuna, orden_dosis;")
        conn.commit()
        cur.close()
        os.remove(f2_name)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def load_vacunas_agrupadas(dataset):
    name = dataset["name"]
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        tablename = name
        csvname = tablename+".csv"
        cur.execute("DROP TABLE IF EXISTS " +tablename +";")
        cur.execute("CREATE TABLE " +tablename +"(\
            jurisdiccion_codigo_indec varchar(2),\
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

def load_acta_recepcion(dataset):
    wb = load_workbook(dataset["name"]+".xlsx", data_only=True)
    sheet = wb[dataset["sheet"]]
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        tablename = dataset["name"]
        cur.execute("DROP TABLE IF EXISTS " +tablename +";")
        cur.execute("CREATE TABLE IF NOT EXISTS " +tablename +"(\
            empresa text,\
            cantidad integer,\
            guia_aerea text,\
            fecha_entrega date,\
            empresa_traslado text\
            );")
        first = True
        for row in sheet.values:
            if(first):
                first = False
            else:
                if(str(row[0]) != "TOTAL"):
                    date = row[3]
                    # Filter non-standard dates
                    if(type(row[3]) == str):
                        date = re.findall("[0-9]+/[0-9]+/[0-9]+", str(row[3]))
                        numbers = date[0].split("/")
                        if(int(numbers[2]) < 100):
                            numbers[2] = 2000 + int(numbers[2])
                        date = datetime(int(numbers[2]), int(numbers[1]), int(numbers[0]))
                    cur.execute("INSERT INTO " +tablename +"(empresa,cantidad,guia_aerea,fecha_entrega,empresa_traslado) VALUES(\'"
                                    +str(row[0]) +"\', " +str(row[1]) +", \'" +str(row[2]) +"\', \'" +str(date) +"\', \'" +str(row[5]) +"\');")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def load_departamentos(dataset):
    name = dataset["name"]
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        tablename = name
        csvname = tablename+".csv"
        cur.execute("DROP TABLE IF EXISTS " +tablename +";")
        cur.execute("CREATE TABLE " +tablename +"(\
            gid integer,\
            objeto text,\
            geom text,\
            fna text,\
            gna text,\
            nam text,\
            inl varchar(5),\
            fdc text,\
            sag text\
            );")
        cur.execute("COPY " +tablename +" FROM '" +os.getcwd()+"/"+csvname +"' DELIMITER ',' CSV HEADER")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def load_provincias(dataset):
    name = dataset["name"]
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        tablename = name
        csvname = tablename+".csv"
        cur.execute("DROP TABLE IF EXISTS " +tablename +";")
        cur.execute("CREATE TABLE " +tablename +"(\
            gid integer,\
            entidad integer,\
            objeto text,\
            geom text,\
            fna text,\
            gna text,\
            nam text,\
            inl varchar(5),\
            fdc text,\
            sag text\
            );")
        cur.execute("COPY " +tablename +" FROM '" +os.getcwd()+"/"+csvname +"' DELIMITER ',' CSV HEADER")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def is_dataset_up_to_date(dataset, etag):
    if (etag == OUTDATED_ETAG):
        return False
    conn = None
    try:
        uptodate = False
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        tablename = "etags"
        csvname = tablename+".csv"
        cur.execute("CREATE TABLE IF NOT EXISTS etags(\
            dataset text,\
            latest_etag text\
            );")
        cur.execute("SELECT * FROM etags WHERE dataset LIKE \'" +dataset["name"] +"\' AND latest_etag LIKE \'" +etag +"\';")
        result = cur.fetchone()
        conn.commit()
        cur.close()
        if(result != None):
            uptodate = True;
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return uptodate

def update_etag(dataset, etag):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        tablename = "etags"
        csvname = tablename+".csv"
        cur.execute("CREATE TABLE IF NOT EXISTS etags(\
            dataset text,\
            latest_etag text\
            );")
        cur.execute("DELETE FROM etags WHERE dataset LIKE \'" +dataset["name"] +"\';")
        cur.execute("INSERT INTO etags(dataset, latest_etag) VALUES(\'" +dataset["name"] +"\', \'" +etag +"\');")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def download(dataset):
    if(dataset["name"] == "datos_nomivac_covid19" or dataset["name"] == "Covid19VacunasAgrupadas"
                or dataset["name"] == "departamento" or dataset["name"] == "provincia"):
        filename = dataset["name"] +".zip"
        csvname = dataset["name"] +".csv"
        r = requests.head(dataset["url"], allow_redirects=True)
        etag = OUTDATED_ETAG
        if ("ETag" in r.headers):
            etag = r.headers["ETag"]
        if is_dataset_up_to_date(dataset, etag):
            print("-Etag up to date. No need to download again!")
            return ""
        print("-Downloading " +dataset["name"])
        r = requests.get(dataset["url"], allow_redirects=True, timeout=20)
        open(filename, 'wb').write(r.content)
        time.sleep(3)
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(".")
        print("-Dataset " +dataset["name"] +" downloaded and extracted!")
        os.remove(filename)
        return etag
    else:
        filename = dataset["name"]+".xlsx"
        r = requests.get(dataset["url"], allow_redirects=True)
        tree = html.fromstring(r.content)
        download_link = tree.xpath('//a[@class="btn btn-green btn-block"]/@href')[0]
        r = requests.head(download_link, allow_redirects=True)
        etag = r.headers["ETag"]
        if is_dataset_up_to_date(dataset, etag):
            print("-Etag up to date. No need to download again!")
            return ""
        print("-Downloading " +dataset["name"])
        r = requests.get(download_link, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        print("-Dataset " +dataset["name"] +" downloaded!")
        return etag

def download_datasets():
    sets = [{"url": "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/datos_nomivac_covid19.zip", "name": "datos_nomivac_covid19", "function": load_datos_nomivac_covid19},
            {"url": "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19VacunasAgrupadas.csv.zip", "name": "Covid19VacunasAgrupadas", "function": load_vacunas_agrupadas},
            {"url": "https://dnsg.ign.gob.ar/apps/api/v1/capas-sig/Geodesia+y+demarcaci%C3%B3n/L%C3%ADmites/departamento/csv", "name": "departamento", "function": load_departamentos},
            {"url": "https://dnsg.ign.gob.ar/apps/api/v1/capas-sig/Geodesia+y+demarcaci%C3%B3n/L%C3%ADmites/provincia/csv", "name": "provincia", "function": load_provincias},
            {"url": "http://datos.salud.gob.ar/dataset/actas-de-recepcion-de-vacunas-covid-19/archivo/d2851fa6-b105-4f15-b352-dd3d792bd526", "name": "actas_de_recepcion_vacunas",
                "sheet": "Carolina", "function": load_acta_recepcion}
            ]
    for x in sets:
        print("\nRetrieving dataset " +x["name"])
        etag = download(x)
        if(etag != ""):
            x["function"](x)
            update_etag(x, etag)
        print("-Table " +x["name"] +" is now up to date!")
    print("\n\n*** DB FULLY UPDATED! See you in 24 hours! ***\nPlease keep this process running in the background\n")

def main():
    data_dir = os.path.abspath(os.path.join(BASE_PATH, "data"))
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    os.chdir(data_dir)
    # Task scheduling
    load_populations()
    schedule.every(24).hours.do(download_datasets)
    # Loop so that the scheduling task keeps on running all time.
    load_vaccine_names("vacunas", VACCINE_NAMES)
    download_datasets()
    while True:
        # Checks whether a scheduled task is pending to run or not
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
