instruction = {'addi': 1, 'add': 2, 'sub': 3, 'bne': 4, 'beq': 5, 'slt': 6, 'sll': 7, 'lw': 8, 'sw': 9, 'j': 11,
               'jr': 12, 'jal': 13,'multu':14,'mflo':15}
#registers = arr.array('i', [])
# memory = arr.array('i', [])

value_sw=0

def remove(string):
    string = string.replace("$", "")
    return string.replace(" ", "")

g = -1
h_instr=0
cachemiss1=0
cachetotal1=0

cachemiss2=0
cachetotal2=0


cache1_size=64
cache2_size=256
block_size=16
#block_size1=8
cache1_latency=0
cache2_latency=2
memory_latency=10#memory access time
associativity=2

commands_cache = []
with open('INPUT_FOR_CACHE.txt', 'r') as file:
    for line in file:
        result = line.find('#')
        if result != -1:
            line = line[0:result]
            line=remove(line)
            #line = line + '\n'
        if not line.isspace():
            commands_cache.append(line)
print(commands_cache)
str_line=commands_cache[0]
res_index=str_line.find('k')
print('res',res_index)
if res_index == -1:
    res_index = str_line.find('b')
    str_line = str_line[0:res_index ]
    print('64 ==',str_line)
    cache1_size = (int(str_line)) //4

else:
    str_line = str_line[0:res_index]
    print('64kb ==', str_line)
    cache1_size=256*(int(str_line))
del commands_cache[0]


str_line=commands_cache[0]
res_index=str_line.find('k')
if res_index == -1:
    res_index = str_line.find('b')
    str_line = str_line[0:res_index ]
    cache2_size =  (int(str_line)) //4

else:
    str_line = str_line[0:res_index ]
    cache2_size = 256 * (int(str_line))

del commands_cache[0]

str_line=commands_cache[0]
block_size=(int(str_line))
del commands_cache[0]

str_line=commands_cache[0]
associativity=(int(str_line))
del commands_cache[0]

str_line=commands_cache[0]
cache1_latency=(int(str_line))
del commands_cache[0]

str_line=commands_cache[0]
cache2_latency=(int(str_line))
del commands_cache[0]

str_line=commands_cache[0]
memory_latency=(int(str_line))
del commands_cache[0]

#f = open("INPUT_FOR_CACHE.txt", "w")
#for line in commands:
 #   f.write(line)
#f.close()
#print(commands_cache)







blocks=[0]*block_size

