
.data
        .word 4
.word 10
.word 7
.word 1
.word 5
.word 9
.word 2
.word 8
.word 23
.word 22
.word 56
.word 78
.word 89
.word 99
.word 89
.word 87

.word 45
.word 67
.word 56
.word 77
.word 45
.word 101
.word 787
.word 676
.word 34
.word 231
.word 17
.word 900
.word 500


.word 341

.word 44
.word 112
.word 75
.word 6
.word 3
.text
.globl main
main:
        addi $s6,$s6,0x10010000
 addi $t0,$zero,0  
addi $t1,$t1,34  # number of elements are 35
        addi $t8,$zero,1
        jal quick_sort#calling the function
   jal quick_sort
        jr $ra
        
        
        
       quick_sort:
	           slt $s0,$t0,$t1
	           beq $s0,$t8,start
	           
	           jr $ra
	           
	           
	           
	           start:
	                     addi $sp,$sp,-12
	                     sw $ra,0($sp)
	                     jal partition
	                     sw $t2,4($sp)
	                     sw $t1,8($sp)
	                     addi $t1,$t2,-1
	                     jal quick_sort
	                     
	                     lw $t1,8($sp)
	                     lw $s2,4($sp)
	                     addi $s2,$s2,1 
	                     addi $t0,$s2,0
	                     jal quick_sort
	                     lw $ra,0($sp)
	                     addi $sp,$sp,12 
	                     
	                     jr $ra
        


partition:
            #addi $sp,$sp,-12
            #sw $t0,0($sp)#start
            #sw $t1,4($sp)#end=n-1
            #sw $ra,8($sp)
            
            
            
            addi $t2,$t0,-1#i
            addi $t3,$t0,0 #j
            sll $t5,$t1,2
            add $t5,$t5,$s6 
            lw $t4,0($t5)
            
            loop:
                beq $t3,$t1,exit
                sll $s0,$t3,2 
                add $s0,$s0,$s6
                lw $s2,0($s0)
                slt $t6,$t4,$s2
                beq $t6,$zero,swap
                addi $t3,$t3,1 
                j loop
                
                swap:
                        addi $t2,$t2,1 
                        sll $s4,$t2,2 
                        add $s4,$s4,$s6 
                        lw $s1,0($s4)
                        sw $s1,0($s0)
                        sw $s2,0($s4)
                        addi $t3,$t3,1 
                        j loop
                        
                exit:
                        sll $s0,$t3,2 
                        add $s0,$s0,$s6
                        lw $s2,0($s0)
                        addi $t2,$t2,1 
                        sll $s4,$t2,2 
                        add $s4,$s4,$s6 
                        lw $s1,0($s4)
                        sw $s1,0($s0)
                        sw $s2,0($s4)
                        addi $t3,$t3,1
                jr $ra
                
            
            
            
            
            
            
            
            
            