# Create your views here.

from django.views.generic.edit import ProcessFormView
from django.views.generic import ListView
from django.http import HttpResponse
from django.core import serializers

class IncluirArquivoView(ProcessFormView):
    
    def post(self, request, *args, **kwargs):
        print(request.REQUEST['particao_id'])
        return HttpResponse("Teste", mimetype = "text/plain")
        
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
        
class SerializadorJSON(object):
    def render_to_response(self, context):
        return self.get_json_response(self.converter_para_json(context))
        
    def get_json_response(self, conteudo, **httpresponse_kwargs):
        return HttpResponse(conteudo, content_type='application/json', **httpresponse_kwargs)
   
    def converter_para_json(self, context):        
        return serializers.serialize("json", context['object_list'])
   
class ListaJSON(SerializadorJSON, ListView):
    pass