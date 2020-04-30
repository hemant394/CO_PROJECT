instruction = {'addi': 1, 'add': 2, 'sub': 3, 'bne': 4, 'beq': 5, 'slt': 6, 'sll': 7, 'lw': 8, 'sw': 9, 'j': 11,
               'jr': 12, 'jal': 13,'multu':14,'mflo':15}
#registers = arr.array('i', [])
# memory = arr.array('i', [])
g = -1
h_instr=0

loops = {}
b=False
index=0
memory = [0] * 1024
commands = []
with open('quick_sort.s', 'r') as file:
    for line in file:
        result = line.find('#')
        if result != -1:
            line = line[0:result]
            line = line + '\n'
        if not line.isspace():
            commands.append(line)
f = open("quick_sort.s", "w")
for line in commands:
    f.write(line)
f.close()

list_command = []
temp_reg = []
temp_reg1 = []
i= 0


# def remove(string):
#   return string.replace(" ", "")
def remove_new(string):
    string = string.replace(":", "")
    return string.replace(" ", "")


def removewith(string):
    string = string.replace("$", "")
    return string.replace(" ", "")


def remove(string):
    string = string.replace("$", "")
    return string.replace(" ", "")


def add(list_command, temp_reg):  # addi,add,sub,slt,bne
    list_command.append(list(temp_reg))


fh = open('quick_sort.s')
line = fh.readline()
#print(line)
str = line.strip()
if str == '.data':
    h_instr=h_instr+1
    #print('111')
    line = fh.readline()
    #print(line)
    str = line.strip()
    str = str.split(' ', 1)

    if str[0] == '.word':
        h_instr = h_instr + 1
        if len(str) == 1:
            print('syntax error!')
            exit(1)
        if str[1][0:2] == '0x':
            r = int(str[1], 16)
            memory[i] = r
        else:
            memory[i] = int(str[1])
        #memory.insert(i, int(str[1]))
        #memory[i]=int(str[1])
        line = fh.readline()
        i = i + 1
        #print(line)
        str = line.strip()
        str = str.split(' ', 1)
        #print(str)
        #print('hii')
        while str[0] == '.word':
            h_instr = h_instr + 1
            if len(str) == 1:
                print('syntax error!')
                exit(1)
            memory[i] = int(str[1])
            #memory.insert(i, int(str[1]))
            i = i + 1
            line = fh.readline()
            #print(line)
            str = line.strip()
            str = str.split(' ', 1)
    if str[0] == '.text':
        h_instr = h_instr + 1
        #print('112')
        line = fh.readline()
        #print(line)
        str = line.strip()
        str = str.split(' ', 5)
        if len(str) == 2 and str[0] == '.globl' and str[1] == 'main':
            #print('113')
            line = fh.readline()
            #print(line)
            str = line.strip()
            if str == 'main:':
                h_instr = h_instr + 1
                #print('114')
                line = fh.readline()
                # print(line)
                str = line.strip()
                while line:
                    #print(line)
                    temp_reg = []
                    temp_reg3 = []
                    temp_reg1 = []
                    temp_regsp = []
                    first_word = str.split()[0]
                    #print(first_word)
                    # print(str)
                    if first_word not in instruction:
                        if first_word[len(first_word) - 1] == ':':
                            #print('new_loop')
                            #print(list_command)
                            first_word = remove_new(first_word)
                            loops[first_word] = len(list_command)
                            #print(loops)

                        else:
                            print(' instruction is not supported')
                            exit(1)

                    elif instruction[first_word] >= 1 and instruction[first_word] <= 7:
                        str = str.split(' ', 1)[1]
                        str = remove(str)
                        # print(str)
                        temp_reg.append(first_word)
                        temp_reg1 = str.split(',')
                        temp_reg.append(temp_reg1)
                        add(list_command, temp_reg)
                    elif instruction[first_word] == 9 or instruction[first_word] == 8:
                        first_word = str.split()[0]
                        temp_reg.append(first_word)
                        str = str.strip()
                        str = str.split(' ', 1)[1]
                        str = removewith(str)
                        temp_reg3 = str.split(',')
                        temp_regsp.append(temp_reg3[0])
                        str = temp_reg3[1]
                        temp_reg3 = str.split('(')
                        temp_reg3[1] = temp_reg3[1][0:len(temp_reg3[1]) - 1]
                        temp_regsp.append(temp_reg3[0])
                        temp_regsp.append(temp_reg3[1])
                        temp_reg.append(temp_regsp)
                        add(list_command, temp_reg)
                    elif instruction[first_word] == 12 or instruction[first_word] == 11 or instruction[
                        first_word] == 13 or instruction[first_word]==15:
                        if instruction[first_word] ==12:
                            if b==False:
                                index=len(list_command)
                                #print('index of ra')
                                #print(index)
                                b=True
                        temp_reg.append(first_word)
                        str = str.split(' ', 1)[1]
                        str = remove(str)
                        temp_reg.append(str)
                        list_command.append(temp_reg)
                        #print(list_command)
                        # temp_reg.clear()
                        # temp_reg1.clear()
                    elif instruction[first_word] == 14:
                        str = str.split(' ', 1)[1]
                        str = remove(str)
                        temp_reg.append(first_word)
                        temp_reg1 = str.split(',')
                        temp_reg.append(temp_reg1)
                        list_command.append(temp_reg)
                        #print(first_word)
                        #print(instruction[first_word])
                        #print(temp_reg)

                    line = fh.readline()
                    str = line.strip()
            else:
                print('main missing')
                exit(1)
        else:
            print('error in .globl main')
            exit(1)
    else:
        print('error .text missing')
        exit(1)
