# Create your views here.

from django.views.generic.edit import ProcessFormView
from django.views.generic import ListView
from django.http import HttpResponse, Http404, HttpResponseBadRequest,\
    HttpResponseServerError
from django.core import serializers
from hddquery.models import Arquivo, HD, Particao, TipoArquivo

class TipoArquivoTodosView(ProcessFormView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(", ".join(TipoArquivo.todas_extensoes()), mimetype="text/plain")

    def post(self, request, *args, **kwargs):
        return self.get(request)

class IncluirArquivoView(ProcessFormView):
    
    def post(self, request, *args, **kwargs):
        from datetime import datetime
        p = request.POST
        a=Arquivo()
        a.data_hora = datetime.strptime(p.get('data_hora',''),'%Y-%m-%d %H:%M:%S')
        a.tamanho = int(p['tamanho'])
        a.particao = Particao.objects.get(id=int(p['particao']))
        a.nome = unicode(p['nome'])
        a.caminho_completo = unicode(p['caminho_completo'])
        a.hash = p['hash']
        try:
            a.save()
            l = Arquivo.objects.filter(id=a.id)
            return Serializador().render_to_response({'object_list' : l}, ('json','application/json'))
        except Exception as e:
            print e
            return HttpResponseServerError(a.nome)
        #
        
    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest()

tipos = {"json" : "application/json", "xml" : "text/xml"}

class ParticoesView(ListView):
    template_name = "particao_list.html"
    context_object_name = "lista_particoes"
    model = Particao
    
    def get_queryset(self):
        return Particao.objects.filter(hd__id = self.kwargs['hd_id'])
    
    def get_context_data(self, **kwargs):
        contexto = ListView.get_context_data(self, **kwargs)
        contexto['hd'] = HD.objects.get(id=self.kwargs['hd_id'])
        return contexto

class ArquivosView(ListView):
    template_name = "arquivo_list.html"
    context_object_name = "lista_arquivos"
    model = Arquivo
    
    def get_queryset(self):
        return Arquivo.objects.filter(particao__id = self.kwargs['particao_id'])
    
    def get_context_data(self, **kwargs):
        contexto = ListView.get_context_data(self, **kwargs)
        contexto['particao'] = Particao.objects.get(id=self.kwargs['particao_id'])
        return contexto

        
class Serializador(object):    
    
    def render_to_response(self, context, tipo_e_tipo_mime):
        return self.get_response(self.converter(context, tipo_e_tipo_mime[0]), tipo_e_tipo_mime[1])
        
    def get_response(self, conteudo, tipo_mime, **httpresponse_kwargs):
        return HttpResponse(conteudo, content_type=tipo_mime, **httpresponse_kwargs)
   
    def converter(self, context, tipo):
        return serializers.serialize(tipo, context['object_list'])   
                    
class ListaHibrida(Serializador, ListView):
    def render_to_response(self, context):
        ext = self.kwargs.get("ext","").lower()
        if tipos.has_key(ext):
            return Serializador.render_to_response(self, context, (ext, tipos[ext]))
        elif ext == "html":
            return ListView.render_to_response(self, context)
        else:
            raise Http404
        
class ParticoesListaHibrida(ParticoesView, ListaHibrida):
    pass

class ArquivosListaHibrida(ArquivosView, ListaHibrida):
    pass