import os.path
import re
import md5
import datetime
from hddquery.models import TipoArquivo
from win32file import GetFileAttributes as gfa

# { x : p.__getattribute__(x) for x in dir(p) if type(app.Arquivo.__dict__.get(x,"")) == property}

class HD(object):
    pass

def metodo_post(url, **params):
    from urllib import urlencode
    from urllib2 import urlopen
    from json import load
    if len(params) > 0:   
        x = urlopen(url, urlencode(params))
    else:
        x=urlopen(url)
    return load(x)
    

def get_extensao(nome):
    if "." in nome: return re.split(r"\.", nome)[-1]
    else: return ""
    
class FSArquivo(object):
    extensoes = {}
    def __init__(self, caminho, arquivo, filtro=[]):
        self._caminho = caminho
        self._arquivo = arquivo
        h = md5.md5()
        self._tamanho = 0
        self._data_hora = datetime.datetime.fromtimestamp(os.path.getmtime(self.nome_completo))
        with open(self.nome_completo, "rb") as arq:
            k = arq.read(16384)
            while(len(k) > 0):
                h.update(k)
                self._tamanho = self._tamanho + len(k)
                k = arq.read(16384)
        self._hash = h.hexdigest()
        FSArquivo.extensoes[self.extensao] = FSArquivo.extensoes.get(self.extensao,0) + 1
    
    @property
    def caminho(self):
        return self._caminho
    
    @property
    def arquivo(self):
        return self._arquivo
    
    @property
    def nome_completo(self):
        s = self._caminho
        if s[-1] != "/" and s[-1] != "\\":
            s = s + "/"
        return s + self._arquivo
    
    @property
    def hash(self):
        return self._hash
    
    @property
    def extensao(self):        
        return get_extensao(self._arquivo)
    
    @property
    def tamanho(self):
        return self._tamanho
    
    @property
    def data_hora(self):
        return self._data_hora
    
    @property
    def dicionario(self):
        return {'nome': self.arquivo, 'caminho_completo' : self.caminho, 'tamanho' : self.tamanho, 'data_hora' : self.data_hora, 'hash' : self.hash}
    
    def __str__(self):
        return "[%s] %s (%s)" % (self.extensao, self._arquivo, self.hash)

def atr_val(a):
    return reduce(lambda i,j : i and j, map(lambda p : a & p == 0, [2,4,65536]))
        
class Particao(object):
    def __init__(self, endereco_part = 'C:'):
        self._endereco_part = endereco_part
    
    @property    
    def endereco_part(self):
        return self._endereco_part
    
    def endereco(self, base="/"):
        return self._endereco_part + base
    
    def obter_arquivos(self, base=u'/', filtro = []):
#        retorno = []
        ender = self.endereco(base)
        try:
            lista = os.listdir(ender)
        except:
            lista = []
        for item in lista:
            if not item.startswith("."):
                nome_completo = ender + item
                if item[0] != '$':
                    if atr_val(gfa(nome_completo)):
                        if os.path.isdir(nome_completo):
#                            retorno = retorno + self.obter_arquivos(base + item + "/", filtro)
                            for i in self.obter_arquivos(base + item + "/", filtro):
                                yield i
                        else:
                            if os.path.isfile(nome_completo) and (len(filtro) == 0 or get_extensao(item) in filtro):
                                a = FSArquivo(ender,item)
#                                print nome_completo
                                yield a
#                                retorno.append(a)
#        return retorno
                

def main():
    f = TipoArquivo.todas_extensoes()
    print("Informe a letra da unidade com os dois pontos (:)")
    letra = unicode(raw_input())
    print("Escolha o HD/Pendrive na relacao abaixo:")
    for item in [(hd[u'pk'], str(hd[u'fields'][u'nome'])) for hd in metodo_post("http://localhost:8000/hdd/lista.json")]:
        print("[%02d]     %s\n" % item)
    hd_id = int(raw_input())
    lista_particoes=[]
    for part in metodo_post("http://localhost:8000/hdd/" + str(hd_id) + "/particoes.json"):
        lista_particoes.append((part[u'pk'], part[u'fields'][u'nome'].encode("UTF-8").decode("ISO-8859-1"))) 
    if len(lista_particoes) == 0:
        print("Erro! O HD nao tem particoes!")
        return
    elif len(lista_particoes) > 1:
        print("Escolha a particao:")
        for p in lista_particoes:
            print("[%02d]      %s" % p)
        part_id = int(raw_input())        
    else:
        part_id = lista_particoes[0][0]
    qt = 0
    for item in Particao(letra.upper()).obter_arquivos(filtro=f):
        d = item.dicionario
        d['particao'] = part_id
        d['caminho_completo'] = d['caminho_completo'][2:].encode("UTF-8")
        d['nome'] = d['nome'].encode("UTF-8")
        qt = qt + 1        
        r = metodo_post("http://localhost:8000/hdd/arquivo/novo/", **d)
#        resposta = 
    print qt
                
if __name__ == "__main__":
    main()