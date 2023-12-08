import json

class GeneradorCodigo:
    def __init__(self, arbol_sintactico):
        self.arbol_sintactico = arbol_sintactico
        self.codigo_generado = []

    def generar_codigo(self, output_file="generacion_ifelse.asm"):
        self.codigo_generado = []
        self._generar_encabezado()
        self._generar_declaraciones()
        self._generar_main()
        self._generar_fin_programa()

        with open(output_file, "w") as file:
            file.write("\n".join(self.codigo_generado))

    def _generar_encabezado(self):
        self.codigo_generado.append(".data")

    def _generar_declaraciones(self):
        self.codigo_generado.append("var_a: .word 0")
        self.codigo_generado.append("var_b: .word 0")
        self.codigo_generado.append("mensaje_a_menor: .asciiz \"A es menor que B\\n\"")
        self.codigo_generado.append("mensaje_b_menor: .asciiz \"B es menor que A\\n\"")

    def _generar_main(self):
        self.codigo_generado.append(".text")
        self.codigo_generado.append("main:")

        # Declaración y asignación de variables
        self.codigo_generado.append("li $t0, 10")  # a = 10
        self.codigo_generado.append("sw $t0, var_a")
        self.codigo_generado.append("li $t0, 20")  # b = 20
        self.codigo_generado.append("sw $t0, var_b")

        # Comparación a < b
        self.codigo_generado.append("lw $t0, var_a")
        self.codigo_generado.append("lw $t1, var_b")
        self.codigo_generado.append("blt $t0, $t1, label_true")

        # label_false
        self.codigo_generado.append("label_false:")
        self.codigo_generado.append('la $a0, mensaje_b_menor')
        self.codigo_generado.append("li $v0, 4")  # Imprimir mensaje_b_menor
        self.codigo_generado.append("syscall")
        self.codigo_generado.append("j label_end")

        # label_true
        self.codigo_generado.append("label_true:")
        self.codigo_generado.append('la $a0, mensaje_a_menor')
        self.codigo_generado.append("li $v0, 4")  # Imprimir mensaje_a_menor
        self.codigo_generado.append("syscall")

        # label_end
        self.codigo_generado.append("label_end:")
        self.codigo_generado.append("jr $ra")

    def _generar_fin_programa(self):
        pass
