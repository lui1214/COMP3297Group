from django.views.generic import TemplateView
from orders.models import Item

class PbiView(TemplateView):

	template_name = "pbi_list.html"

	def get_context_data(self, **kwargs):
		item = self.kwargs['item']

		context = super().get_context_data(**kwargs)
		context['pbi_list'] = Item.objects.all()
		return context