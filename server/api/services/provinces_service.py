from api.persistence.db_driver import run_query
from api.persistence.query_helper import Query

def get_provinces():
    query = "Select nam, inl FROM provincia"
    provinces = run_query(query)
    return provinces

def get_vaccines_by_single_province(province):
    data = [province]
    query =  Query("covid19vacunasagrupadas")
    pop_query = Query("population")
    pop_query.group_by(["provinciaid", "provincia"])
    pop_query.select(["provincia", "provinciaid", "sum(pop2021) as population"])
    query.queryjoin(pop_query, "pops", "jurisdiccion_codigo_indec", "provinciaid")
    query.where("jurisdiccion_codigo_indec = %s")
    query.group_by(["jurisdiccion_codigo_indec", "jurisdiccion_nombre", "population"])
    query.select(["jurisdiccion_codigo_indec", "jurisdiccion_nombre, sum(primera_dosis_cantidad) as primera_dosis, sum(segunda_dosis_cantidad) as segunda_dosis, sum(segunda_dosis_cantidad) + sum(primera_dosis_cantidad) as total_dosis", "population as poblacion"])
    result = run_query(query.get(),data=data)
    if len(result) > 0:
        result = result[0]
        result["porc_primera_dosis"] = round((result["primera_dosis"] / result["poblacion"]) * 100, 2)
        result["porc_ambas_dosis"] = round((result["segunda_dosis"] / result["poblacion"]) * 100, 2)
    return result

def get_vaccines_by_province():
    pop_query = Query("population")
    pop_query.group_by(["provinciaid", "provincia"])
    pop_query.select(["provincia", "provinciaid", "sum(pop2021) as population"])
    query =  Query("covid19vacunasagrupadas")
    query.queryjoin(pop_query, "pops", "jurisdiccion_codigo_indec", "provinciaid")
    query.group_by(["jurisdiccion_codigo_indec", "jurisdiccion_nombre", "population"])
    query.select(["jurisdiccion_codigo_indec", "jurisdiccion_nombre, sum(primera_dosis_cantidad) as primera_dosis, sum(segunda_dosis_cantidad) as segunda_dosis, sum(segunda_dosis_cantidad) + sum(primera_dosis_cantidad) as total_dosis", "population as poblacion"])
    result = run_query(query.get())

    for e in result:
        e["porc_primera_dosis"] = round((e["primera_dosis"] / e["poblacion"]) * 100, 2)
        e["porc_ambas_dosis"] = round((e["segunda_dosis"] / e["poblacion"]) * 100, 2)
    return result


def get_all_vaccines_geodata():
    query = Query("covid19vacunasagrupadas")
    query.select(["jurisdiccion_codigo_indec", "jurisdiccion_nombre", "sum(primera_dosis_cantidad) as primera_dosis", "sum(segunda_dosis_cantidad) as segunda_dosis", "population as poblacion", "geom as geometry"])
    query.join("provincia", "jurisdiccion_codigo_indec", "inl")
    pop_query = Query("population")
    pop_query.group_by(["provinciaid", "provincia"])
    pop_query.select(["provincia", "provinciaid", "sum(pop2021) as population"])
    query.queryjoin(pop_query, "pops", "jurisdiccion_codigo_indec", "provinciaid")
    query.group_by(["jurisdiccion_codigo_indec", "jurisdiccion_nombre", "geom", "population"])

    result = run_query(query.get())

    for e in result:
        e["porc_primera_dosis"] = round((e["primera_dosis"] / e["poblacion"]) * 100, 2)
        e["porc_ambas_dosis"] = round((e["segunda_dosis"] / e["poblacion"]) * 100, 2)
    return result
