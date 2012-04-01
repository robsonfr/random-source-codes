# Create your views here.

from django.views.generic.edit import ProcessFormView
from django.views.generic import ListView
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.core import serializers
from hddquery.models import Arquivo, HD, Particao

class IncluirArquivoView(ProcessFormView):
    
    def post(self, request, *args, **kwargs):
        campos = (f.attname for f in Arquivo._meta.fields)
        p = {x : y for x,y in request.POST.items() if x in campos}
        a = Arquivo.objects.create(**p)
        l = Arquivo.objects.filter(id=a.id)
        print(request.REQUEST['particao_id'])
        return Serializador().render_to_response({'object_list' : l}, ('json','application/json'))
        
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