elif str == '.text':
    line = fh.readline()
    str = line.strip()
    str = str.split(' ', 5)
    if len(str) == 2 and str[0] == '.globl' and str[1] == 'main':
        line = fh.readline()
        str = line.strip()
        if str == 'main:':
            line = fh.readline()
            str = line.strip()
            while line:
                #print(line)
                temp_reg = []
                temp_reg3 = []
                temp_reg1 = []
                temp_regsp = []
                first_word = str.split()[0]
                #print(first_word)
                # print(str)
                if first_word not in instruction:
                    if first_word[len(first_word) - 1] == ':':
                        #print('new_loop')
                        #print(list_command)
                        first_word = remove_new(first_word)
                        loops[first_word] = len(list_command)
                        #print(loops)

                    else:
                        print('instruction is not supported')
                        exit(1)

                elif instruction[first_word] >= 1 and instruction[first_word] <= 7:
                    str = str.split(' ', 1)[1]
                    str = remove(str)
                    # print(str)
                    temp_reg.append(first_word)
                    temp_reg1 = str.split(',')
                    temp_reg.append(temp_reg1)
                    add(list_command, temp_reg)
                elif instruction[first_word] == 9 or instruction[first_word] == 8:
                    first_word = str.split()[0]
                    temp_reg.append(first_word)
                    str = str.strip()
                    str = str.split(' ', 1)[1]
                    str = removewith(str)
                    temp_reg3 = str.split(',')
                    temp_regsp.append(temp_reg3[0])
                    str = temp_reg3[1]
                    temp_reg3 = str.split('(')
                    temp_reg3[1] = temp_reg3[1][0:len(temp_reg3[1]) - 1]
                    temp_regsp.append(temp_reg3[0])
                    temp_regsp.append(temp_reg3[1])
                    temp_reg.append(temp_regsp)
                    add(list_command, temp_reg)
                elif instruction[first_word] == 12 or instruction[first_word] == 11 or instruction[first_word] == 13 or instruction[first_word] == 15:
                    temp_reg.append(first_word)
                    str = str.split(' ', 1)[1]
                    str = remove(str)
                    temp_reg.append(str)
                    list_command.append(temp_reg)
                    #print(list_command)
                    # temp_reg.clear()
                    # temp_reg1.clear()
                elif instruction[first_word] ==14:
                    str = str.split(' ', 1)[1]
                    str = remove(str)
                    temp_reg.append(first_word)
                    temp_reg1 = str.split(',')
                    temp_reg.append(temp_reg1)
                    list_command.append(temp_reg)
                    #print('multu')
                    #print(temp_reg)

                line = fh.readline()
                str = line.strip()
else:
    print(' error in finding segments')
    exit(1)
fh.close()
# print(len(list_command))
# print(memory)
#print(loops)
count = 0x10010000
registers = {'zero': 0, 'k1': 0, 'at': 0, 'v0': 0, 'v1': 0, 'a0': 3, 'a1': 0x7ffff6b4, 'a2': 0x7ffff6c4, 'a3': 0,
             't0': 0, 't1': 0,
             't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0,
             't7': 0, 's0': 0, 's1': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 't8': 0, 't9': 0, 'k0': 0, 'gp': 0x10008000, 'sp': 0x10011000, 's8': 0, 'ra': 0}

