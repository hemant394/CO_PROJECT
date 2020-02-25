.data
	.word 12
.word 34
.word 67
.word  1
.word  45
.word  90
   .word 6#nvrjrk
.word  11
.word  33



.word  67
#hemnjnxa
.word  19
.text
#fndcj
.globl main
main:
addi $s6,$s6,0x10010000
addi $t7,$t7,1
addi $s0,$s0,1
addi $s7,$s7,-1
addi $t5,$t5,11 #number of elements are 11
loop:  
addi $s1,$s0,-1
                sll $t1,$s0,2
                add $t1,$t1,$s6
                lw $t2,0($t1)
                loopa:
                     beq $s7,$s1,exit
                     sll $t1,$s1,2
                     add $t1,$t1,$s6
                     lw $s3,0($t1)
                     slt $s5,$s3,$t2
                     beq $s5,$zero,new
                     beq $t7,$s5,exit#hemanjdk
                     j loopa
                     new:
                            sw $s3,4($t1)
                            addi $s1,$s1,-1
                            j loopa
                     exit:  
                            addi $t4,$s1,1
                            sll $t1,$t4,2
                            add $t1,$t1,$s6                            
                            sw $t2,0($t1)
                            addi $s0,$s0,1
                            beq $t5,$s0,exi
                            j loop   
                    exi:
                    jr $ra