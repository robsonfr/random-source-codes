from django.db import models
from django.forms import ModelForm
import re
from django.db.utils import DEFAULT_DB_ALIAS

# Create your models here.

class HD(models.Model):
    """Um... HD, oras!
    """
    numero_serial = models.CharField(max_length=32)
    nome = models.CharField(max_length=40, unique=True)
    tamanho = models.CharField(max_length = 20)
    dh_registro = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return "%s [%s]"  % (self.nome, self.tamanho)
    
class Particao(models.Model):
    """Uma particao dentro do HD
    """
    nome = models.CharField(max_length = 255)
    tipo = models.CharField(max_length = 20)
    tamanho = models.BigIntegerField()
    dh_registro = models.DateTimeField(auto_now = True)
    hd = models.ForeignKey(HD)
    
    class Meta:
        verbose_name_plural = "particoes"
    
    def _get_tamanho_formatado(self):
        if self.tamanho < 1024:
            return "%d bytes" % (self.tamanho)
        elif 1024 <= self.tamanho < 1048576:
            return "%d KBytes" % int(self.tamanho / 1024)
        elif 1048576 <= self.tamanho < (1048576 * 1024):
            return "%d MBytes" % int(self.tamanho / 1048576)
        else:
            return "%d GBytes" % int(self.tamanho / 1048576 / 1024)
    
    tamanho_formatado = property(_get_tamanho_formatado)
    
    def __unicode__(self):
        return "%s [%s]" % (self.nome, self.tamanho_formatado)

class TipoArquivo(models.Model):
    """Tipos de arquivos
    suportados por este projeto
    """
    nome = models.CharField(max_length=40)
    extensoes = models.CharField(max_length=126)
    
    class Meta:
        verbose_name_plural = "tipos arquivo"
    
    def _get_extensoes(self):
        return re.split(r"[,;]\s*", str(self.extensoes.lower()))
    
    def __unicode__(self):
        return "%s [%s]" % (self.nome, ", ".join(self._get_extensoes()))
    
    lista_extensoes = property(_get_extensoes)
    
    @staticmethod
    def todas_extensoes():
        return reduce(lambda p,q : p+q, map(lambda i : i.lista_extensoes, TipoArquivo.objects.all()))
    
    @staticmethod
    def por_extensao(extensao):
        for tipo in TipoArquivo.objects.all():
            if extensao.lower() in tipo.lista_extensoes: 
                return tipo 
        return None
    
class Arquivo(models.Model):
    """Arquivos de um HD
    Uma busca normalmente retorna uma lista
    de Arquivos
    """
    
    nome = models.CharField(max_length=255)
    caminho_completo = models.CharField(max_length=1024)
    hash = models.CharField(max_length=64)
    data_hora = models.DateTimeField()
    tamanho = models.BigIntegerField()
    dh_registro = models.DateTimeField(auto_now = True)
    tipo = models.ForeignKey(TipoArquivo)
    particao = models.ForeignKey(Particao)
    
    def save(self, *args, **kwargs):
        if self.tipo is None and "." in self.nome:
            import re            
            self.tipo = TipoArquivo.por_extensao(re.split(r"\.", self.nome)[-1])
        super(Arquivo, self).save(*args, **kwargs)
        
    
class HDForm(ModelForm):
    class Meta:
        model = HD
        
class ParticaoForm(ModelForm):
    class Meta:
        model = Particao
        
class TipoArquivoForm(ModelForm):
    class Meta:
        model = TipoArquivo
    