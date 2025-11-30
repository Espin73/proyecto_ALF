import re

#Expresiones regulares 
patron_telefono = r"^\s*(\d{9})\s*$"
patron_nif = r"^\s*(?:\d{8}[A-Z]|[XYZ]\d{7}[A-Z])\s*$"

patron_fecha1 = r"^\s*\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}\s*$" #Primer formato de la fecha
patron_fecha2 = r"^[A-Za-z]+\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}\s*[AaPp][Mm]\s*$" #Segundo formato de la fecha
patron_fecha3 = r"^\s*\d{2}:\d{2}:\d{2}\s+\d{2}/\d{2}/\d{4}\s*$" #Tercer formato de la fecha

patron_coord1 = r"^\s*([+-]?\d+\.\d+)\s*,\s*([+-]?\d+\.\d+)\s*$" #Primer formato de las coordenadas
patron_coord2 = r"^\s*(\d+)°(\d+)'(\d+\.\d{4})\"\s*([NS])\s*,\s*(\d+)°(\d+)'(\d+\.\d{4})\"\s*([EW])\s*$" #Segundo formato de las coordenadas
patron_coord3 = r"^\s*(\d{3})(\d{2})(\d{2}\.\d{4})([NS])(\d{3})(\d{2})(\d{2}\.\d{4})([EW])\s*$" #Tercer formato de las coordenadas

#Comprobar expresiones regulares
re_telefono_sucio = re.compile(patron_telefono)
re_nif_sucio = re.compile(patron_nif)

re_f1_sucia = re.compile(patron_fecha1)
re_f2_sucia = re.compile(patron_fecha2)
re_f3_sucia = re.compile(patron_fecha3)

re_coord1_sucia = re.compile(patron_coord1)
re_coord2_sucia = re.compile(patron_coord2)
re_coord3_sucia = re.compile(patron_coord3)

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

#Funciones auxiliares para fecha
MESES = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12,}

def es_bisiesto(a):
    return (a % 4 == 0 and a % 100 != 0) or (a % 400 == 0)

def dias_meses(m, a):
    if m in (1,3,5,7,8,10,12):
        return 31
    if m in (4,6,9,11):
        return 30
    return 29 if es_bisiesto(a) else 28

#Funcion fecha
def validar_fecha(fecha: str):
    fecha_limpia = fecha.strip()
    coincidencia1 = re_f1_sucia.fullmatch(fecha_limpia)
    coincidencia2 = re_f2_sucia.fullmatch(fecha_limpia)
    coincidencia3 = re_f3_sucia.fullmatch(fecha_limpia)

    #Formato 1
    if coincidencia1:

        fecha_str, hora_str = fecha_limpia.split()
        a_str, m_str, d_str = fecha_str.split("-")
        H_str, M_str = hora_str.split(":")
        S_str = "0"

    #Formato 2
    elif coincidencia2:

        sin_ampm, ampm = fecha_limpia.rsplit(" ", 1)
        trozo_fecha, trozo_hora = sin_ampm.rsplit(" ", 1)

        mes_nombre, resto = trozo_fecha.split(" ",1)
        d_str, a_str = resto.replace(",", " ").split()
        H_str, M_str = trozo_hora.split(":")
        S_str = "0"
        
        #Por si nos dan un mes que no esté en el formato correcto
        mes_nombre = mes_nombre.capitalize()
        if mes_nombre not in MESES:
            return None
        m_str = str(MESES[mes_nombre])

        #Para ajustar las horas con lo de AM y PM
        H_aux = int(H_str)
        ampm = ampm.lower()
        if ampm == "pm" and H_aux != 12:
            H_aux += 12
        if ampm == "am" and H_aux == 12:
            H_aux = 0
        H_str = str(H_aux)
   

    #Formato 3
    elif coincidencia3:

        trozo_hora, trozo_fecha = fecha_limpia.split(" ",1)

        H_str, M_str, S_str = trozo_hora.split(":")
        d_str, m_str, a_str = trozo_fecha.split("/")

    else: 
        return None

    a = int(a_str)
    m = int(m_str)
    d = int(d_str)
    H = int(H_str)
    M = int(M_str)
    S = int(S_str)

    if not (1 <= m <= 12):
        return None
    if not (1 <= d <= dias_meses(m, a)):
        return None
    if not (0 <= H <= 23 and 0 <= M <= 59 and 0 <= S <= 59):
        return None

    return {"a": a, "m": m, "d": d, "H": H, "M": M, "S": S}


