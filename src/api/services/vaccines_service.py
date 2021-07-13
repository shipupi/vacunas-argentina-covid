from api.persistance.db_driver import run_query


def get_vaccines():
    return {"message": "Hello World"}

def get_arrivals():
    arrivals  = run_query("SELECT * FROM actas_de_recepcion_vacunas")
    return arrivals


