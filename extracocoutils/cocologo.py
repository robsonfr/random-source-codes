def bits(v):
    return (((v >> 4) != 0) << 1) + ((v & 0x0f) != 0)

with open("cocotla_logo_2.bmp","rb") as entrada:
    entrada.seek(0x4A)
    dados = bytearray(entrada.read())
    
cores = [0, 2, 3, 0, 4, 0, 0, 0]
resposta = [0] * 512    
for j in range(16):
    for i in range(32):
        c = int(dados[i + j * 64])
        d = int(dados[i + j * 64 + 32])
        if c >> 4 != 0:
            cor = c >> 4
        elif c & 0x07 != 0:
            cor = c & 0x07
        elif d >> 4 != 0:
            cor = d >> 4
        else:
            cor = d & 0x07
            
        resposta[i + j * 32] = (bits(c) << 2)  + (bits(d)) + 128 + (cores[cor] << 4)
        
        
        
for baite in resposta:
    print "    db 0x%02x" % baite
    