from compressao import *
            
with open("snd_src.raw", "rb") as arq:
    dados=bytearray(arq.read())[0:5000]

contar = contagem(dados)
ll = contar.items()
ls = qsort(ll, lambda p,q: q[1] - p[1])
ns = 5
d2 = dados[:]
lw = qsort(redutor_freq(ls, d2, ns), lambda p,q: p[0] - q[0])
lq = [a[0] for a in lw]

bw = [h & 0xFC for h in d2]
for i in xrange(len(bw)):
    if bw[i] <= 0x2F: bw[i] = 0x2C
    elif 0xC0 <= bw[i] < 0xD0:  bw[i] = 0xC4
    elif bw[i] >= 0xD3: bw[i] = 0xD0
d2 = bytearray(bw)    
q = qsort(contagem(d2).items(), lambda a,b: a[1] - b[1])

mdr = gerar_arvore_huffman(q)

with open("snd_cut.raw","wb") as a3:
    a3.write(bytearray([len(lq)]))
    a3.write(bytearray(lq))
    a3.write(d2)
    
with open("snd_compressed.raw","wb") as a4:
    a4.write(bytearray(comprimir(mdr, d2)))    

print "; The following code can be compiled using a 6809 Assembler, such as AS09, found at:"
print "; http://www.kingswood-consulting.co.uk/assemblers/"

gera_assembly(mdr, "$E7AD", "")
gera_arvore_array(mdr, d2)