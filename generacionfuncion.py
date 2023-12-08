import json

class GeneradorCodigo:
    def __init__(self, arbol_sintactico):
        self.arbol_sintactico = arbol_sintactico
        self.codigo_generado = []

    def generar_codigo(self, output_file="generacion_funcion.asm"):
        self.codigo_generado = []
        self._generar_encabezado()
        self._generar_declaraciones()
        self._generar_main()
        self._generar_funcion_suma()
        self._generar_fin_programa()

        with open(output_file, "w") as file:
            file.write("\n".join(self.codigo_generado))

    def _generar_encabezado(self):
        self.codigo_generado.append(".data")

    def _generar_declaraciones(self):
        self.codigo_generado.append("var_a: .word 0")
        self.codigo_generado.append("var_b: .word 0")
        self.codigo_generado.append("var_resultado: .word 0")

    def _generar_main(self):
        self.codigo_generado.append(".text")
        self.codigo_generado.append("main:")

        # Declaración y asignación de variables
        self.codigo_generado.append("li $t0, 8")
        self.codigo_generado.append("sw $t0, var_a")
        self.codigo_generado.append("li $t0, 9")
        self.codigo_generado.append("sw $t0, var_b")

        # Llamada a la función suma
        self._generar_llamada_funcion("suma", ["var_a", "var_b"])
        self.codigo_generado.append("sw $v0, var_resultado")

        # Imprimir resultado
        self.codigo_generado.append("li $v0, 1")
        self.codigo_generado.append("lw $a0, var_resultado")
        self.codigo_generado.append("syscall")

        # Retornar 0
        self.codigo_generado.append("li $v0, 10")
        self.codigo_generado.append("syscall")

    def _generar_funcion_suma(self):
        self.codigo_generado.append("suma:")
        self.codigo_generado.append("add $v0, $a0, $a1")  # resultado = a + b
        self.codigo_generado.append("jr $ra")

    def _generar_fin_programa(self):
        pass

    def _generar_llamada_funcion(self, nombre_funcion, parametros):
        # Espacio para guardar registros
        self.codigo_generado.append("addiu $sp, $sp, -4")
        self.codigo_generado.append("sw $ra, 0($sp)")

        # Generar código para los parámetros
        for i, parametro in enumerate(parametros):
            self.codigo_generado.append(f"lw $a{i}, {parametro}")

        # Llamada a la función
        self.codigo_generado.append(f"jal {nombre_funcion}")

        # Recuperar registros
        self.codigo_generado.append("lw $ra, 0($sp)")
        self.codigo_generado.append("addiu $sp, $sp, 4")