qcache1=[blocks]*(cache1_size // block_size)
qcache2=[blocks]*(cache2_size // block_size)


loops = {}
b=False
index=0
memory_total_size = 16384# 64KB == number of words == 16384
memory = [0] * memory_total_size
memory_size=memory_total_size


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
count = 268500992
spsize=268500992 + 4*memory_size
registers = {'zero': 0, 'k1': 0, 'at': 0, 'v0': 0, 'v1': 0, 'a0': 3, 'a1': 0, 'a2': 0, 'a3': 0, 't0': 0, 't1': 0, 't2': 0,
             't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 's0': 0, 's1': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 't8': 0,
             't9': 0, 'k0': 0, 'gp': 0, 'sp': spsize ,'s8': 0, 'ra': 0}

registers_dirty_bit = {'zero': 0, 'r0': 0, 'at': 0, 'v0': 0, 'v1': 0, 'a0': 0, 'a1': 0, 'a2': 0, 'a3': 0,
                       't0': 0, 't1': 0,
                       't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0,
                       't7': 0, 's0': 0, 's1': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 't8': 0,
                       't9': 0, 'k0': 0,
                       'k1': 0, 'gp': 0, 'sp': 0, 's8': 0, 'ra': 0}



def memory_read(addr):
    global cycle
    #addr = address - count
    cycle = cycle + memory_latency
    addr = addr * block_size
    temp_list=[]
    for kk in range(addr,addr + block_size):
        #print('kkk',kk)
        temp_list.append(memory[kk])
    return  temp_list

def memory_write(addr,listt):
    global cycle
    cycle = cycle + memory_latency
    for kk in range(addr,addr + block_size):
        memory[kk]=listt[kk-addr]


valid_cache2=[-1]*(cache2_size // block_size)
dir_cache2=[0]*(cache2_size // block_size)

s111 = 0

def cache2_read(addr,address):
    global cachemiss2
    global cachetotal2
    global cycle
    global s111
    global value_sw
    cachetotal2=cachetotal2 + 1
    cain2 = (cache2_size // block_size) // associativity
    blonum2 = addr % cain2
    s11 = associativity * blonum2
    found=False
    s111 = s11
    if value_sw == 1:
        for hh in range(s11, s11 + associativity):
            if valid_cache2[hh] == addr:
                dir_cache2[hh] = 1
                break


    for hh in range(s11, s11 + associativity):
        if valid_cache2[hh] == addr:
            cycle = cycle + cache1_latency
            found=True
            ret=qcache2[hh]
            val_temp=valid_cache2[hh]
            dir_temp=dir_cache2[hh]
            rk = hh
            for jk in range(hh,s11 + associativity - 1):
                rk=jk
                if valid_cache2[ jk + 1] != -1:
                    dir_cache2[jk]=dir_cache2[jk + 1]
                    valid_cache2[jk] = valid_cache2[jk + 1]
                    qcache2[jk]=qcache2[jk+1]

            qcache2[rk ] = ret
            dir_cache2[rk ]=dir_temp
            valid_cache2[rk ] = val_temp
            #print('checking cache 2',qcache2)
            return ret
            #write through in cache1 the element which we got here
            #and write through in cache 2 the element ehich got deleted from cache1
            #break
        elif valid_cache2[hh] == -1:
            cachemiss2 = cachemiss2 + 1
            # memory se nikal ke laana
            cycle = cycle + cache1_latency +cache2_latency
            return  memory_read(address)
    if not found :
        cachemiss2 = cachemiss2 + 1
        cycle = cycle + cache1_latency + cache2_latency
        temper = memory_read(address)
        ''''#tra_to_mem = qcache2[s11]
        if dir_cache2[s11] == 1:
            memory_write(valid_cache2[s11],qcache2[s11])
            dir_cache2[s11] = 0

        for iii in range(s11, s11 + associativity - 1):
            valid_cache2[iii] = valid_cache2[iii + 1]
            dir_cache2[iii] = dir_cache2[iii + 1]
            qcache2[iii] = qcache2[iii + 1]
        qcache2[s11 + associativity - 1] = temper
        dir_cache2[s11 + associativity - 1] = 0
        valid_cache2[s11 + associativity - 1] = addr'''
        return  temper





valid_cache1=[-1]*(cache1_size // block_size)

dir_cache1=[0]*(cache1_size // block_size)

s12 = 0

def cache1_read(address):
    #print('cache1=',cache1_size)
    #print('address === ',address)
    ca=cache1_size // block_size
    global  cachemiss1
    global value_sw
    global s12
    global cachetotal1
    #print("dirt cache print",dir_cache1)




    cachetotal1 = cachetotal1 + 1
    #print("ca====",ca)
    cain=ca // associativity
    #print("cain====", cain)
    addr = address
    addr=addr // block_size
    address = addr
    addr = block_size*addr
    #print('cain===',cain)
    blonum= address % cain
    s1=associativity*blonum
    if value_sw == 1:
        for hh in range(s1, s1 + associativity):
            if valid_cache1[hh] == addr:
                dir_cache1[hh] = 1
                break

    s12 = s1


    if valid_cache1[s1] == -1:
        #print('firsttime')
        cachemiss1=cachemiss1 + 1
        temp_list=memory_read(address)
        valid_cache1[s1] = addr
        qcache1[s1]=temp_list
        if value_sw == 1:
            dir_cache1[s1]=1

        return  qcache1[s1]
    else:
        found=False
        #print('secondtime')
        for hh in range(s1,s1+associativity):
            if valid_cache1[hh] == addr:
                found=True
                ret = qcache1[hh]
                if value_sw == 1:
                    dir_cache1[hh]=1
                dir_index=dir_cache1[hh]
                valid_index = valid_cache1[hh]
                rk = hh
                for jk in range(hh, s1+associativity - 1):
                    rk=jk
                    if valid_cache1[jk + 1] != -1:
                        dir_cache1[jk] =  dir_cache1[jk + 1]
                        valid_cache1[jk] = valid_cache1[jk + 1]
                        qcache1[jk] = qcache1[jk + 1]

                #read karna hai
                qcache1[rk ] = ret
                valid_cache1[rk ] = valid_index
                dir_cache1[rk ] = dir_index
                return ret
            elif valid_cache1[hh] == -1:
                #memory se nikal ke laana
                cachemiss1 = cachemiss1 + 1
                temp_list=memory_read(address)
                valid_cache1[hh] = addr
                if value_sw == 1:
                    dir_cache1[hh]=1
                qcache1[hh] = temp_list
                found=True
                #read karna h aur return bhi
                return temp_list
        if not found:
            done=False
            #print('kumar')
            cachemiss1 = cachemiss1 + 1
            #print("addr",valid_cache1[s1],'dirty bit',dir_cache1[s1])
            temper = cache2_read(addr,address)
            #print("addr", valid_cache1[s1], 'dirty bit', dir_cache1[s1])
            #tratocache2 = valid_cache1[s1]
            if dir_cache1[s1]==1:
                dir_cache1[s1] = 0
                #print('hemant')
                cain2 = (cache2_size // block_size) // associativity
                blonum2 = addr % cain2
                s11 = associativity * blonum2
                for hh in range(s11, s11 + associativity):
                    if valid_cache2[hh] == valid_cache1[s1]:
                        #print('bhaisahab')
                        qcache2[hh]=qcache1[s1]
                        dir_cache2[hh] = 1
                        done=True
                        break

                    elif valid_cache2[hh] == -1:
                        valid_cache2[hh]=valid_cache1[s1]
                        #print('donejjj')
                        qcache2[hh]=qcache1[s1]
                        done=True
                        dir_cache2[hh] = 1
                        break

                #print('hello')
                if not done :
                    #print('hiiiiiiiiiii')
                    if dir_cache2[s11] == 1:
                        memory_write(valid_cache2[s11], qcache2[s11])
                        dir_cache2[s11] = 0

                    for iii in range(s11, s11 + associativity - 1):
                        valid_cache2[iii] = valid_cache2[iii + 1]
                        qcache2[iii] = qcache2[iii + 1]
                        dir_cache2[iii] = dir_cache2[iii + 1]
                    qcache2[s11 + associativity - 1] = qcache1[s1]
                    dir_cache2[s11 + associativity - 1] = 1
                    #print('dhhhdhd',valid_cache1[s1])
                    valid_cache2[s11 + associativity - 1] = valid_cache1[s1]






            for iii in range(s1,s1+associativity-1):
                valid_cache1[iii]=valid_cache1[iii + 1]
                qcache1[iii]=qcache1[iii + 1]
                dir_cache1[iii]=dir_cache1[iii + 1]

            qcache1[s1+associativity-1] = temper
            dir_cache1[s1+associativity-1] = 0
            #print('returned address',addr)
            valid_cache1[s1+associativity-1] = addr
            return temper


def cache_controller(address):
    #print('address====',address)
    list_data = cache1_read(address)
    return list_data


def writein_memory():
    for count1 in range(0,(cache1_size // block_size)):
        if valid_cache1[count1] != -1:
            memory_write(valid_cache1[count1],qcache1[count1])

    for count1 in range(0,(cache2_size // block_size)):
        if valid_cache2[count1] != -1:
            memory_write(valid_cache2[count1],qcache2[count1])





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
    print('str3',str3)
    a = registers[str3] + int(str2) - count
    #print('value for loading==',a)
    a = a // 4
    #print('val hsah a',a)
    val = cache_controller(a)
    # print(a)
    rr = a % block_size
    registers[str1] = val[rr]



def sw(str1, str2, str3):
    global value_sw
    global s12
    a = registers[str3] + int(str2) - count
    a = a // 4
    # print(a)
    value_sw = 1
    yy = cache_controller(a)
    rr = a % block_size
    yy[rr] = registers[str1]
    value_sw = 0
    addr = a // block_size
    addr = block_size * addr
    for hh in range(s111, s111 + associativity):
        if valid_cache2[hh] == addr:
            dir_cache2[hh] = 1
            break

    for hh in range(s12, s12 + associativity):
        if valid_cache1[hh] == addr:
            dir_cache1[hh] = 1
            break



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
    if len(h) == 0 and len(d) == 0:
        writein_memory()
    s = h
    r = d


print()
print(' STATE OF REGISTERS IN THE END == ',registers)

print()
#print('FULL MEMORY == ',memory)
#print()
print('MEMORY USED == ',memory[0:i_count])
stalls=h_instr + 4
stalls=cycle-stalls
print('TOTAL NUMBER OF CYCLES == ',cycle)
#print(g)
print('number of instructions == ',h_instr)
print('stalls == ',stalls)
print('IPC == ',h_instr/cycle)
if cachetotal1 != 0:
    print('cache1 miss rate == ', cachemiss1 / cachetotal1)
else:
    print('cache1 miss rate == ', 0)

if cachetotal2 != 0:
    print('cache2 miss rate == ', cachemiss2 / cachetotal2)
else:
    print('cache2 miss rate == ', 0)

print('cache - 1 storage == ',qcache1)
print('cache - 2 storage == ',qcache2)
