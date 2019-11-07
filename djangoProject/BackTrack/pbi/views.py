from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView,ListView
from .models import Item,Person,Project,Task,Developer,ScrumMaster,ProductOwner,Sprint
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
from datetime import datetime
import datetime
from django.utils import timezone

def index(request):
    return HttpResponseRedirect("/pbi/viewPBI/")
	
class PbiUpdateView(UpdateView):
		model = Item
		fields = '__all__'
		template_name = 'pbi_new.html'
		pk_pbiUpdate_kwargs = 'pbiUpdate_pk'
		
		def get_object(self,queryset=None):
			snum = int(self.kwargs.get(self.pk_pbiUpdate_kwargs,None))
			obj = get_object_or_404(Item, pk=snum)
			return obj
			
class PbiDeleteView(DeleteView):
		model = Item
		template_name = 'pbi_delete.html'
		pk_pbiDelete_kwargs = 'pbiDelete_pk'
		success_url = '/pbi/viewPBI/'
		
		def get_object(self,queryset=None):
			snum = int(self.kwargs.get(self.pk_pbiDelete_kwargs,None))
			obj = get_object_or_404(Item, pk=snum)
			return obj

class PbiCreateView(CreateView):
		model = Item
		fields = '__all__'
		template_name = 'pbi_new.html'

class PbiDetailView(TemplateView):
		template_name = 'pbi_detail.html'
		
		def get_context_data(self, **kwargs):
			item = self.kwargs['item']
			
			context = super().get_context_data(**kwargs)
			context['item'] = Item.objects.get(pk=item)
			return context

class PbiView(TemplateView):
		template_name = 'pbi_list.html'

		def get_context_data(self, **kwargs):
			ctx = super(PbiView, self).get_context_data(**kwargs)
			ctx['header'] = ['Order', 'Feature Name', 'Description', 'Original Sprint Size','Remaining Sprint Size', 'Estimate of Story Point', 'Cumulative Story Point', 'Status', 'Last Modified', 'Created At', 'Action']
			ctx['rows'] = Item.objects.all().order_by('order', '-last_modified')

			x = 1
			for i in ctx['rows']:
				if (i.order != x):
					i.order = x
					i.save()
				#i.last_sorted = timezone.now()
				x+=1

			cumulative = 0
			for i in ctx['rows']:
				i.cumulative_story_point = 0

			for i in ctx['rows']:
				cumulative = cumulative + i.estimate_of_story_point
				i.cumulative_story_point = cumulative

			q = Item.objects.aggregate(itemCount=Count('order'),
				remainSS=Sum('remaining_sprint_size'),
				totalSS=Sum('original_sprint_size'),
			)
			ctx['itemCount'] = q['itemCount']
			ctx['remainSS'] = q['remainSS']
			ctx['totalSS'] = q['totalSS']
			return ctx

class PbiCurrentView(TemplateView):
		template_name = 'pbi_currentList.html'

		def get_context_data(self, **kwargs):
			ctx = super(PbiCurrentView, self).get_context_data(**kwargs)
			ctx['header'] = ['Order', 'Feature Name', 'Description', 'Original Sprint Size','Remaining Sprint Size', 'Estimate of Story Point', 'Cumulative Story Point', 'Status', 'Last Modified', 'Created At', 'Action']
			ctx['rows'] = Item.objects.all().order_by('order', '-last_modified')

			cumulative = 0
			for i in ctx['rows']:
				i.cumulative_story_point = 0

			for i in ctx['rows']:
				cumulative = cumulative + i.estimate_of_story_point
				i.cumulative_story_point = cumulative

			q = Item.objects.aggregate(itemCount=Count('order'),
				remainSS=Sum('remaining_sprint_size'),
				totalSS=Sum('original_sprint_size'),
			)
			ctx['itemCount'] = q['itemCount']
			ctx['remainSS'] = q['remainSS']
			ctx['totalSS'] = q['totalSS']
			return ctx

class PersomHomepage(TemplateView):
		template_name = 'PersonHomePage.html'

		def get_context_data(self, **kwargs):
			person = self.kwargs['person']
			context = super().get_context_data(**kwargs)
			context['person']=Person.objects.get(pk = person)
			return context

class ProjectList(TemplateView):
	template_name="ProjectList.html"
	model = Project
	
	def get_context_data(self, **kwargs):
		ctx = super(ProjectList, self).get_context_data(**kwargs)
		ctx['header'] = ['Project Name', 'Description', 'Action']
		ctx['rows'] = Project.objects.all()
		return ctx
		
#-------------------sprintbacklog---------------------------------
class sprint_backlog(TemplateView):
	template_name = "sprint_backlog.html"
	def get_context_data(self, **kwargs):
		sprint = self.kwargs['sprint']
		context = super().get_context_data(**kwargs)
		context['pbi_list'] = Item.objects.filter(sprint__pk = sprint)
		context['task_list']= Task.objects.filter(sprint__pk = sprint)
		context['sprint'] = Sprint.objects.get(pk = sprint)
		return context
		
class TaskCreateView(CreateView):
		model = Task
		fields = '__all__'
		template_name = 'task_create.html'
