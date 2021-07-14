from api.persistence.db_driver import run_query
from api.persistence.query_helper import Query

def get_provinces():
    query = "Select gid, fna, gna, nam, inl FROM provincia"
    provinces = run_query(query)
    return provinces

def get_vaccines_by_province(province=None):
    data = [province]
    query =  Query("covid19vacunasagrupadas")
    if province:
        query.where("jurisdiccion_codigo_indec = %s")
    query.group_by(["jurisdiccion_codigo_indec", "jurisdiccion_nombre"])
    query.select(["jurisdiccion_codigo_indec", "jurisdiccion_nombre, sum(primera_dosis_cantidad) as primera_dosis, sum(segunda_dosis_cantidad) as segunda_dosis, sum(segunda_dosis_cantidad) + sum(primera_dosis_cantidad) as total_dosis"])
    return run_query(query.get(),data=data)


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