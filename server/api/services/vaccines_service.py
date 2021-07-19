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

    first_dose = 0
    second_dose = 0
    total = 0
    population = 0
    for p in by_province:
        first_dose += p["primera_dosis"]
        second_dose += p["segunda_dosis"]
        total+= p["total_dosis"]
        population += p["poblacion"]
    response = {
        "primera_dosis": first_dose,
        "segunda_dosis": second_dose,
        "poblacion": population,
        "porcentaje_primera_dosis": round(first_dose / population * 100, 2),
        "porcentaje_ambas_dosis": round(second_dose / population * 100, 2)
    }
    return response

def get_brand_timeline():
    query = Query("timeline")
    fields = ["fecha_aplicacion", "orden_dosis", "vacuna"]
    query.group_by(fields)
    fields.append("sum(cantidad) as cantidad")
    query.select(fields)
    query.orderby("fecha_aplicacion", "ASC")
    query.orderby("vacuna", "ASC")
    query.orderby("orden_dosis", "ASC")
    return run_query(query.get())

def get_timeline():
    query = Query("timeline")
    fields = ["fecha_aplicacion", "orden_dosis"]
    query.group_by(fields)
    fields.append("sum(cantidad) as cantidad")
    query.select(fields)
    query.orderby("fecha_aplicacion", "ASC")
    query.orderby("orden_dosis", "ASC")

    pop_query = Query("population")
    pop_query.select("sum(pop2021) as sum")
    pop = run_query(pop_query.get())
    pop = pop[0]['sum']
    result = run_query(query.get())
    days = {}
    acums = {
        "primera_dosis": 0,
        "segunda_dosis": 0
    }
    # Asumimos que vienen ordenados por dia. Por eso podemos llevar el contador de acums por afuera del ciclo
    # Sin tener que buscar el valor del dia anterior
    for r in result:
        ndosis = r["orden_dosis"]
        this_dosis = "primera_dosis"
        other_dosis = "segunda_dosis"
        if ndosis == 2:
            this_dosis = "segunda_dosis"
            other_dosis = "primera_dosis"
        day = r["fecha_aplicacion"]
        if day in days:
            days[day][this_dosis] = r["cantidad"]
            acums[this_dosis] += r["cantidad"]
            days[day]["acum_{}".format(this_dosis)] = acums[this_dosis]
            days[day]["porc_{}".format(this_dosis)] = round(acums[this_dosis] / pop * 100, 2)
        else:
            acums[this_dosis] += r["cantidad"]
            days[day] = {
                "fecha": day,
                this_dosis: r["cantidad"],
                "acum_{}".format(this_dosis): acums[this_dosis],
                "porc_{}".format(this_dosis): round(acums[this_dosis] / pop * 100, 2)
            }
    
    last = {
        "primera_dosis": 0,
        "segunda_dosis": 0
    }
    for d in days:
        for dosis in last:
            if dosis not in days[d]:
                days[d][dosis] = 0
                days[d]["acum_{}".format(dosis)] = last[dosis]
                days[d]["porc_{}".format(dosis)] = round(last[dosis] / pop * 100, 2)
            else:
                last[dosis] = days[d]["acum_{}".format(dosis)]
    return list(days.values())