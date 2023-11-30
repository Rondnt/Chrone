from lexico import main as lexico_main
from generacion import GeneradorCodigo

def main():
    # Ejecutar el analizador léxico
    lexico_main()

    # Crear un generador de código
    generador = GeneradorCodigo(None)

    # Generar código y guardar en el archivo
    generador.generar_codigo(output_file="codigo_generado.asm")

    # Finalmente, ejecutar el analizador semántico
    #semantico_main()

if __name__ == '__main__':
    # Ejecutar la función main al ejecutar main.py
    main()
