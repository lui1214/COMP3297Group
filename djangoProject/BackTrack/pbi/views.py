from django.views.generic import TemplateView
from pbi.models import Item

class PbiView(TemplateView):
      template_name = 'pbi_list.html'

      def get_context_data(self, **kwargs):
            ctx = super(PbiView, self).get_context_data(**kwargs)
            ctx['header'] = ['Order', 'Feature Name', 'Description', 'Original Sprint Size','Remaining Sprint Size', 'Estimate of Story Point', 'Status']
            ctx['rows'] = Item.objects.all()
            return ctx