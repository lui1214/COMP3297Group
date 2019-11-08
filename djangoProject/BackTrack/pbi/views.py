from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView,ListView
from .models import Item,Person,Project,Task,Developer,ScrumMaster,ProductOwner,Sprint
from .forms import ItemForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum
from datetime import datetime
import datetime
from django.utils import timezone
from django.forms import modelformset_factory
from django.urls import reverse_lazy, reverse

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
	#fields = ['order']
	template_name = 'pbi_new.html'
	success_url = '/pbi/viewPBI/'    
	
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
		ctx['header'] = ['Order', 'Feature Name', 'Description', 'Sprint', 'Remaining Sprint Size', 'Estimate of Story Point', 'Cumulative Story Point', 'Status', 'Last Modified', 'Created At', 'Action']
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
			totalSS=Sum('estimate_of_story_point'),
		)
		
		ctx['itemCount'] = q['itemCount']
		ctx['remainSS'] = q['remainSS']
		ctx['totalSS'] = q['totalSS']
		return ctx
class PbiView(TemplateView):
	template_name = 'pbi_list.html'

	def get_context_data(self, **kwargs):
		ctx = super(PbiView, self).get_context_data(**kwargs)
		ctx['header'] = ['Order', 'Feature Name', 'Description', 'Sprint', 'Remaining Sprint Size', 'Estimate of Story Point', 'Cumulative Story Point', 'Status', 'Last Modified', 'Created At', 'Action']
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
			totalSS=Sum('estimate_of_story_point'),
		)

		ctx['itemCount'] = q['itemCount']
		ctx['remainSS'] = q['remainSS']
		ctx['totalSS'] = q['totalSS']
		return ctx
class PbiCurrentView(TemplateView):
	template_name = 'pbi_currentList.html'
	
	def get_context_data(self, **kwargs):
		ctx = super(PbiCurrentView, self).get_context_data(**kwargs)
		ctx['header'] = ['Order', 'Feature Name', 'Description', 'Sprint', 'Remaining Sprint Size', 'Estimate of Story Point', 'Cumulative Story Point', 'Status', 'Last Modified', 'Created At', 'Action']
		ctx['rows'] = Item.objects.all().order_by('order', '-last_modified')
		
		cumulative = 0
		for i in ctx['rows']:
			i.cumulative_story_point = 0
			
		for i in ctx['rows']:
			cumulative = cumulative + i.estimate_of_story_point
			i.cumulative_story_point = cumulative
			
		q = Item.objects.aggregate(itemCount=Count('order'),
			remainSS=Sum('remaining_sprint_size'),
			totalSS=Sum('estimate_of_story_point'),
		)
		
		ctx['itemCount'] = q['itemCount']
		ctx['remainSS'] = q['remainSS']
		ctx['totalSS'] = q['totalSS']
		return ctx

#-------------------------person----------------------------------------------------
class PersomHomepage(TemplateView):
	template_name = 'PersonHomePage.html'

	def get_context_data(self, **kwargs):
		person = self.kwargs['person']
		context = super().get_context_data(**kwargs)
		context['person']=Person.objects.get(pk = person)
		return context
#--------------------------project------------------------------------------------------
class ProjectList(TemplateView):
	template_name="ProjectList.html"
	model = Project
	
	def get_context_data(self, **kwargs):
		ctx = super(ProjectList, self).get_context_data(**kwargs)
		ctx['header'] = ['Project Name', 'Description', 'Action']
		ctx['rows'] = Project.objects.all()
		return ctx

class ProjectView(TemplateView):
	template_name = 'project_view.html'
	def get_context_data(self, **kwargs):
		project = self.kwargs['project']
		context = super().get_context_data(**kwargs)
		context['project'] = Project.objects.get(pk=project)
		context['developer_list'] = Developer.objects.filter(project__pk = project)
		context['sprint_list'] = Sprint.objects.filter(project__pk = project)
		return context

