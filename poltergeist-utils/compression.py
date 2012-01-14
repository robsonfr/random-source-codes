"""Compression functions, such as RLE and Huffman, 
as well as a Quicksort sorting algorithm
"""

def qsort(lista, fncComp):
    """A lame (and recursive) implementation of the quicksort sorting algorithm created by C. A. R. Hoare
       lista : a list or a tuple, or anything iterable
       
       fncComp : function (can be lambda) that is used for comparing the list items and returns  -1,0 or 1 
                 whether the item is lower, the same or greater than the other
       returns : a new list, sorted
    """         
    l = len(lista)
    if l<=1: return lista
    pivot = l / 2
    p = lista[pivot]
    return qsort([i for i in lista if fncComp(i,p) < 0], fncComp) + [p] + qsort([j for j in lista if fncComp(j,p) >= 0 and j != p], fncComp)

class arvore_huffman:
    """ A Huffman tree, which items in its leaves and the sums in its branches
    """
    
    def __init__(self, v1):
        self.valor = v1
        self.esquerda = None
        self.direita = None
        self.pai = None
  
    def __str__(self):
        return "[%04X %04d]" % self.valor  

def insere_arvore(valor1, valor2):
    """ Inserts two values in the Huffman tree:
        1. a new summing node is created, which the item field equals to 0xFFFF
        and the frequency field as the sum of the frequencies (first index) of each value
        
        valor1 e valor2 : values to be inserted in the tree;
                          must be instances of arvore_huffman
        returns : the new node with the junction of such values
    """
    novo = arvore_huffman((0xFFFF, valor1.valor[1] + valor2.valor[1]))
    if valor1.valor[1] < valor2.valor[1]:
        novo.esquerda = valor1
        novo.direita = valor2
    else:
        novo.esquerda = valor2
        novo.direita = valor1
    valor1.pai = novo
    valor2.pai = novo
    return novo
    
def gerar_arvore_huffman(lista):
    """ Generates the Huffman tree according to a two-tuple list provided
        The first element of the tuple is the value and the second is
		the frequency which such value was found in the data to be compressed
        
		lista : a list of tuples
		
        returns : tree's root
    """    
    l2 = [arvore_huffman(l) for l in lista]
    while len(l2) > 1:
        item = insere_arvore(l2[0], l2[1])
        l2 = [item] + l2[2:]
        if len(l2) > 1: l2 = qsort(l2, lambda p,q : p.valor[1] - q.valor[1])
    return l2[0]
    

def redutor_freq(lista, ddd, num_itens):
    """ Attempts to decrease the frequency of items in a byte list
        
        lista : a list of tuples as (value, frequency)
        
        ddd : a byte list to have its frequency decreased
        
        num_itens : the desired number of distinct items in the final byte list
        
        returns : a list of bytes with the decreased frequency
    """
    l2 = lista
    k = 0
    while len(l2) > num_itens:
        redutor = len(l2) / num_itens
        if redutor < 1: break
        v = l2[k][0]
        for i in xrange(len(ddd)):
            if abs(ddd[i] - v) <= redutor: ddd[i] = v
        l2 = [w for w in l2 if w[0] == v or abs(w[0] - v) > redutor]
        l2 = qsort(l2, lambda p,q: q[1] - p[1])
        k = k + 1
        if k == len(l2): break
    return l2
    
def rle(origem):
    """ RLE (Run length encoding) compression that works with source data values lower than 16 (0x10) only
		
		origem : the source byte list
		
        retorna : a new byte list as follows:
                  byte < 16 : the byte itself
                  byte >= 0x8X : byte X being repeated (byte - 0x80) >> 4 + 2 times
                                 i.e. 0x95 means byte 0x05 repeated 3 times
    """
    ret = []
    i = 1
    l = len(origem)
    ant = origem[0]
    r = 1
    while i < l:
        o = origem[i]
        if o == ant:
            r = r + 1
            if r == 10:
                ret.append(0xF0 + ant)
                r = 1
        else:
            if r > 1:
                ret.append(0x80 + ant + ((r-2) << 4))
            else:
                ret.append(ant)
            r = 1
            ant = o
        i = i + 1    
    if r > 1: ret.append(0x80 + ant + ((r-2) << 4))
    else: ret.append(ant)
    return bytearray(ret)


def contagem(d):
    """ Creates a dictionary with the frequency of each byte of the provided list
		d : the list
		
		returns : the dictionary with the frequencies
    """
    cc = {}
    for i in d:
        if i in cc.keys():
            cc[i] = cc[i] + 1
        else: cc[i] = 1
    return cc

def bits_to_byte(b):
    """ Converts a bit list in an integer value.
		Although it expects bytes, theoretically it could generate integers and longs as well
		b : a list of single digit numbers, from the most to the least significative bit 
    """    
    r,k = (0,len(b)-1)
    for j in b:
        r = r + (j << k)
        k = k - 1
    return r

