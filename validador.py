import re

#Expresiones regulares 
patron_telefono = r"^\s*(\d{9})\s*$"
patron_nif = r"^\s*(?:\d{8}[A-Z]|[XYZ]\d{7}[A-Z])\s*$"

#Comprobar expresiones regulares
re_telefono_sucio = re.compile(patron_telefono)
re_nif_sucio = re.compile(patron_nif)

#Función telefono
def validar_telefono(telefono):

    coincidencia = re_telefono_sucio.fullmatch(telefono)

    if coincidencia:
        num = coincidencia.group(1)
        return "+34" + num
    else:
        return None

#Función NIF
def validar_nif(nif):
    
    letras_dni = "TRWAGMYFPDXBNJZSQVHLCKE"
    
    coincidencia = re_nif_sucio.fullmatch(nif)

    if not coincidencia:
        return None
    else:
        nif_limpio = coincidencia.group(0).strip()
        
        #DNI
        if nif_limpio[0].isdigit():
            cadena_num = nif_limpio[:8]
            letra = nif_limpio[8]
            
            n = int(cadena_num)
            indice = n % 23
            letra_esperada = letras_dni[indice]
            
            if letra == letra_esperada:
                return nif_limpio
            else:
                return None
        #NIE
        else:
            letra_inicio = nif_limpio[0]
            cadena_num = nif_limpio[1:8]
            letra_final = nif_limpio[8]

            inicio = {"X": "0", "Y": "1", "Z": "2"}
            cadena_num = inicio[letra_inicio] + cadena_num
            
            n = int(cadena_num)

            indice = n % 23
            letra_esperada = letras_dni[indice]
            
            if letra_final == letra_esperada:
                return nif_limpio
            else:
                return None    

def extraer_linea(linea: str):

    partes = linea.split(";")
    if len(partes) != 6:
        return None
    
    telef_linea = partes[0].strip()
    nif_linea = partes[1].strip()
    fecha_linea = partes[2].strip()
    coord_linea = partes[3].strip()
    prod_linea = partes[4].strip()
    precio_linea = partes[5].strip()

    #Normalizar
    telef_n = validar_telefono(telef_linea)
    if telef_n is None:
        return None
    
    nif_n = validar_nif(nif_linea)
    if nif_n is None:
        return None

    return {

        "telefono_normalizado": telef_n, "telefono_original": telef_linea, "nif": nif_n, "fecha": fecha_linea, "coord": coord_linea, "producto": prod_linea, "precio": precio_linea }       



    