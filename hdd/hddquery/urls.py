from django.conf.urls.defaults import *
from django.views.generic import ListView, CreateView
from hddquery.models import HD
from hddquery.views import IncluirArquivoView, ListaJSON

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('hddquery.views',
    # Examples:
    # url(r'^$', 'hdd.views.home', name='home'),
    url(r'^hdds/$', ListView.as_view(model = HD, context_object_name="lista_hds")), 
    url(r'^lista.json$', ListaJSON.as_view(model = HD, context_object_name="lista_hds")), 
    url(r'^novo/$', CreateView.as_view(model = HD, template_name="hd_new.html", success_url="/hdd/hdds/")),
    url(r'^arquivo/novo/$', IncluirArquivoView.as_view()),
)