def ordena_arvore(item1, item2):
    """ Says whether item1 is before or after item2, according to the following criterion:        
        - the number of bits in the Huffman string
        - if the number of bits is the same, the string's nummeric value
		
		item1, item2 : the items to be ordered
		
		returns : -1 if item1 is before item2, 1 if it is the opposite, 0 if item1 == item2
		
    """
    if len(item1[1]) != len(item2[1]): 
		return len(item1[1]) - len(item2[1])
    else: 
        return( bits_to_byte(item1[1]) - bits_to_byte(item2[1]))   
 
 
def imprime_arvore_nr(raiz):
    """ Prints the Huffman tree from the provided root, using a non-recursive method
	    
		raiz : the root node
	
    """    
    nos_a_percorrer = [[raiz,[]]]
    qt_bits = 0
    ret = []
    while len(nos_a_percorrer) > 0:
        i = nos_a_percorrer.pop(0)
        if i[0].esquerda is not None: nos_a_percorrer.append([i[0].esquerda,['1']+i[1]])
        if i[0].direita is not None: nos_a_percorrer.append([i[0].direita,['0']+i[1]])
        if i[0].esquerda is None and i[0].direita is None: 
            i[1].reverse()
            bb = i[0].valor[1] * len(i[1])
            qt_bits = qt_bits + bb
            ret.append([i[0].valor[0], mascara(i[1])])
            
    print qt_bits / 8.0
    r2 = qsort(ret, ordena_arvore)
    for k, l in r2:
        print "%02X %s" % (k, "".join([str(j) for j in l]))
    return r2
        
def mascara(lista_bits):
    """ Creates a list of integer values from a bit list which each bit is a string.
        Used by gera_cod_huffman
		
		lista_bits : a bit list such as [ '0', '0', '1', '0', '1', '0', '1', '0' ]
		
		returns : a bit list such as [ 0, 0, 1, 0, 1, 0, 1, 0 ]
    """    
    return [int(i) for i in lista_bits]
    
def gera_cod_huffman(raiz):
    """ Generates the Huffman code of the items from the root node
        using a non-recursive, queue-based algorithm
        
        returns : a dictionary with the value from the tree and a bit list from the tree's processing
		
    """
    nos_a_percorrer = [[raiz,[]]]
    ret = {}
    while len(nos_a_percorrer) > 0:
        i = nos_a_percorrer.pop(0)
        if i[0].esquerda is not None: nos_a_percorrer.append([i[0].esquerda,['1']+i[1]])
        if i[0].direita is not None: nos_a_percorrer.append([i[0].direita,['0']+i[1]])
        if i[0].esquerda is None and i[0].direita is None: 
            i[1].reverse()
            ret[i[0].valor[0]] = mascara(i[1])
    return ret    
    

    
def comprimir(arvore, dados):
    """ Creates a byte list (actaully a continuation) which is, in fact, a bit string of the
        Huffman codes (from the specified tree) of the values found in dados
		
		arvore : the Huffman tree
		
		dados : the data to be compressed
		
		returns : the byte list (continuation)
    """    
    codigos = gera_cod_huffman(arvore)
    bits = []
    for item in dados:
        ch = codigos[item]
        bits = bits + list(ch)
        if len(bits) >= 8:
            yield bits_to_byte(bits[0:8])
            bits = bits[8:]
    if len(bits) > 0: 
        k = bits
        for u in xrange(8-len(bits)): k.append(0)
        yield bits_to_byte(k)

def prox_bit(d):
    for baite in d:
        bt = baite
        for k in xrange(8):
            if bt & 0x80 !=0 : yield 1
            else: yield 0
            bt = (bt << 1) & 0xFF
        
        
def descomprimir(arvore, dados_comp, num_bytes=0):
    """ Decompress the data according to the provided Huffman tree
		
		arvore : the Huffman tree
		
		dados_comp : the data to be decompressed
		
		num_bytes : the maximum of bytes to be generated.
    """
    bits = prox_bit(dados_comp)
    j = 0
    while num_bytes == 0 or j < num_bytes:
        inicio = arvore
        while inicio is not None:
            try:
                b = bits.next()
                if b == 1 and inicio.esquerda is not None:
                    if inicio.esquerda.esquerda is None:
                        j = j + 1
                        yield inicio.esquerda.valor[0]
                        break
                    else:
                        inicio = inicio.esquerda
                elif b == 0 and inicio.direita is not None:
                    if inicio.direita.esquerda is None:
                        j = j + 1
                        yield inicio.direita.valor[0]
                        break
                    else:
                        inicio = inicio.direita                    
            except:
                return
    
    
    
