from django.views.generic import TemplateView
from pbi.models import Item
from pbi.forms import ItemForm

def newPBI(request):
	template_name = 'pbi_new.html'
	form = ItemForm(request.POST or None)
	
	if form.is_valid():
		obj = Item.objects.create(
			order = form.cleaned_data.get('order'),
			name = form.cleaned_data.get('name'),
			description = form.cleaned_data.get('description'),
			original_sprint_size = form.cleaned_data.get('original_sprint_size'),
			remaining_sprint_size = form.cleaned_data.get('remaining_sprint_size'),
			estimate_of_story_point = form.cleaned_data.get('estimate_of_story_point'),
			status = form.cleaned_data.get('status')
		)
		return HttpResponse('OK')
	return render(request, template_name, context={'form':form})
		
		
class PbiView(TemplateView):
      template_name = 'pbi_list.html'

      def get_context_data(self, **kwargs):
            ctx = super(PbiView, self).get_context_data(**kwargs)
            ctx['header'] = ['Order', 'Feature Name', 'Description', 'Original Sprint Size','Remaining Sprint Size', 'Estimate of Story Point', 'Status']
            ctx['rows'] = Item.objects.all()
            return ctx