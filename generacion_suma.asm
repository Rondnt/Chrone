.data
var_x: .word 0
var_y: .word 0
.text
main:
li $a0, 5
la $t0, var_x
sw $a0, 0($t0)
la $t0, var_x
lw $a0, 0($t0)
sw $a0, 0($sp)
addiu $sp, $sp, -4
li $a0, 10
lw $t1, 4($sp)
add $a0, $a0, $t1
addiu $sp, $sp, 4
la $t0, var_y
sw $a0, 0($t0)
li $v0, 1
syscall
jr $ra
