from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView,ListView
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum
from datetime import datetime
import datetime
import hashlib
import os
import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms import modelformset_factory
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
    return HttpResponseRedirect("/pbi/profile/")
    
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("/pbi/login/")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {'form' : form})

"""
@login_required(login_url='/pbi/login/')
def ProfileView(request):
    
    u = User.objects.get(username = request.user.username)
    
    try:
        p = Person.objects.get(user = u)
    except Person.DoesNotExist:
        newPerson = Person(user = u)
        newPerson.save()
        p = newPerson
        
    return HttpResponseRedirect('/pbi/viewProfile/%i/' % p.id)
    
class RedirectedProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'
    
    template_name = 'profile_view.html'
    
    def get_context_data(self, **kwargs):
        person = self.kwargs['person']
        context = super().get_context_data(**kwargs)
        context['person'] = Person.objects.get(pk=person)
        
        try :
            context['project'] = context['person'].project
        except Project.DoesNotExist:
            context['project'] = []
            
        return context
"""        

class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name="profile_view.html"
    model = Person
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        u = self.request.user
        try:
            p = Person.objects.get(user = u)
        except Person.DoesNotExist:
            newPerson = Person(user = u)
            newPerson.save()
            
        person1 = Person.objects.get(user = u)
        context['project'] = person1.project
        context['person'] = person1
        return context

        
@login_required(login_url='/pbi/login/')
def JoinProjectView(request):
    u = request.user
    per = Person.objects.get(user = u)
    if per.project is not None and per.project.status != "Completed":
        return render(request, 'alert.html', {"message" : "Project joined"})
    
    if request.method == "POST":
        form = JoinProjectForm(request.POST)
        if form.is_valid():
            field = form.cleaned_data['field']
            try:
                pro = Project.objects.get(Dhash = field)
                per.project = pro
                per.role = "Developer"
                per.save()
                return redirect("/pbi/")
            except Project.DoesNotExist:
                try:
                    pro = Project.objects.get(SMhash = field)
                    per.project = pro
                    per.role = "Scrum Master"
                    per.save()
                    return redirect("/pbi/")
                except Project.DoesNotExist:
                    return render(request, 'alert.html', {"message" : "Project does not exist"})
    else:
        form = JoinProjectForm()

    return render(request, "project_join.html", {"form" : form})

"""
class PersonUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Person
    fields = '__all__'
    template_name = 'pbi_new.html'
    pk_personUpdate_kwargs = 'personUpdate_pk'
    
    def get_object(self,queryset=None):
        snum = int(self.kwargs.get(self.pk_personUpdate_kwargs,None))
        obj = get_object_or_404(Person, pk=snum)
        return obj
    def get_success_url(self):
        return reverse_lazy('profile')
"""
    
class PbiUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Item
    fields = ['order', 'name', 'description', 'remaining_sprint_size', 'estimate_of_story_point', 'status']
    template_name = 'pbi_new.html'
    pk_pbiUpdate_kwargs = 'pbiUpdate_pk'
    
    def get_object(self,queryset=None):
        snum = int(self.kwargs.get(self.pk_pbiUpdate_kwargs,None))
        obj = get_object_or_404(Item, pk=snum)
        return obj
    def get_success_url(self):
        return reverse_lazy('viewProductbacklog', kwargs={'project': self.object.project_id})
"""        
class PbiUpdateSprintView(LoginRequiredMixin, UpdateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Item
    fields = ['sprint']
    template_name = 'pbi_new.html'
    pk_pbiUpdate_kwargs = 'pbiUpdate_pk'
    
    def get_object(self,queryset=None):
        snum = int(self.kwargs.get(self.pk_pbiUpdate_kwargs,None))
        obj = get_object_or_404(Item, pk=snum)
        return obj
    def get_success_url(self):
        return reverse_lazy('viewProductbacklog', kwargs={'project': self.object.project_id})
"""
@login_required(login_url='/pbi/login/')
def PbiUpdateSprintView(request, pbiUpdate_pk):

    obj = get_object_or_404(Item, pk=pbiUpdate_pk)
    obj.sprint = Sprint.objects.get(number = obj.project.last_sprint, project = obj.project)
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewProductbacklog/%i/' % obj.project.id)

class PbiDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Item
    template_name = 'pbi_delete.html'
    pk_pbiDelete_kwargs = 'pbiDelete_pk'
    
    def get_object(self,queryset=None):
        snum = int(self.kwargs.get(self.pk_pbiDelete_kwargs,None))
        obj = get_object_or_404(Item, pk=snum)
        return obj
    def get_success_url(self):
        return reverse_lazy('viewProductbacklog', kwargs={'project': self.object.project_id})

class PbiCreateView(LoginRequiredMixin, CreateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Item
    fields = ['order', 'name', 'description', 'remaining_sprint_size', 'estimate_of_story_point']
    #fields = ['order']
    template_name = 'pbi_new.html'
    success_url = '/pbi/viewPBI/'
    def get_success_url(self):
        return reverse_lazy('viewProductbacklog', kwargs={'project': self.object.project_id})
    
class PbiDetailView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'pbi_detail.html'
    
    def get_context_data(self, **kwargs):
        item = self.kwargs['item']
        
        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=item)
        return context
        
@login_required(login_url='/pbi/login/')
def PbiAddToSprintView(request, pbi_pk):

    obj = get_object_or_404(Item, pk=pbi_pk)
    obj.added = True
    obj.status = 'In Progress'
    if obj.sprint.status != "Completed":
        k = obj.sprint
        k.status = "In Progress"
        k.save()
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewProductbacklog/%i/' % obj.project.id)

@login_required(login_url='/pbi/login/')    
def PbiRemoveFromSprintView(request, pbi_pk):

    obj = get_object_or_404(Item, pk=pbi_pk)
    obj.added = False
    obj.status = 'Not yet started'
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewProductbacklog/%i/' % obj.project.id)

