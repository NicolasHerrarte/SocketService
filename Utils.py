def auto_string_conversion(value):

    v = value.strip().lower()

    if v == "true":
        return True
    if v == "false":
        return False

    try:
        return int(value)
    except:
        pass

    try:
        return float(value)
    except:
        pass

    return value