registers_dirty_bit = {'zero': 0, 'r0': 0, 'at': 0, 'v0': 0, 'v1': 0, 'a0': 0, 'a1': 0, 'a2': 0, 'a3': 0,
                       't0': 0, 't1': 0,
                       't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0,
                       't7': 0, 's0': 0, 's1': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 't8': 0,
                       't9': 0, 'k0': 0,
                       'k1': 0, 'gp': 0, 'sp': 0, 's8': 0, 'ra': 0}


lo=1
def add(str1, str2, str3):
    registers[str1] = registers[str2] + registers[str3]

registers['ra']=index

def addi(str1, str2, str3):
    r = 0
    if str3[0:2] == '0x':
        r = int(str3, 16)
    else:
        r = int(str3)
    registers[str1] = registers[str2] + r
def multu(str1,str2):
    lo=registers[str1]*registers[str2]
    return lo

def mflo(str1):
    registers[str1]=lo


def sub(str1, str2, str3):
    registers[str1] = registers[str2] - registers[str3]


def slt(str1, str2, str3):
    if registers[str2] < registers[str3]:
        registers[str1] = 1
    else:
        registers[str1] = 0


def sll(str1, str2, str3):
    registers[str1] = registers[str2] << int(str3)


def lw(str1, str2, str3):
    a = registers[str3] + int(str2) - count
    #print(a)
    a = a // 4
    # print(a)
    registers[str1] = memory[a]


def sw(str1, str2, str3):
    a = registers[str3] + int(str2) - count
    a = a // 4
    # print(a)
    memory[a] = registers[str1]

i_count=i
#print(list_command)
i = 0
print(list_command)
print()
print('REGISTERS = ',registers)
#print(len(list_command))



cycle = 0
flag = True
s = ['IF']
r = []
r.append(0)

