from api.persistance.db_driver import run_query
from api.persistance.query_helper import Query
def get_provinces():
    query = "Select gid, fna, gna, nam, inl FROM provincia"
    provinces = run_query(query)
    return provinces

def get_vaccines_by_province(province=None, geospatial=False):
    if geospatial:
        if province:
            return get_province_geodata(province)
        else:
            return get_all_vaccines_geodata()
    data = province
    query =  Query("covid19vacunasagrupadas")
    if province:
        query.where("jurisdiccion_codigo_indec = %s")
    query.group_by(["jurisdiccion_codigo_indec", "jurisdiccion_nombre"])
    query.select(["jurisdiccion_codigo_indec", "jurisdiccion_nombre, sum(primera_dosis_cantidad) as primera_dosis, sum(segunda_dosis_cantidad) as segunda_dosis, sum(segunda_dosis_cantidad) + sum(primera_dosis_cantidad) as total_dosis"])
    return run_query(query.get(),data=data)

def get_province_geodata(province):
    query = "SELECT * "\
        "from dosis_por_distrito d, departamento geo " \
        "WHERE d.codigo_indec = geo.inl " \
        "AND d.jurisdiccion_residencia_id = %s"\
        "GROUP BY jurisdiccion_codigo_indec, jurisdiccion_nombre, p.geom"
    return run_query(query, province)

def get_all_vaccines_geodata():
    # Hacemos la query a mano porque el join no es soportado por el query builder
    query = "SELECT v.jurisdiccion_codigo_indec, v.jurisdiccion_nombre,"\
        " sum(primera_dosis_cantidad) as primera_dosis, "\
        "sum(segunda_dosis_cantidad) as segunda_dosis, "\
        "sum(segunda_dosis_cantidad) + sum(primera_dosis_cantidad) as total_dosis, "\
        "p.geom "\
        "from covid19vacunasagrupadas v, provincia p " \
        "WHERE v.jurisdiccion_codigo_indec = p.inl " \
        "GROUP BY jurisdiccion_codigo_indec, jurisdiccion_nombre, p.geom"
    return run_query(query)