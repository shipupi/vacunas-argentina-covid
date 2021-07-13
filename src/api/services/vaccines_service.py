from api.persistence.db_driver import run_query
from api.services.provinces_service import get_vaccines_by_province


def get_arrivals():
    arrivals  = run_query("SELECT * FROM actas_de_recepcion_vacunas")
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

