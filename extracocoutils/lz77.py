class DistComp(object):
    def __init__(self, cod, dist, comp = 1):
        self.cod = cod
        self.dist = dist
        self.comp = comp
        
    @property
    def list(self):
        return [self.cod, self.dist, self.comp]

    def __str__(self):
        return "%s [%d, %d]" % tuple(self.list)
        
    def compara(self, outro):
        if self.comp != outro.comp:
            return outro.comp - self.comp
        else:
            return outro.dist - self.dist
        
        
def busca(entrada, i, cod = 'C'):
    opcoes = []
    tam = len(entrada)
    #j = max(max(i - 127, i-1),0)
    j = max(i - 127, 0)
    d = i
    off = 0
    
    while j < i and j < tam:
        k = j
        d = i
        if dados[j] == dados[d]:            
            l = 0
            while dados[k] == dados[d]:                
                l = l + 1
                d = d + 1
                k = k + 1
                if d == tam or l == 127 or k == tam:
                    break
            off = j - i
            #return (d-1,DistComp(cod, off, l))
            opcoes.append((d-1,DistComp(cod, off, l)))
        if k == i or k == tam:
            break
        j = j + 1        
    if len(opcoes) > 0:
        opcoes.sort(lambda a,b : a[1].compara(b[1]))
        return opcoes[0]
    else:
        return None   
    #return None
    
if __name__ == "__main__":
    import sys
    from struct import pack
    if len(sys.argv) < 2:
        print "Sintaxe: lz77.py <entrada>"
        sys.exit()
    partes = sys.argv[1].split(".")
        
    with open(".".join(partes),"rb") as arq:
        dados = bytearray(arq.read())[:65536]
    
    with open("xxx.bin", "wb") as w:
        w.write(dados)
    tam_arquivo = len(dados)

    freq = {}
    for item in dados:
        freq[item] = freq.get(item,0) + 1

    frs = freq.items()
    frs.sort(lambda a,b : a[1] - b[1])
    cod = frs[0][0]        
    saida = [tam_arquivo >> 8, tam_arquivo & 0xff, cod]

#    baite = int(dados[0])
#    saida.append(baite)
#    if int(cod) == baite:
#        saida.append(0)
#        saida.append(0)

    i = 0
    while i < tam_arquivo:
        if i > 0:
            p = busca(dados, i, cod)
        else:
            p = None
        if p:
            if p[1].comp >= 3:
                saida = saida + p[1].list
                i = p[0]
            else:
                for _ in range(p[1].comp):
                    saida.append(dados[i])
                    i = i + 1
                i = i - 1
        else:
            baite = int(dados[i])
            saida.append(baite)
            
            if int(cod) == baite:
                saida.append(0)
            
        i = i + 1

    compactado = []
    for b in saida:
        fmt = "B"
        if b < 0:
            fmt = "b"
        compactado.append(pack(fmt, b))
        
    descomp = []   

    limite = saida[0] * 256 + saida[1]
    saida.pop(0)
    saida.pop(0)    
    cc = saida.pop(0)
    m = 0
    while len(descomp) < limite:
        item = saida[m]
        if int(item) != int(cc):        
            descomp.append(item)
            m = m + 1
        else:        
            if saida[m + 1] == 0:
                descomp.append(item)
                m = m + 2
            else:
                q = len(descomp) + saida[m+1] 
                for _ in range(saida[m+2]):
                    descomp.append(descomp[q])
                    q = q + 1
                m = m + 3

    print "%02.2f %%" % ((len(compactado) + 66) * 100.0 / (1.0 * tam_arquivo), )
    

    
    with open(".".join(partes + ["lz"]),"wb") as ot:        
        ot.write(bytearray(compactado))
    
    with open(".".join(partes[:-1] + ['unc', partes[-1]]),"wb") as out:
        out.write(bytearray(descomp))