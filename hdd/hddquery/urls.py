from django.conf.urls.defaults import *
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from hddquery.models import HD, Particao
from hddquery.views import IncluirArquivoView, ListaHibrida, ParticoesView,\
    ParticoesListaHibrida, ArquivosListaHibrida
from django.views.generic.list import ListView
from hddquery.models import HD
from django.views.decorators.csrf import csrf_exempt

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('hddquery.views',
    # Examples:
    # url(r'^$', 'hdd.views.home', name='home'),
    url(r'^$', ListView.as_view(model = HD, context_object_name="lista_hds")), 
    url(r'^lista\.(?P<ext>.+)$', ListaHibrida.as_view(model = HD, context_object_name="lista_hds")), 
    url(r'^novo/$', CreateView.as_view(model = HD, template_name="hd_new.html", success_url="/hdd/")),
    url(r'^arquivo/novo/$', csrf_exempt(IncluirArquivoView.as_view())),
    url(r'^(?P<pk>\d+)/editar/$', UpdateView.as_view(model = HD, template_name="hd_new.html", success_url = "/hdd/")),
    url(r'^(?P<hd_id>\d+)/particoes/$', ParticoesView.as_view()),
    url(r'^(?P<hd_id>\d+)/particoes\.(?P<ext>.+)$', ParticoesListaHibrida.as_view()),
    url(r'^(?P<hd_id>\d+)/particao/(?P<particao_id>\d+)/arquivos\.(?P<ext>.+)$', ArquivosListaHibrida.as_view()),
    url(r'^(?P<hd_id>\d+)/particao/(?P<pk>\d+)/editar/$', UpdateView.as_view(model = Particao, template_name="particao_new.html", success_url = "/hdd/")),
    url(r'^(?P<hd_id>\d+)/particao/(?P<pk>\d+)/arquivos\.(?P<ext>.+)$', UpdateView.as_view(model = Particao, template_name="particao_new.html", success_url = "/hdd/")),
    url(r'^(?P<hd_id>\d+)/particao/nova/$', CreateView.as_view(model = Particao, template_name="particao_new.html", success_url="/hdd/")),
)
