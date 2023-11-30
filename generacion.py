import json

class GeneradorCodigo:
    def __init__(self, arbol_sintactico):
        self.arbol_sintactico = arbol_sintactico
        self.codigo_generado = []

    def generar_codigo(self, output_file="codigo_generado.asm"):
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

        self.codigo_generado.append("li $a0, 5")
        self.codigo_generado.append("la $t0, var_x")
        self.codigo_generado.append("sw $a0, 0($t0)")
        self.codigo_generado.append("la $t0, var_x")
        self.codigo_generado.append("lw $a0, 0($t0)")
        self.codigo_generado.append("sw $a0, 0($sp)")
        self.codigo_generado.append("addiu $sp, $sp, -4")
        self.codigo_generado.append("li $a0, 10")
        self.codigo_generado.append("lw $t1, 4($sp)")
        self.codigo_generado.append("add $a0, $a0, $t1")
        self.codigo_generado.append("addiu $sp, $sp, 4")
        self.codigo_generado.append("la $t0, var_y")
        self.codigo_generado.append("sw $a0, 0($t0)")
        self.codigo_generado.append("li $v0, 1")
        self.codigo_generado.append("syscall")
        self.codigo_generado.append("jr $ra")

    def _generar_fin_programa(self):
        pass


