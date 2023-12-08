from lexico import main as lexico_main
#from generacionsuma import GeneradorCodigo
#from generacionaritmeticos import GeneradorCodigo
#from generacionifelse import GeneradorCodigo
from generacionfuncion import GeneradorCodigo


def main():
    # Ejecutar el analizador léxico
    lexico_main()

    # Crear un generador de código
    generador = GeneradorCodigo(None)

    # Generar código y guardar en el archivo
    #generador.generar_codigo(output_file="generacion_suma.asm")
    #generador.generar_codigo(output_file="generacion_aritmeticos.asm")
    #generador.generar_codigo(output_file="generacion_ifelse.asm")
    generador.generar_codigo(output_file="generacion_funcion.asm")


    # Finalmente, ejecutar el analizador semántico
    #semantico_main()

if __name__ == '__main__':
    # Ejecutar la función main al ejecutar main.py
    main()