class PbiProjectView(TemplateView):
	template_name = 'product_backlog.html'
	def get_context_data(self, **kwargs):
		project = self.kwargs['project']
		ctx = super().get_context_data(**kwargs)
		ctx = super(PbiProjectView, self).get_context_data(**kwargs)
		ctx['header'] = ['Order', 'Feature Name', 'Description', 'Sprint', 'Remaining Sprint Size', 'Estimate of Story Point', 'Cumulative Story Point', 'Status', 'Last Modified', 'Created At', 'Action']
		ctx['rows'] = Item.objects.filter(project__pk = project).order_by('order', '-last_modified')
		ctx['row1']=ctx['rows'][0]
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
			totalSS=Sum('estimate_of_story_point'),
		)

		ctx['itemCount'] = q['itemCount']
		ctx['remainSS'] = q['remainSS']
		ctx['totalSS'] = q['totalSS']
		return ctx

#-------------------sprintbacklog---------------------------------
class viewSprintBacklog(TemplateView):
	template_name = "sprint_backlog.html"
	def get_context_data(self, **kwargs):
		sprint = self.kwargs['sprint']
		context = super().get_context_data(**kwargs)
		context['pbi_list'] = Item.objects.filter(sprint__pk = sprint)
		context['task_list']= Task.objects.filter(sprint__pk = sprint)
		context['sprint'] = Sprint.objects.get(pk = sprint)
		
		nys = 0
		ip = 0
		done = 0
		total = []
		
		for i in context['task_list']:
			if i.status=="Completed":
				done = done + i.hour
			elif i.status=="In Progress":
				ip = ip + i.hour
			else:
				nys = nys + i.hour
		for i in context['pbi_list']:
			for j in context['task_list']:
				if j.item.name == i.name:
					k = next((p for p in total if p["name"] == j.item.name), False)
					if k == False:
						if j.status == "Completed":
							nameDict = { "name" : j.item.name, "remain" : 0, "burn" : j.hour, "totalDone": j.hour}
							total.append(nameDict)
						else:
							nameDict = { "name" : j.item.name, "remain" : j.hour, "burn" : 0, "totalDone": j.hour}
							total.append(nameDict)
					else:
						if j.status == "Completed":
							k["burn"] = k["burn"] + j.hour
						else:
							k["remain"] = k["remain"] + j.hour
						k["totalDone"] = k["totalDone"] +j.hour
				
		context['nys'] = nys
		context['ip'] = ip
		context['done'] = done
		context['remain'] = nys + ip
		context['tot'] = done + nys + ip
		context['total'] = total
		return context


class TaskCreateView(CreateView):
	model = Task
	fields = '__all__'
	template_name = 'task_create.html'
	
	def get_success_url(self):
		return reverse_lazy('sprintbacklog', kwargs={'sprint': self.object.sprint_id})

"""	def get_context_data(self, **kwargs):
		item = self.kwargs['item']
		context = super().get_context_data(**kwargs)
		context['item'] = Item.objects.get(pk=item)
		return context
"""

class TaskDeleteView(DeleteView):
	model = Task
	template_name = 'task_delete.html'
	pk_taskDelete_kwargs = 'taskDelete_pk'
	
	def get_success_url(self):
		return reverse_lazy('sprintbacklog', kwargs={'sprint': self.object.sprint_id})
	
	def get_object(self,queryset=None):
		snum = int(self.kwargs.get(self.pk_taskDelete_kwargs,None))
		obj = get_object_or_404(Task, pk=snum)
		return obj
			
class TaskView(TemplateView):
	template_name = 'task_view.html'
		
	def get_context_data(self, **kwargs):
		task = self.kwargs['task']
		context = super().get_context_data(**kwargs)
		context['task'] = Task.objects.get(pk=task)
		return context

class TaskUpdateView(UpdateView):
		model = Task
		fields = ['name','hour','description','status']
		template_name = 'task_create.html'
		pk_taskUpdate_kwargs = 'taskUpdate_pk'
		
		def get_success_url(self):
			return reverse_lazy('sprintbacklog', kwargs={'sprint': self.object.sprint_id})
		
		def get_object(self,queryset=None):
			snum = int(self.kwargs.get(self.pk_taskUpdate_kwargs,None))
			obj = get_object_or_404(Task, pk=snum)
			return obj