"""
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
"""
#-------------------------person----------------------------------------------------
class PersomHomepage(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'PersonHomePage.html'

    def get_context_data(self, **kwargs):
        person = self.kwargs['person']
        context = super().get_context_data(**kwargs)
        context['person']=Person.objects.get(pk = person)
        return context
#--------------------------project------------------------------------------------------
@login_required(login_url='/pbi/login/')
def ProjectToInProgressView(request, project_pk):

    obj = get_object_or_404(Project, pk=project_pk)
    obj.status = 'In Progress'
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewProductbacklog/%i/' % obj.id)

@login_required(login_url='/pbi/login/')
def ProjectToCompletedView(request, project_pk):
    
    obj = get_object_or_404(Project, pk=project_pk)
    obj.status = 'Completed'
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewProductbacklog/%i/' % obj.id)
   
class ProjectList(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name="ProjectList.html"
    model = Project
    
    def get_context_data(self, **kwargs):
        ctx = super(ProjectList, self).get_context_data(**kwargs)
        ctx['header'] = ['Project Name', 'Description', 'Status', 'Action']
        u = self.request.user
        per = Person.objects.get(user = u)
        p = per.project
        ctx['r'] = p
        return ctx

class ProjectView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'project_view.html'
    def get_context_data(self, **kwargs):
        project = self.kwargs['project']
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=project)
        context['developer_list'] = Person.objects.filter(project__pk = project, role = 'Developer')
        context['productowner_list'] = Person.objects.filter(project__pk = project, role = 'Product Owner')
        context['scrummaster_list'] = Person.objects.filter(project__pk = project, role = 'Scrum Master')
        context['sprint_list'] = Sprint.objects.filter(project__pk = project)
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Project
    fields = ['name', 'description']
    template_name = 'sprint_create.html'
    def get_success_url(self):
        #return HttpResponseRedirect('/pbi/ProjectAddPO/%i/' % self.object.pk)
        return reverse_lazy('ProjectAddPO', kwargs={'project_pk': self.object.pk})

@login_required(login_url='/pbi/login/')
def ProjectAddPOView(request, project_pk):
    obj = get_object_or_404(Project, pk=project_pk)
    u = request.user
    person1 = Person.objects.get(user = u)
    person1.role = 'Product Owner'
    person1.project = obj
    person1.save()
    
    return HttpResponseRedirect("/pbi/")

class PbiProjectView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'product_backlog.html'
    def get_context_data(self, **kwargs):
        project = self.kwargs['project']
        ctx = super().get_context_data(**kwargs)
        ctx = super(PbiProjectView, self).get_context_data(**kwargs)
        ctx['header'] = ['Order', 'Feature Name', 'Description', 'Sprint', 'Remaining Sprint Size', 'Estimate of Story Point', 'Cumulative Story Point', 'Status', 'Last Modified', 'Created At', 'Action']
        ctx['rows'] = Item.objects.filter(project__pk = project).order_by('order', '-last_modified')
        ctx['row1'] = Project.objects.get(pk=project)
        x = 1
        for i in ctx['rows']:
            if (i.order != x):
                i.order = x
                i.save()
            #i.last_sorted = timezone.now()
            x+=1
        
        for i in ctx['rows']: 
            try:
                find = Task.objects.filter(item = i)
                for j in find:
                    j.sprint = i.sprint
                    j.save()
            except Task.DoesNotExist:
                i = i
                
        for i in ctx['rows']:
            if i.status == "Not finished" and i.sprint.status == "In Progress":
                i.status = "In Progress"
            elif i.status == "In Progress" and i.sprint.status == "Completed":
                i.status = "Not finished"
        
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
        
class PbiProjectCurrentView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'product_backlog_current.html'
    def get_context_data(self, **kwargs):
        project = self.kwargs['project']
        ctx = super().get_context_data(**kwargs)
        ctx = super(PbiProjectCurrentView, self).get_context_data(**kwargs)
        ctx['header'] = ['Order', 'Feature Name', 'Description', 'Sprint', 'Remaining Sprint Size', 'Estimate of Story Point', 'Cumulative Story Point', 'Status', 'Last Modified', 'Created At', 'Action']
        ctx['rows'] = Item.objects.filter(project__pk = project).order_by('order', '-last_modified')
        ctx['row1'] = Project.objects.get(pk=project)

        for i in ctx['rows']:        
            try:
                find = Task.objects.filter(item = i)
                for j in find:
                    if j.sprint.status == "In Progress":
                        j.sprint = i.sprint
                        j.save()
            except Task.DoesNotExist:
                i = i
                
        for i in ctx['rows']:
            if i.status == "Not finished" and i.sprint.status == "In Progress":
                i.status = "In Progress"
            elif i.status == "In Progress" and i.sprint.status == "Completed":
                i.status = "Not finished"
        
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
"""        
class SprintCreateView(LoginRequiredMixin, CreateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Sprint
    fields = ['capacity']
    template_name = 'sprint_create.html'
    def get_success_url(self):
        return reverse_lazy('ProjectView', kwargs={'project': self.object.project_id})
"""

class SprintCreateView(LoginRequiredMixin, CreateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'
    model = Sprint
    fields = ['capacity']
    template_name = 'sprint_create.html'
    def get_success_url(self):
        return reverse_lazy('SprintAddDetail', kwargs={'sprint_pk': self.object.pk})

@login_required(login_url='/pbi/login/')
def SprintAddDetailView(request, sprint_pk):
    obj = get_object_or_404(Sprint, pk=sprint_pk)
    u = request.user
    person1 = Person.objects.get(user = u)
    pro = person1.project
    obj.project = pro
    obj.number = pro.last_sprint + 1
    pro.last_sprint = pro.last_sprint + 1
    pro.save()
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewProject/%i/' % obj.project.id)


class SprintDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Sprint
    template_name = 'sprint_delete.html'
    pk_sprintDelete_kwargs = 'sprintDelete_pk'
    
    def get_success_url(self):
        p = Project.objects.get(id = self.object.project_id)
        tempS = Sprint.objects.get(project = p, number = p.last_sprint)
        i = Item.objects.filter(project = p, sprint = tempS)
        for items in i:
            if items.status == "In Progress":
                items.status == "Not finished"
            items.sprint = Sprint.objects.get(project = p, number = p.last_sprint - 1)
            
            tasks = Task.objects.filter(item = items)
            for t in tasks:
                t.sprint = t.item.sprint
                t.save()
            
            items.save()
        p.last_sprint = p.last_sprint - 1
        p.save()
        
        return reverse_lazy('ProjectView', kwargs={'project': self.object.project_id})
    
    def get_object(self,queryset=None):
        snum = int(self.kwargs.get(self.pk_sprintDelete_kwargs,None))
        obj = get_object_or_404(Sprint, pk=snum)
        return obj
        
class SprintUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Sprint
    fields = '__all__'
    template_name = 'sprint_create.html'
    pk_sprintUpdate_kwargs = 'sprintUpdate_pk'
        
    def get_success_url(self):
        return reverse_lazy('ProjectView', kwargs={'project': self.object.project_id})
        
    def get_object(self,queryset=None):
        snum = int(self.kwargs.get(self.pk_sprintUpdate_kwargs,None))
        obj = get_object_or_404(Sprint, pk=snum)
        return obj
        
#-------------------sprintbacklog---------------------------------
class viewSprintBacklog(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

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
            if i.item.added == True:
                if i.status=="Completed":
                    done = done + i.hour
                elif i.status=="In Progress":
                    ip = ip + i.hour
                else:
                    nys = nys + i.hour
                
        for i in context['pbi_list']:
            for j in context['task_list']:
                if j.item.added == True:
                    if j.item.name == i.name:
                        k = next((p for p in total if p["name"] == j.item.name), False)
                        if k == False:
                            if j.status == "Completed":
                                nameDict = { "name" : j.item.name, "remain" : 0, "burn" : j.hour, "totalDone": j.hour, "allDone": 1, "completed": 1, "notCompleted": 0, "CNC": 1}
                                total.append(nameDict)
                            else:
                                nameDict = { "name" : j.item.name, "remain" : j.hour, "burn" : 0, "totalDone": j.hour, "allDone": 0, "completed": 0, "notCompleted": 1, "CNC": 1}
                                total.append(nameDict)
                        else:
                            if j.status == "Completed":
                                k["burn"] = k["burn"] + j.hour
                                k["completed"] = k["completed"] + 1
                            else:
                                k["remain"] = k["remain"] + j.hour
                                k["notCompleted"] = k["notCompleted"] + 1
                                k["allDone"] = 0
                            k["CNC"] = k["CNC"] + 1
                            k["totalDone"] = k["totalDone"] + j.hour
                            
        if len(context['pbi_list']) == 0:
            megaDone = 0;
        
        if len(context['pbi_list']) > 0:
            megaDone = 1;
            
            for i in context['pbi_list']:
                for j in total:
                    if i.name == j["name"]:
                        i.remaining_sprint_size = j["notCompleted"]
                        i.estimate_of_story_point = j["CNC"]
                        if j["allDone"] == 1:
                            i.status = "Completed"
                        elif j["allDone"] == 0:
                            if i.sprint.status == "Completed":
                                i.status = "Not finished"
                                """
                                try:
                                    find = Sprint.objects.get(number = i.sprint.number + 1, project = i.project)
                                    i.sprint = find
                                    find2 = Task.objects.get(sprint = i.sprint.number + 1, project = i.project, item = i)
                                    for k in find2:
                                        if k.status != "Completed":
                                            k.sprint = i.sprint.number + 1
                                            k.save()
                                except Sprint.DoesNotExist:
                                    i.sprint = i.sprint
                                """
                            else:
                                i.status = "In Progress"
                            megaDone = 0
                        i.save()
                        
            """
            if megaDone == 1:
                k = context['sprint']
                k.status = "Completed"
                j = k.project
                
                try:
                    find = Sprint.objects.get(number = k.number + 1, project = j)
                except Sprint.DoesNotExist:
                    newSprint = Sprint(number = k.number + 1 , capacity = 0, status = "Not yet started", project = j)
                    newSprint.save()
            
                j.last_sprint = k.number + 1
                j.save()
                k.save()
            
            elif megaDone == 0:
                k = context['sprint']
                k.status = "In Progress"
                j = k.project
                j.last_sprint = k.number
                j.save()
                k.save()
            """
            
        context['megaDone'] = megaDone
        context['nys'] = nys
        context['ip'] = ip
        context['done'] = done
        context['remain'] = nys + ip
        context['tot'] = done + nys + ip
        context['total'] = total
        return context

@login_required(login_url='/pbi/login/')
def SprintToInProgressView(request, sprint_pk):
    obj = get_object_or_404(Sprint, pk=sprint_pk)
    obj.status = 'In Progress'
    
    j = obj.project
    j.last_sprint = obj.number
    j.save()
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.id)

@login_required(login_url='/pbi/login/')
def SprintToCompletedView(request, sprint_pk):

    obj = get_object_or_404(Sprint, pk=sprint_pk)
    obj.status = 'Completed'
    obj.end_at = timezone.now()
    obj.save()
    
    j = obj.project
    finished = 1
    k = Item.objects.filter(sprint__pk = sprint_pk)
    for f in k:
        if f.status != "Completed":
            finished = 0
    
    try:
        find = Sprint.objects.get(number = obj.number + 1, project = j)
    except Sprint.DoesNotExist:
        if finished == 0:
            
            j.last_sprint = obj.number + 1
            j.save()
            newSprint = Sprint(number = obj.number + 1 , capacity = 0, status = "Not yet started", project = j)
            newSprint.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.id)
"""
class TaskCreateView(LoginRequiredMixin, CreateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Task
    fields = ['name', 'description', 'hour']
    template_name = 'task_create.html'
    
    def get_success_url(self):
        return reverse_lazy('sprintbacklog', kwargs={'sprint': self.object.sprint_id})
"""
class TaskCreateView(LoginRequiredMixin, CreateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'
    model = Task
    fields = ['name', 'description', 'hour']
    template_name = 'task_create.html'
    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `Ipsum` instance exists
        before going any further.
        """
        self.item = get_object_or_404(Item, pk=kwargs['item_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        form.instance.item = self.item
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('TaskAddDetail', kwargs={'task_pk': self.object.pk})

@login_required(login_url='/pbi/login/')
def TaskAddDetailView(request, task_pk):
    obj = get_object_or_404(Task, pk=task_pk)
    u = request.user
    person1 = Person.objects.get(user = u)
    pro = person1.project
    s = Sprint.objects.get(project = pro, number = pro.last_sprint)
    obj.sprint = s
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.sprint.id)
"""
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Task
    fields = ['name', 'description', 'hour', 'status', 'person']
    template_name = 'task_create.html'
    pk_taskUpdate_kwargs = 'taskUpdate_pk'
        
    def get_success_url(self):
        return reverse_lazy('sprintbacklog', kwargs={'sprint': self.object.sprint_id})
        
    def get_object(self,queryset=None):
        snum = int(self.kwargs.get(self.pk_taskUpdate_kwargs,None))
        obj = get_object_or_404(Task, pk=snum)
        return obj
"""
"""    def get_context_data(self, **kwargs):
        item = self.kwargs['item']
        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=item)
        return context
"""

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Task
    template_name = 'task_delete.html'
    pk_taskDelete_kwargs = 'taskDelete_pk'
    
    def get_success_url(self):
        return reverse_lazy('sprintbacklog', kwargs={'sprint': self.object.sprint_id})
    
    def get_object(self,queryset=None):
        snum = int(self.kwargs.get(self.pk_taskDelete_kwargs,None))
        obj = get_object_or_404(Task, pk=snum)
        return obj
            
class TaskView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'task_view.html'
        
    def get_context_data(self, **kwargs):
        task = self.kwargs['task']
        context = super().get_context_data(**kwargs)
        context['task'] = Task.objects.get(pk=task)
        return context

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Task
    fields = ['name', 'description', 'hour']
    template_name = 'task_create.html'
    pk_taskUpdate_kwargs = 'taskUpdate_pk'
        
    def get_success_url(self):
        return reverse_lazy('sprintbacklog', kwargs={'sprint': self.object.sprint_id})
        
    def get_object(self,queryset=None):
        snum = int(self.kwargs.get(self.pk_taskUpdate_kwargs,None))
        obj = get_object_or_404(Task, pk=snum)
        return obj

@login_required(login_url='/pbi/login/')
def TaskToNotYetStartedView(request, task_pk):

    obj = get_object_or_404(Task, pk=task_pk)
    obj.status = 'Not yet started'
    k = obj.sprint
    k.status = "In Progress"
    k.save()
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.sprint.id)

@login_required(login_url='/pbi/login/')
def TaskToInProgressView(request, task_pk):

    obj = get_object_or_404(Task, pk=task_pk)
    obj.status = 'In Progress'
    k = obj.sprint
    k.status = "In Progress"
    k.save()
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.sprint.id)

@login_required(login_url='/pbi/login/')
def TaskToCompletedView(request, task_pk):

    obj = get_object_or_404(Task, pk=task_pk)
    obj.status = 'Completed'
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.sprint.id)
    
@login_required(login_url='/pbi/login/')
def TaskOwnView(request, task_pk):
    obj = get_object_or_404(Task, pk=task_pk)
    u = request.user
    person1 = Person.objects.get(user = u)
    obj.person = person1
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.sprint.id)