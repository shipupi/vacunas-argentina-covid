from api.persistence.db_driver import run_query
from api.persistence.query_helper import Query


def get_departments_by_province(province):
    query = Query("departamento")
    query.select(["gid", "fna", "gna", "nam", "inl", "fdc", "sag", "pop2021 as poblacion"])
    query.join("population", "inl", "departamentoid")
    query.where("inl LIKE %s || '%%'")
    data = [province]
    departments = run_query(query.get(), data=data)
    return departments

def get_departments():
    query = Query("departamento")
    query.select(["gid", "fna", "gna", "nam", "inl", "fdc", "sag", "pop2021 as poblacion"])
    query.join("population", "inl", "departamentoid")
    departments = run_query(query.get())
    return departments

# Hacemos la query a mano porque el join no es soportado por el query builder
def get_province_geospatial(province):
    query = "SELECT depto_residencia, codigo_indec, depto_residencia_id, "\
        "sum(cantidad) as cantidad_dosis, "\
        "orden_dosis, "\
        "dep.geom as geometry "\
        "from dosis_por_distrito dosis, departamento dep " \
        "WHERE dosis.codigo_indec = dep.inl " \
        "AND dosis.jurisdiccion_residencia_id = %s "\
        "GROUP BY depto_residencia, depto_residencia_id, codigo_indec, dep.geom, orden_dosis"
    print(query)
    data = [province]
    return run_query(query, data=data)

def get_vaccines_by_department(province=None):
    query = Query("dosis_por_distrito")
    if province:
        query.where("jurisdiccion_residencia_id = %s")
        data = [province]
    else:
        data = None
    departments = run_query(query.get(), data=data)
    departments_merged = {}
    for d in departments:
        dept_id = d["codigo_indec"]
        ndosis = d["orden_dosis"]
        this_dosis = "primera_dosis"
        other_dosis = "segunda_dosis"
        if ndosis == 2:
            this_dosis = "segunda_dosis"
            other_dosis = "primera_dosis"
        if dept_id in departments_merged:
            departments_merged[dept_id][this_dosis] += d["cantidad"]
            departments_merged[dept_id]["total_dosis"] += d["cantidad"]
        else:
            d[this_dosis] = d["cantidad"]
            d[other_dosis] = 0
            d["total_dosis"] = d["cantidad"]
            del d["vacuna"]
            del d["orden_dosis"]
            del d["cantidad"]
            departments_merged[dept_id] = d

    return list(departments_merged.values())