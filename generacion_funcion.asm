.data
var_a: .word 0
var_b: .word 0
var_resultado: .word 0
.text
main:
li $t0, 8
sw $t0, var_a
li $t0, 9
sw $t0, var_b
addiu $sp, $sp, -4
sw $ra, 0($sp)
lw $a0, var_a
lw $a1, var_b
jal suma
lw $ra, 0($sp)
addiu $sp, $sp, 4
sw $v0, var_resultado
li $v0, 1
lw $a0, var_resultado
syscall
li $v0, 10
syscall
suma:
add $v0, $a0, $a1
jr $ra