def validar_coord(coord):

    coord_limpia = coord.strip()
    coincidencia1 = re_coord1_sucia.fullmatch(coord_limpia)
    coincidencia2 = re_coord2_sucia.fullmatch(coord_limpia)
    coincidencia3 = re_coord3_sucia.fullmatch(coord_limpia)

    #Formato 1
    if coincidencia1:

        lat = float(coincidencia1.group(1))
        lon = float(coincidencia1.group(2))

        if not (-90 <= lat <= 90):
            return None
        if not (-180 <= lon <= 180):
            return None

        return {"lat": lat, "lon": lon}
    
    #Formato 2
    elif coincidencia2:

        g_lat, m_lat, s_lat, l_lat = coincidencia2.group(1), coincidencia2.group(2), coincidencia2.group(3), coincidencia2.group(4)
        g_lon, m_lon, s_lon, l_lon = coincidencia2.group(5), coincidencia2.group(6), coincidencia2.group(7), coincidencia2.group(8)

        g_lat, m_lat, s_lat = int(g_lat), int(m_lat), float(s_lat)
        g_lon, m_lon, s_lon = int(g_lon), int(m_lon), float(s_lon)

        if not (0 <= m_lat < 60 and 0 <= s_lat < 60):
            return None
        if not (0 <= m_lon < 60 and 0 <= s_lon < 60):
            return None
        
        lat = g_lat + (m_lat/60) + (s_lat/3600)
        lon = g_lon + (m_lon/60) + (s_lon/3600)

        if l_lat == 'S':
            lat = -lat
        if l_lon == 'W':
            lon = -lon

        if not (-90 <= lat <= 90):
            return None
        if not (-180 <= lon <= 180):
            return None
        
        return {"lat": lat, "lon": lon}

    elif coincidencia3:

        g_lat, m_lat, s_lat, l_lat = coincidencia3.group(1), coincidencia3.group(2), coincidencia3.group(3), coincidencia3.group(4)
        g_lon, m_lon, s_lon, l_lon = coincidencia3.group(5), coincidencia3.group(6), coincidencia3.group(7), coincidencia3.group(8)

        g_lat, m_lat, s_lat = int(g_lat), int(m_lat), float(s_lat)
        g_lon, m_lon, s_lon = int(g_lon), int(m_lon), float(s_lon)

        if not (0 <= m_lat < 60 and 0 <= s_lat < 60):
            return None
        if not (0 <= m_lon < 60 and 0 <= s_lon < 60):
            return None
        
        lat = g_lat + (m_lat/60) + (s_lat/3600)
        lon = g_lon + (m_lon/60) + (s_lon/3600)

        if l_lat == 'S':
            lat = -lat
        if l_lon == 'W':
            lon = -lon

        if not (-90 <= lat <= 90):
            return None
        if not (-180 <= lon <= 180):
            return None
        
        return {"lat": lat, "lon": lon}        


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

    #Normalizar telef
    telef_n = validar_telefono(telef_linea)
    if telef_n is None:
        return None
    
    #Normalizar nif
    nif_n = validar_nif(nif_linea)
    if nif_n is None:
        return None

    #Normalizar fecha
    fecha_n = validar_fecha(fecha_linea)
    if fecha_n is None:
        return None
    
    #Normalizar coordenadas
    coord_n = validar_coord(coord_linea)
    if coord_n is None:
        return None

    return {

        "telefono_normalizado": telef_n, "telefono_original": telef_linea, "nif": nif_n, "fecha": fecha_n, "coord": coord_n, "producto": prod_linea, "precio": precio_linea }       



    