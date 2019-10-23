from django.views.generic import TemplateView, UpdateView, CreateView
from pbi.models import Item
from pbi.forms import ItemForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

def index(request):
    return HttpResponse("Hello, world. You're at the index.")
	
class PbiUpdateView(UpdateView):
		model = Item
		fields = '__all__'
		template_name = 'pbi_new.html'
		pk_pbiUpdate_kwargs = 'pbiUpdate_pk'
		
		def get_object(self,queryset=None):
			snum = int(self.kwargs.get(self.pk_pbiUpdate_kwargs,None))
			obj = get_object_or_404(Item, pk=snum)
			return obj
		
class PbiCreateView(CreateView):
		model = Item
		fields = '__all__'
		template_name = 'pbi_new.html'
		
class PbiView(TemplateView):
      template_name = 'pbi_list.html'

      def get_context_data(self, **kwargs):
            ctx = super(PbiView, self).get_context_data(**kwargs)
            ctx['header'] = ['Order', 'Feature Name', 'Description', 'Original Sprint Size','Remaining Sprint Size', 'Estimate of Story Point', 'Status']
            ctx['rows'] = Item.objects.all()
            return ctx