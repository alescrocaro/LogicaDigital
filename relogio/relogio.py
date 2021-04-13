from time import sleep


def p_nand_2(a, b):
    return int(not(a and b))

def p_nand_3(a, b, c):
    return int(not(a and b and c))

def p_not(a):
    return int(not(a))

def ff_jk(ck=1, j=1, k=1, qa=0, test=0):
    qa1, qa2 = qa, p_not(qa)
    qf1, qf2 = qa1, qa2
    while True:
        s1 = p_nand_3(j, ck, qa2)
        s2 = p_nand_3(k, ck, qa1)
        qf1 = p_nand_2(s1, qf2)
        qf2 = p_nand_2(s2, qf1)
        if qf1 != qf2:
            return qf1
        elif test:
            print('Atualização:', qf1, qf2)


###############################################################################

def segmentos_7(v):
    s = lambda desenho, existe: desenho if int(existe) else ' '
    inter = ('', '.', '', '.', '', ' ', '', '')
    l1, l2, l3 = '', '', ''
    v = [nb[v[i:i+4]] for i in range(0, len(v), 4)]
    for i, c in enumerate((0, 0, 1, 0, 1, 0, 1, 0)):
        l1 += '{} {} '.format(' ' * c, s('_', v[i][0]))
        l2 += '{}{}{}'.format(s('|', v[i][5]), s('_', v[i][6]), s('|', v[i][1]))
        l2 += inter[i]
        l3 += '{}{}{}'.format(s('|', v[i][4]), s('_', v[i][3]), s('|', v[i][2]))
        l3 += inter[i]
    return '{}\n{}\n{}'.format(l1, l2, l3)

# Acionamento de cada segmento
nb = {
    '0000': '1111110', # 0
    '0001': '0110000', # 1
    '0010': '1101101', # 2
    '0011': '1111001', # 3
    '0100': '0110011', # 4
    '0101': '1011011', # 5
    '0110': '0011111', # 6
    '0111': '1110000', # 7
    '1000': '1111111', # 8
    '1001': '1110011', # 9
    '1010': '1110111', # A
    '1011': '1100111', # P
    '1100': '1010101', # M
    '1111': '0000000', # 24h
}

vet = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1111']

def relogio(n, ap):
    str = ''
    #horas
    horas = n//3600
    hd = horas//10
    hu = horas%10
    if hd == 0 & hu == 0:
        str = str + ''.join(vet[1])
        str = str + ''.join(vet[2])
    else:
        str = str + ''.join(vet[hd])
        str = str + ''.join(vet[hu])
    #minutos
    minutos = (n%3600)//60
    md = minutos//10
    mu = minutos%10
    str = str + ''.join(vet[md])
    str = str + ''.join(vet[mu])
    #segundos
    segundos = (n%3600)%60
    sd = segundos//10
    su = segundos%10
    str = str + ''.join(vet[sd])
    str = str + ''.join(vet[su])
    #ampm
    if ap == 0:
        str = str + ''.join(vet[10])
    else:
        str = str + ''.join(vet[11])
    str = str + ''.join(vet[12])
    print(segmentos_7(v=str))

def s_to_bi(n):# Segundos para binário em 16 bits
    str = ''
    i = n_ff-1
    for _ in range(0, n_ff):
        if n-(2**i) >= 0:
            str = str + ''.join('1')
            n = n-(2**i)
        else:
            str = str + ''.join('0')
        i -= 1
    return str

###############################################################################

#SEGUNDOS
n_ff = 16  # Numero de flipflops
qf, qa = [0] * (n_ff + 1), [0] * (n_ff + 1)

#preset com hora real
import datetime

now = datetime.datetime.now()
numb = 0
numb += ((now.hour-3)%12)*(3600)
numb += now.minute*60
numb += now.second
ampm = 0

if now.hour >= 12:
    ampm = 1

pr = s_to_bi(n=numb)  # setando valor de "preset" para hora

for i, p in enumerate(pr[-1::-1]):
    qf[i] = qa[i] = int(p)

cl = '1010100011000000' # setando valor de "clear"
ck = int(pr, 2) * 2 #clock


# funcionamento ...
while True:
    try:
        if cl == ''.join([str(q) for q in qf[-2::-1]]):
            for i in range(len(qf)):
                qf[i] = qa[i] = 0
            ck = 0
            ampm = not(ampm)

        num=0

        # Retorna valor binário para segundos
        for i in range(0, (n_ff + 1)):
            num += (qf[i] * (2 ** i))

        relogio(n=num, ap = ampm)

        #jk
        sleep(0.5) # 1/2 segundo em baixa e 1/2 segundo em alta
        qa[0] = ff_jk(ck=(ck % 2), j=1, k=1, qa=qa[0])

        #roda todos os ffjk uma vez
        for i in range(1, (n_ff + 1)):
            if (ck + 1) % (2 ** i) == 0:
                qa[i] = ff_jk(ck=qf[i - 1], j=1, k=1, qa=qa[i])
                qf[i - 1] = qa[i - 1]

        ck += 1 #acrescenta o clock
    except KeyboardInterrupt:
        break

###############################################################################
