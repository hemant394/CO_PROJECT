.data
.text
.globl main
main:
	addi $s6,$zero,7 #factorial(7)=$s3=5040
	jal fact
	jr $ra
	fact:
	beq $s6,$zero,exit
	addi $sp,$sp,-8
	sw $ra,0($sp)
         sw $s6,4($sp)
	addi $s6,$s6,-1
	jal fact
	lw $ra,0($sp)
        lw $s2,4($sp)
	multu $s3, $s2
        mflo $s3
        addi $sp,$sp,8
	jr $ra
	exit:
	addi $s3,$s3,1
	jr $ra