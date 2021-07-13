from api.persistence.db_driver import run_query
from api.persistence.query_helper import Query
from api.services.provinces_service import get_vaccines_by_province


def get_arrivals():
    # Hacemos a mano porque el query builder no soporta join
    query = "SELECT * FROM actas_de_recepcion_vacunas, vacunas WHERE actas_de_recepcion_name = empresa "\
        "ORDER BY fecha_entrega ASC, nomivac_name ASC"
    arrivals  = run_query(query)
    return arrivals


def get_bignumbers():
    by_province = get_vaccines_by_province()
    print(by_province)

    first_dose = 0
    second_dose = 0
    total = 0
    for p in by_province:
        first_dose += p["primera_dosis"]
        second_dose += p["segunda_dosis"]
        total+= p["total_dosis"]
    response = {
        "primera_dosis": first_dose,
        "segunda_dosis": second_dose,
        "total": total
    }
    return response

def get_timeline():
    query = Query("timeline")
    fields = ["fecha_aplicacion", "orden_dosis", "vacuna"]
    query.group_by(fields)
    fields.append("sum(cantidad) as cantidad")
    query.select(fields)
    query.orderby("fecha_aplicacion", "ASC")
    query.orderby("vacuna", "ASC")
    query.orderby("orden_dosis", "ASC")
    return run_query(query.get())