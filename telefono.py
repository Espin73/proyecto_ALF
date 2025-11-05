import regex as re


patron_telefono = r"^\s*(\d{9})\s*$"

er_telefono = re.compile(patron_telefono)

def comprobar_telefono(telefono):

    coincidencia = er_telefono.fullmatch(telefono)

    if coincidencia:
        num = coincidencia.group(1)
        return "+34" + num
    else:
        return None