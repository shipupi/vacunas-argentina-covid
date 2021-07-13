from api.persistance.db_driver import run_query
from api.persistance.query_helper import Query
def get_provinces():
    query = "Select gid, fna, gna, nam, inl FROM provincia"
    provinces = run_query(query)
    return provinces

def get_vaccines_by_province(province=None, geospatial=False):
    data = province
    query =  Query("covid19vacunasagrupadas")
    if province:
        query.where("jurisdiccion_codigo_indec = %s")
    query.group_by(["jurisdiccion_codigo_indec", "jurisdiccion_nombre"])
    query.select(["jurisdiccion_codigo_indec", "jurisdiccion_nombre, sum(primera_dosis_cantidad) as primera_dosis, sum(segunda_dosis_cantidad) as segunda_dosis, sum(segunda_dosis_cantidad) + sum(primera_dosis_cantidad) as total_dosis"])
    print(query.get(), data)
    return run_query(query.get(),data=data)