while len(s) > 0:
    h = []
    d = []
    #global cycle
    cycle = cycle + 1
    #global g
    #global h_instr
    #g=r[len(s)-1]
   # print(cycle)
    #global flag



    while len(s) > 0:
        #print(r)
        # print('hii')
        # print(g)

        x = instruction[list_command[r[0]][0]]
        if s[0] == 'IF':
            #h_instr=h_instr+1
            if x == 1 or x == 2 or x == 3 or x == 6 or x == 7 or x == 8 or x == 9 or x==14 or x==15 :
                h.append('ID')
                d.append(r[0])
                g = g + 1
                if r[0] + 1 >= len(list_command):
                    flag = False
            elif x==4 or x==5 or x==11 or x==12 or x==13:
                h.append('ID')
                d.append(r[0])
                flag=False

        elif s[0] == 'ID':
            if x==11:
                flag=True
                h.append('EX')
                d.append(r[0])
                g=loops[list_command[r[0]][1]] - 1
            if x==12:
                flag = True
                h.append('EX')
                d.append(r[0])
                g = registers['ra'] - 1
                if registers['ra'] == index:
                    flag = False

            if x==13:
                flag = True
                h.append('EX')
                d.append(r[0])
                registers['ra'] = r[0] + 1
                g = loops[list_command[r[0]][1]] - 1



            if x == 1 or x == 2 or x == 3 or x == 6 or x == 7 or x == 8 or x == 9 or x==14 or x==15:
                # cycle=cycle+1
                #g = g + 1
                h.append('EX')
                d.append(r[0])
            elif x == 4 or x==5:
                if registers_dirty_bit[list_command[r[0]][1][1]] == 1 or registers_dirty_bit[
                    list_command[r[0]][1][0]] == 1:
                    #print('hemant')
                    h = h + s
                    d = d + r
                    break
                elif registers_dirty_bit[list_command[r[0]][1][1]] == 2 or registers_dirty_bit[
                    list_command[r[0]][1][0]] == 2:
                    h = h + s
                    #print('kumar')
                    d = d + r
                    break
                else:
                    g = g + 1
                    h.append('EX')
                    d.append(r[0])
                    #h = h + s
                    #d = d + r
                    if x==5:

                        if registers[list_command[r[0]][1][0]] != registers[list_command[r[0]][1][1]]:
                            flag = True
                            g=r[0]
                        else:
                            flag = False
                    if x==4:
                        #flag = True
                        if registers[list_command[r[0]][1][0]] == registers[list_command[r[0]][1][1]]:
                            flag = True
                            g=r[0]
                        else:
                            flag = False
                    #break


        elif s[0] == 'EX':
            if x == 1 or x == 2 or x == 3 or x == 6 or x == 7 or x == 8 or x == 9 or x== 4 or x==5 or x==11 or x==12 or x==13 or x==14 or x==15:
                # cycle=cycle+1


                if x == 15:
                    if registers_dirty_bit[list_command[r[0]][1]] == 1:
                        h = h + s
                        d = d + r
                        break
                    else:
                        registers_dirty_bit[list_command[r[0]][1]] = 2
                        mflo(list_command[r[0]][1])
                        print()
                        print('INSTRUCTION == ', list_command[r[0]])
                        print('REGISTERS == ', registers)

                if x == 14:
                    if registers_dirty_bit[list_command[r[0]][1][1]] == 1 or  registers_dirty_bit[list_command[r[0]][1][0]] == 1:
                        h = h + s
                        d = d + r
                        flag=False
                        break
                    else:
                        #registers_dirty_bit[list_command[r[0]][1]] = 2
                        flag=True
                        lo = multu(list_command[r[0]][1][0], list_command[r[0]][1][1])
                        print()
                        print('INSTRUCTION == ', list_command[r[0]])
                        print('lo == ',lo)
                        print('REGISTERS == ', registers)

                if x == 1:
                    if registers_dirty_bit[list_command[r[0]][1][1]] == 1:
                        h = h + s
                        d = d + r
                        break
                    else:
                        registers_dirty_bit[list_command[r[0]][1][0]] = 2
                        addi(list_command[r[0]][1][0], list_command[r[0]][1][1], list_command[r[0]][1][2])
                        print()
                        print('INSTRUCTION == ', list_command[r[0]])
                        print('REGISTERS == ', registers)

                elif x == 2:
                    if registers_dirty_bit[list_command[r[0]][1][1]] == 1 or registers_dirty_bit[
                        list_command[r[0]][1][2]] == 1:
                        h = h + s
                        d = d + r
                        break
                    else:
                        registers_dirty_bit[list_command[r[0]][1][0]] = 2
                        add(list_command[r[0]][1][0], list_command[r[0]][1][1], list_command[r[0]][1][2])
                        print()
                        print('INSTRUCTION == ', list_command[r[0]])
                        print('REGISTERS == ', registers)

                elif x == 3:
                    if registers_dirty_bit[list_command[r[0]][1][1]] == 1 or registers_dirty_bit[
                        list_command[r[0]][1][2]] == 1:
                        h = h + s
                        d = d + r
                        break
                    else:
                        registers_dirty_bit[list_command[r[0]][1][0]] = 2
                        sub(list_command[r[0]][1][0], list_command[r[0]][1][1], list_command[r[0]][1][2])
                        print()
                        print('INSTRUCTION == ', list_command[r[0]])
                        print('REGISTERS == ', registers)

                elif x == 6:
                    if registers_dirty_bit[list_command[r[0]][1][1]] == 1:
                        h = h + s
                        d = d + r
                        break
                    else:
                        registers_dirty_bit[list_command[r[0]][1][0]] = 2
                        slt(list_command[r[0]][1][0], list_command[r[0]][1][1], list_command[r[0]][1][2])
                        print()
                        print('INSTRUCTION == ', list_command[r[0]])
                        print('REGISTERS == ', registers)

                elif x == 4:
                    if registers_dirty_bit[list_command[r[0]][1][1]] == 1 or registers_dirty_bit[list_command[r[0]][1][0]] == 1:
                        h = h + s
                        d = d + r
                        break
                    else:
                        flag = True
                        print()
                        print('INSTRUCTION == ', list_command[r[0]])
                        print('REGISTERS == ', registers)
                        if registers[list_command[r[0]][1][0]] != registers[list_command[r[0]][1][1]]:
                            g = loops[list_command[r[0]][1][2]] - 1
                       # else:    #g is PC

                       # else:
                        #    g=g+1

                elif x == 5:
                    if registers_dirty_bit[list_command[r[0]][1][1]] == 1 or registers_dirty_bit[list_command[r[0]][1][0]] == 1:
                        h = h + s
                        d = d + r
                        break
                    else:
                        flag = True
                        print()
                        print('INSTRUCTION == ', list_command[r[0]])
                        print('REGISTERS == ', registers)
                        if registers[list_command[r[0]][1][0]] == registers[list_command[r[0]][1][1]]:
                            g = loops[list_command[r[0]][1][2]] - 1
                       # else:    #g is PC

                        #else:
                            #g=g+1

                elif x == 7:
                    if registers_dirty_bit[list_command[r[0]][1][1]] == 1:
                        h = h + s
                        d = d + r
                        break
                    else:
                        registers_dirty_bit[list_command[r[0]][1][0]] = 2
                        sll(list_command[r[0]][1][0], list_command[r[0]][1][1], list_command[r[0]][1][2])
                        print()
                        print('INSTRUCTION == ', list_command[r[0]])
                        print('REGISTERS == ', registers)

                elif x == 8:
                    if registers_dirty_bit[list_command[r[0]][1][2]] == 1:
                        h = h + s
                        d = d + r
                        break
                    else:
                        registers_dirty_bit[list_command[r[0]][1][0]] = 1


                elif x == 9:
                    if registers_dirty_bit[list_command[r[0]][1][2]] == 1:
                        h = h + s
                        d = d + r
                        break
                    else:
                        sw(list_command[r[0]][1][0], list_command[r[0]][1][1], list_command[r[0]][1][2])


                #print(h)
                h.append('MEM')
                d.append(r[0])

        elif s[0] == 'MEM':
            if x == 1 or x == 2 or x == 3 or x == 6 or x == 7 :
                registers_dirty_bit[list_command[r[0]][1][2]] = 0
                h.append('WB')
                d.append(r[0])

            if x==9:
                registers_dirty_bit[list_command[r[0]][1][2]] = 0
                h.append('WB')
                d.append(r[0])
                print()
                print('INSTRUCTION == ', list_command[r[0]])
                print('REGISTERS == ', registers)

            if x==15:
                registers_dirty_bit[list_command[r[0]][1]] = 0
                h.append('WB')
                d.append(r[0])

            if x==14:
                h.append('WB')
                d.append(r[0])
            if x==4 or x==5:
                #flag=True
                h.append('WB')
                d.append(r[0])
            elif x==8:
                registers_dirty_bit[list_command[r[0]][1][2]] = 0
                lw(list_command[r[0]][1][0], list_command[r[0]][1][1], list_command[r[0]][1][2])
                h.append('WB')
                d.append(r[0])
                print()
                print('INSTRUCTION == ', list_command[r[0]])
                print('REGISTERS == ', registers)
            #elif x==9:
             #   h.append('WB')
              #  d.append(r[0])
            elif x==11 or x==12 or x==13:
                h.append('WB')
                d.append(r[0])



        elif s[0]=='WB':
            h_instr = h_instr + 1
            #print(memory[0:i_count])
            if x==1 or x==2 or x==3 or x==6 or x==7 or x==8 or x==9:
                if registers_dirty_bit[list_command[r[0]][1][0]] == 1 or  registers_dirty_bit[list_command[r[0]][1][0]] == 2:
                    registers_dirty_bit[list_command[r[0]][1][0]] = 0
            if x==12:
                if registers['ra'] == index:
                    #print(list_command[i])
                    #print(memory[0:i_count])
                    #print(memory)
                    #print(len(list_command))
                    h=[]
                    d=[]
                    break


        #print(h)
        s.pop(0)
        r.pop(0)
    if g +1 >= len(list_command) :#and list_command[g][0]!='jr':
        flag = False
    #print('g == ',g)
    if flag:
        #print('hello')
        x = instruction[list_command[g][0]]
        if x == 1 or x == 2 or x == 3 or x == 6 or x == 7 or x==8 or x==9 or x==4 or x==5 or x==11 or x==12 or x==13 or x==14 or x==15:
            h.append('IF')
            d.append(g+1)
            #g=g+1

    s = h
    r = d


print()
print(' STATE OF REGISTERS IN THE END == ',registers)

print()
print('FULL MEMORY == ',memory)
print()
print('MEMORY USED == ',memory[0:i_count])
stalls=h_instr + 4
stalls=cycle-stalls
print('TOTAL NUMBER OF CYCLES == ',cycle)
#print(g)
print('number of instructions == ',h_instr)
print('stalls == ',stalls)
print('IPC == ',h_instr/cycle)
