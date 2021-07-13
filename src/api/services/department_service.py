from api.persistance.db_driver import run_query
from api.persistance.query_helper import Query



# Hacemos la query a mano porque el join no es soportado por el query builder
def get_province_geospatial(province):
    query = "SELECT depto_residencia, codigo_indec, depto_residencia_id, "\
        "sum(cantidad) as cantidad_dosis, "\
        "orden_dosis, "\
        "dep.geom "\
        "from dosis_por_distrito dosis, departamento dep " \
        "WHERE dosis.codigo_indec = dep.inl " \
        "AND dosis.jurisdiccion_residencia_id = %s "\
        "GROUP BY depto_residencia, depto_residencia_id, codigo_indec, dep.geom, orden_dosis"
    print(query)
    data = [province]
    return run_query(query, data=data)