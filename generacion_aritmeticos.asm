import json

class GeneradorCodigo:
    def __init__(self, arbol_sintactico):
        self.arbol_sintactico = arbol_sintactico
        self.codigo_generado = []

    def generar_codigo(self, output_file="generacion_aritmeticos.asm"):
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
        self.codigo_generado.append("var_x: .word 0")
        self.codigo_generado.append("var_y: .word 0")

    def _generar_main(self):
        self.codigo_generado.append(".text")
        self.codigo_generado.append("main:")

        self.codigo_generado.append("li $t0, 5")
        self.codigo_generado.append("sw $t0, var_x")

        self.codigo_generado.append("lw $t0, var_x")
        self.codigo_generado.append("li $t1, 7")
        self.codigo_generado.append("sub $t2, $t1, $t0")
        self.codigo_generado.append("li $t3, 10")
        self.codigo_generado.append("mul $t4, $t3, $t2")
        self.codigo_generado.append("add $t5, $t4, $t0")
        self.codigo_generado.append("sw $t5, var_y")

        self.codigo_generado.append("li $v0, 1")
        self.codigo_generado.append("lw $a0, var_y")
        self.codigo_generado.append("syscall")

        self.codigo_generado.append("jr $ra")

    def _generar_fin_programa(self):
        pass