def compressao_completa(dados, impr_arvore = False):
    """ Performs all the data compression procedure, from the byte counting
        up to the compression itself, including the Huffman tree generation
    """
    cc = contagem(dados).items()
    cc = qsort(cc, lambda i,j : i[1] - j[1]) 
    ah = gerar_arvore_huffman(cc)
    if impr_arvore: imprime_arvore_nr(ah)
    return comprimir(ah,dados)

def val_asm(item):
    print ("  %-20s" % ""), "LDA    #$%02X" % item.valor[0]
    print ("  %-20s" % ""), "JMP    ARMAZENA"
    
def repr_bits(item):
    r = [int(i) for i in item]
    r.reverse()
    return "%d" % bits_to_byte(r)
    #return "".join(r)
    
def gera_assembly(arvore,origem='$E000',longos="L"):
    """ Creates the Assembly code (MC6809) of the layered tree provided (generated by imprime_arvore_nr)
		
		arvore : the Huffman tree
	
		origem : where the machine code will be
		
		longos : for the branching operations. "L" stands for "long" branching operations. In most cases, it is required.
	
        Registers used: A,B,X,Y,U
        B : Auxiliary
        Y : Number of expected uncompressed bytes
        U : Target address
        X : Source data address
    """
    print "                       org %s" % origem
    print "DECOMP_HUFFMAN:        PSHS    A,B,X,Y,U" 
    print "                       LDB     #8"
    print "                       STB     $2100"
    print "                       LDB     ,X+"
    print "                       JMP     INICIO"
    print "PROX_BIT:              LSLB"
    print "                       PSHS    CC"
    print "                       DEC     $2100"
    print "                       BNE     S_P_B"
    print "                       LDB     #8"
    print "                       STB     $2100"
    print "                       LDB       ,X+"
    print "S_P_B:                 PULS    CC"
    print "                       RTS"
    print "ARMAZENA:              STA       ,U+"
    print "                       LEAY    -1,Y"
    print "                       BNE      INICIO"
    print "                       PULS   U,Y,X,B,A"
    print "                       RTS"
    print "INICIO:"
    
    nos_a_percorrer = [[arvore,[]]]
    leaf = lambda j : j.esquerda is None and j.direita is None
    while len(nos_a_percorrer) > 0:
        atual = nos_a_percorrer.pop(0)
        if len(atual[1]) > 0: 
            print "R_%s:" % repr_bits(atual[1])
        print ("  %-20s" % ""), "JSR    PROX_BIT"
        esq = atual[0].esquerda
        dre = atual[0].direita
        rbe = repr_bits(['1'] + atual[1])
        rbd = repr_bits(['0'] + atual[1])

        if leaf(esq):
            if leaf(dre):    
                print ("  %-20s" % ""), "BCS    R_%s" % rbe 
                val_asm(dre)
                print "R_%s:" % rbe
                val_asm(esq)
            else:
                print ("  %-20s" % ""), longos+"BCC   R_%s" % rbd 
                val_asm(esq)                
        elif leaf(dre):
            print ("  %-20s" % ""), longos+"BCS   R_%s" % rbe 
            val_asm(dre)
        else:
            print ("  %-20s" % ""), longos+"BCS   R_%s" % rbe
            print ("  %-20s" % ""), longos+"BRA   R_%s" % rbd

        if not leaf(esq): nos_a_percorrer.append([esq,['1']+atual[1]])
        if not leaf(dre): nos_a_percorrer.append([dre,['0']+atual[1]])

def gera_arvore_array(arvore, dados):
    """Prints the Huffman tree
		
		arvore : the Huffman tree itself
		
		dados : the data which the Huffman tree will be used
	
    """
    valores = [i for i in xrange(256) if not i in contagem(dados).keys()]
    #resultado = valores[0:4]    
    resultado = []
    print ";" , resultado
    leaf = lambda j : j.esquerda is None and j.direita is None
    nos_a_percorrer = [arvore]
    p = len(resultado)
    while len(nos_a_percorrer) > 0:
        atual = nos_a_percorrer.pop(0)
        esq = atual.esquerda
        dre = atual.direita        
        q = len(resultado)
        p = p + 3
        if leaf(esq) and leaf(dre): 
            resultado = resultado + [0, esq.valor[0], dre.valor[0]]
        elif leaf(esq):
            resultado = resultado + [1, esq.valor[0],p - q]
        elif leaf(dre):
            resultado = resultado + [2, p - q, dre.valor[0]]
        else:
            p = p + 3
            resultado = resultado + [3, p - 3 - q, p - q]
        if not leaf(esq): nos_a_percorrer.append(esq)
        if not leaf(dre): nos_a_percorrer.append(dre)
    print ";" , " ".join([("%02X" % v) for v in resultado])        