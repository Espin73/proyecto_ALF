import sys
from validador import extraer_linea, validar_telefono, validar_nif, validar_fecha


def main():

    if len(sys.argv) < 4:
        return sys.exit(1)
    
    comando = sys.argv[1]
    fichero = sys.argv[3]


    #Telefono
    if comando == "-sphone":

       telef = validar_telefono(sys.argv[2])
       if telef is None:
           sys.exit(1)
       
       try:
           with open(fichero, encoding="utf-8") as f:
               for linea in f:
                    
                    linea_extraida = extraer_linea(linea)
                    if linea_extraida is None:
                        continue

                    if linea_extraida["telefono_normalizado"] == telef:
                        print(linea.rstrip("\n"))
       except:
           sys.exit(1)

    #NIF
    elif comando == "-snif":

        nif_normalizado = validar_nif(sys.argv[2])
        if nif_normalizado is None:
            sys.exit(1)
        
        try:
            with open(fichero, encoding="utf-8") as f:
                for linea in f:
                    
                    linea_extraida = extraer_linea(linea)
                    if linea_extraida is None:
                        continue

                    if linea_extraida["nif"] == nif_normalizado:
                        print(linea.rstrip("\n"))
        except:
            sys.exit(1)

    elif comando == "-stime":

        if len(sys.argv) < 5:
            return sys.exit(1)
        
        desde_str = sys.argv[2]
        hasta_str = sys.argv[3]
        fichero = sys.argv[4]

        desde = validar_fecha(desde_str)
        hasta = validar_fecha(hasta_str)

        if desde is None or hasta is None:
            sys.exit(1)
        
        try:
            with open(fichero, encoding="utf-8") as f:
                for linea in f:
                    
                    linea_extraida = extraer_linea(linea)
                    if linea_extraida is None:
                        continue
                    
                    fecha = linea_extraida["fecha"]
                    
                    fecha_valores = (fecha["a"], fecha["m"], fecha["d"], fecha["H"], fecha["M"], fecha["S"])
                    desde_valores = (desde["a"], desde["m"], desde["d"], desde["H"], desde["M"], desde["S"])
                    hasta_valores = (hasta["a"], hasta["m"], hasta["d"], hasta["H"], hasta["M"], hasta["S"])
                    
                    if desde_valores <= fecha_valores <= hasta_valores:
                        print(linea.rstrip("\n"))
        except:
            sys.exit(1)

    else:
        sys.exit(1)

    

if __name__ == "__main__":
    main()