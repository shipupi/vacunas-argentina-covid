
def validate_int_parameter(param):
    if param and param.isdigit():
        return int(param)
    return None


def validate_bool_param(param):
    if param and param.lower() == "true":
        return True
    return False
