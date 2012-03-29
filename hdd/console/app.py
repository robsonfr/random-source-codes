import os
import sys
import os.path
import re
import md5
import datetime
from win32file import GetFileAttributes as gfa
from hddquery.models import *

# { x : p.__getattribute__(x) for x in dir(p) if type(app.Arquivo.__dict__.get(x,"")) == property}

class HD(object):
    pass

def get_extensao(nome):
    if "." in nome: return re.split(r"\.", nome)[-1]
    else: return ""
    
class Arquivo(object):
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
        Arquivo.extensoes[self.extensao] = Arquivo.extensoes.get(self.extensao,0) + 1
    
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
    
    def obter_arquivos(self, base='/', filtro = []):
        retorno = []
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
                            retorno = retorno + self.obter_arquivos(base + item + "/", filtro)
                        else:
                            if os.path.isfile(nome_completo) and (len(filtro) == 0 or get_extensao(item) in filtro):
                                a = Arquivo(ender,item)
                                print nome_completo
                                retorno.append(a)
        return retorno
                

def main():
    f = TipoArquivo.todas_extensoes()
    for item in Particao("I:").obter_arquivos(filtro=f):
        pass
    extensoes = Arquivo.extensoes.items()
    extensoes.sort(lambda p,q: q[1] - p[1])
    for item in extensoes:
        print "%s  (%7d)" % item

                
if __name__ == "__main__":
    main()