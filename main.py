import sys
from validador import extraer_linea, validar_telefono, validar_nif, validar_fecha


def main():

    if len(sys.argv) < 2:
        return sys.exit(1)
    
    comando = sys.argv[1]

    #Telefono
    if comando == "-sphone":

       if len(sys.argv) < 4:
            sys.exit(1)     
        
       telefono_buscado = sys.argv[2] # Argumento 2 es el teléfono
       fichero = sys.argv[3]
       
       telef = validar_telefono(telefono_buscado)
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

        if len(sys.argv) < 4:
            sys.exit(1)

        fichero = sys.argv[3]
        
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

    #Fecha
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


    elif comando == "-n":
        
        if len(sys.argv) < 3:
            sys.exit(1)
            
        fichero = sys.argv[2]
        
        ft = 3
        fc = 1
        
        if len(sys.argv) == 5:
            try:
                ft = int(sys.argv[3])
                fc = int(sys.argv[4])
                if not (1 <= ft <= 3) or not (1 <= fc <= 3):
                     sys.exit(1)
            except ValueError:
                sys.exit(1)
        elif len(sys.argv) != 3:
             sys.exit(1)

        try:

            from validador import formatear_fecha, formatear_coord
            
            with open(fichero, encoding="utf-8") as f:
                for linea in f:

                    datos = extraer_linea(linea)
                    
                    if datos is None:
                        continue 

                    fecha_str = formatear_fecha(datos["fecha"], ft)
                    coord_str = formatear_coord(datos["coord"], fc)
                    
                    telf_str = datos["telefono_normalizado"]
                    
                    nif_str = datos["nif"]
                    prod_str = datos["producto"]
                    precio_str = datos["precio"]

                    print(f"{telf_str} ; {nif_str} ; {fecha_str} ; {coord_str} ; {prod_str} ; {precio_str}")

        except Exception:
            sys.exit(1) 

    else:
        sys.exit(1)

if __name__ == "__main__":
    main()