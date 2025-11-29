import re
import sys
from validador import extraer_linea, validar_telefono, validar_nif

def main():

    if len(sys.argv) < 4:
        return None
    
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

    else:
        sys.exit(1)

    

if __name__ == "__main__":
    main()