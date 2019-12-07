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
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms import modelformset_factory
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import *

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

@login_required(login_url='/pbi/login/') 
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form' : form})
    
class InviteView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name="mail_list.html"
    model = Person
    
    def get_context_data(self, **kwargs):
        context = super(InviteView, self).get_context_data(**kwargs)
        u = self.request.user
        
        person1 = Person.objects.get(user = u)
        context['person'] = person1
        context['developers'] = []
        context['managers'] = []
        ps = Person.objects.all()
        for i in ps:
            if i.project == None or i.project.status == "Completed":
                if i.role == "Developer" or i.role == "Product Owner":
                    context['developers'].append(i)
                else:
                    context['managers'].append(i)
        return context

@login_required(login_url='/pbi/login/')    
def SendMailView(request, emails):
    u = request.user
    person1 = Person.objects.get(user = u)
    p = person1.project
    dkey = person1.project.Dhash
    inviteMsg = "Hello I am " + person1.user.username + ". I would like to invite you to my project " + p.name + ". Here is the key to join the project: " + dkey
    email = EmailMessage('Project Invitation', inviteMsg, to=[emails])
    email.send()
    
    return HttpResponseRedirect("/pbi/Invite/")

@login_required(login_url='/pbi/login/')    
def SendMailToManagerView(request, emails):
    u = request.user
    person1 = Person.objects.get(user = u)
    p = person1.project
    dkey = person1.project.SMhash
    inviteMsg = "Hello I am " + person1.user.username + ". I would like to invite you to my project " + p.name + ". Here is the key to join the project: " + dkey
    email = EmailMessage('Project Invitation', inviteMsg, to=[emails])
    email.send()
    
    return HttpResponseRedirect("/pbi/Invite/")

@login_required(login_url='/pbi/login/')    
def SendMailToAllView(request):
    u = request.user
    person1 = Person.objects.get(user = u)
    p = person1.project
    dkey = person1.project.Dhash
    inviteMsg = "Hello I am " + person1.user.username + ". I would like to invite you to my project " + p.name + ". Here is the key to join the project: " + dkey
    ps = Person.objects.all()
    developers = []
    for i in ps:
        if i.project == None or i.project.status == "Completed":
            if i.role == "Developer" or i.role == "Product Owner":
                developers.append(i)
            
    for i in developers:
        email = EmailMessage('Project Invitation', inviteMsg, to=[i.user.email])
        email.send()
    
    return HttpResponseRedirect("/pbi/Invite/")
    
@login_required(login_url='/pbi/login/')      
def SendMailToAllManagerView(request):
    u = request.user
    person1 = Person.objects.get(user = u)
    p = person1.project
    dkey = person1.project.SMhash
    inviteMsg = "Hello I am " + person1.user.username + ". I would like to invite you to my project " + p.name + ". Here is the key to join the project: " + dkey
    ps = Person.objects.all()
    managers = []
    for i in ps:
        if i.project == None or i.project.status == "Completed":
            if i.role == "Scrum Master" or i.role == "Manager":
                managers.append(i)
            
    for i in managers:
        email = EmailMessage('Project Invitation', inviteMsg, to=[i.user.email])
        email.send()
    
    return HttpResponseRedirect("/pbi/Invite/")
    
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
def BeDeveloperView(request):
    u = request.user
    person1 = Person.objects.get(user = u)
    person1.role = "Developer"
    person1.chosen = 0
    person1.save()
    
    return HttpResponseRedirect('/pbi/profile/')
    
@login_required(login_url='/pbi/login/')
def BeManagerView(request):
    u = request.user
    person1 = Person.objects.get(user = u)
    person1.role = "Manager"
    person1.chosen = 0
    person1.save()
    
    return HttpResponseRedirect('/pbi/profile/')
        
@login_required(login_url='/pbi/login/')
def JoinProjectView(request):
    u = request.user
    per = Person.objects.get(user = u)
    if per.project is not None and per.project.status != "Completed":
        return render(request, 'alert.html', {"message" : "Already joined a project"})
    
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
    
class PbiUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Item
    fields = ['order', 'name', 'description', 'remaining_sprint_size', 'estimate_of_story_point', 'status']
    template_name = 'pbi_update.html'
    pk_pbiUpdate_kwargs = 'pbiUpdate_pk'
    
    def get_object(self,queryset=None):
        snum = int(self.kwargs.get(self.pk_pbiUpdate_kwargs,None))
        obj = get_object_or_404(Item, pk=snum)
        obj.oldOrder = obj.order
        u = self.request.user
        personCheck = Person.objects.get(user = u)
        if obj.project != personCheck.project or personCheck.role == "Scrum Master":
            obj = None
            return obj
        return obj
    def get_success_url(self):
        return reverse_lazy('viewProductbacklog', kwargs={'project': self.object.project_id})
        
@login_required(login_url='/pbi/login/')
def PbiUpdateSprintView(request, pbiUpdate_pk):

    obj = get_object_or_404(Item, pk=pbiUpdate_pk)
    u = request.user
    personCheck = Person.objects.get(user = u)
    if obj.project != personCheck.project or personCheck.role == "Scrum Master":
        return render(request, 'alert.html', {"message" : "Restricted Access"})
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
        u = self.request.user
        personCheck = Person.objects.get(user = u)
        if obj.project != personCheck.project or personCheck.role == "Scrum Master":
            obj = None
            return obj
        return obj
    def get_success_url(self):
        return reverse_lazy('viewProductbacklog', kwargs={'project': self.object.project_id})

class PbiCreateView(LoginRequiredMixin, CreateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Item
    fields = ['order', 'name', 'description', 'estimate_of_story_point']
    #fields = ['order']
    template_name = 'pbi_new.html'
    success_url = '/pbi/viewPBI/'
    def get_success_url(self):
        obj = get_object_or_404(Item, pk=self.object.pk)
        obj.oldOrder = obj.order
        obj.remaining_sprint_size = obj.estimate_of_story_point
        u = self.request.user
        personCheck = Person.objects.get(user = u)
        pro = personCheck.project
        s = Sprint.objects.get(number = pro.last_sprint, project = pro)
        obj.sprint = s
        obj.project = pro
        obj.save()
        return reverse_lazy('viewProductbacklog', kwargs={'project': obj.project.id})
    
class PbiDetailView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'pbi_detail.html'
    
    def get_context_data(self, **kwargs):
        item = self.kwargs['item']
        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=item)
        u = self.request.user
        personCheck = Person.objects.get(user = u)
        if personCheck.project != context['item'].project:
            context['header'] = []
            context['rows'] = []
            context['person'] = personCheck
            return context
        context['person1'] = personCheck
        return context
        
@login_required(login_url='/pbi/login/')
def PbiAddToSprintView(request, pbi_pk):

    obj = get_object_or_404(Item, pk=pbi_pk)
    u = request.user
    personCheck = Person.objects.get(user = u)
    if obj.project != personCheck.project or personCheck.role == "Scrum Master":
        return render(request, 'alert.html', {"message" : "Restricted Access"})
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
    u = request.user
    personCheck = Person.objects.get(user = u)
    if obj.project != personCheck.project or personCheck.role == "Scrum Master":
        return render(request, 'alert.html', {"message" : "Restricted Access"})
    obj.added = False
    obj.status = 'Not yet started'
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewProductbacklog/%i/' % obj.project.id)

#--------------------------project------------------------------------------------------
@login_required(login_url='/pbi/login/')
def ProjectToInProgressView(request, project_pk):

    obj = get_object_or_404(Project, pk=project_pk)
    
    u = request.user
    personCheck = Person.objects.get(user = u)
    if personCheck.project != Project.objects.get(pk=project_pk) or personCheck.role == "Scrum Master":
        return render(request, 'alert.html', {"message" : "Restricted Access"})
    
    obj.status = 'In Progress'
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewProductbacklog/%i/' % obj.id)

@login_required(login_url='/pbi/login/')
def ProjectToCompletedView(request, project_pk):
    
    obj = get_object_or_404(Project, pk=project_pk)
    
    u = request.user
    personCheck = Person.objects.get(user = u)
    if personCheck.project != Project.objects.get(pk=project_pk) or personCheck.role == "Scrum Master":
        return render(request, 'alert.html', {"message" : "Restricted Access"})
    
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
        
        u = self.request.user
        personCheck = Person.objects.get(user = u)
        context['person1'] = personCheck
        
        if personCheck.project != Project.objects.get(pk=project):
            context['person'] = personCheck
            return context
        
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
        obj = get_object_or_404(Project, pk=self.object.pk)
        u = self.request.user
        person1 = Person.objects.get(user = u)
        person1.role = 'Product Owner'
        person1.project = obj
        p = person1.project
        p.last_sprint = 1
        newSprint = Sprint(number = 1, project = p)
        newSprint.save()
        p.save()
        person1.save()
        
        return reverse_lazy('profile')
        #return HttpResponseRedirect('/pbi/ProjectAddPO/%i/' % self.object.pk)
        #return reverse_lazy('ProjectAddPO', kwargs={'project_pk': self.object.pk})

class PbiProjectView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'product_backlog.html'
    def get_context_data(self, **kwargs):
        project = self.kwargs['project']
        ctx = super().get_context_data(**kwargs)
        
        u = self.request.user
        
        ctx = super(PbiProjectView, self).get_context_data(**kwargs)
        
        personCheck = Person.objects.get(user = u)
        if personCheck.project != Project.objects.get(pk=project):
            ctx['header'] = []
            ctx['rows'] = []
            ctx['person'] = personCheck
            return ctx
            
        ctx['header'] = ['Order', 'Feature Name', 'Description', 'Sprint', 'Remaining Sprint Size', 'Estimate of Story Point', 'Cumulative Story Point', 'Status', 'Last Modified', 'Created At', 'Action']
        ctx['rows'] = Item.objects.filter(project__pk = project).order_by('order', '-oldOrder')
        ctx['row1'] = Project.objects.get(pk=project)
        
        x = 1
        for i in ctx['rows']:
            if (i.order != x):
                i.order = x
            if (i.oldOrder != x):
                i.oldOrder = x
                i.save()
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

        q = ctx['rows'].aggregate(itemCount=Count('order'),
            remainSS=Sum('remaining_sprint_size'),
            totalSS=Sum('estimate_of_story_point'),
        )

        ctx['itemCount'] = q['itemCount']
        ctx['remainSS'] = q['remainSS']
        ctx['totalSS'] = q['totalSS']
        ctx['person1'] = personCheck
        
        return ctx
        
class PbiProjectCurrentView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'product_backlog_current.html'
    def get_context_data(self, **kwargs):
        project = self.kwargs['project']
        ctx = super().get_context_data(**kwargs)
        
        
        u = self.request.user
        
        ctx = super(PbiProjectCurrentView, self).get_context_data(**kwargs)
        
        personCheck = Person.objects.get(user = u)
        if personCheck.project != Project.objects.get(pk=project):
            ctx['header'] = []
            ctx['rows'] = []
            ctx['person'] = personCheck
            return ctx
            
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
        ctx['person1'] = personCheck
        return ctx

class SprintCreateView(LoginRequiredMixin, CreateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'
    model = Sprint
    fields = ['capacity']
    template_name = 'sprint_create.html'
    def get_success_url(self):
        obj = get_object_or_404(Sprint, pk=self.object.pk)
        u = self.request.user
        person1 = Person.objects.get(user = u)
        pro = person1.project
        obj.project = pro
        obj.number = pro.last_sprint + 1
        pro.last_sprint = pro.last_sprint + 1
        pro.status = "In Progress"
        pro.save()
        obj.save()
        return reverse_lazy('ProjectView', kwargs={'project': obj.project.id})
        

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
        
        u = self.request.user
        personCheck = Person.objects.get(user = u)
        if obj.project != personCheck.project or personCheck.role == "Scrum Master":
            obj = None
            return obj
            
        return obj
        
class SprintUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    model = Sprint
    fields = ['capacity', 'status']
    template_name = 'sprint_update.html'
    pk_sprintUpdate_kwargs = 'sprintUpdate_pk'
        
    def get_success_url(self):
        return reverse_lazy('ProjectView', kwargs={'project': self.object.project_id})
        
    def get_object(self,queryset=None):
        snum = int(self.kwargs.get(self.pk_sprintUpdate_kwargs,None))
        obj = get_object_or_404(Sprint, pk=snum)
        u = self.request.user
        personCheck = Person.objects.get(user = u)
        if obj.project != personCheck.project or personCheck.role == "Scrum Master":
            obj = None
            return obj
        return obj
        
#-------------------sprintbacklog---------------------------------
class viewSprintBacklog(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name = "sprint_backlog.html"
    def get_context_data(self, **kwargs):
        sprint = self.kwargs['sprint']
        context = super().get_context_data(**kwargs)
        s = Sprint.objects.get(pk = sprint)
        
        u = self.request.user
        personCheck = Person.objects.get(user = u)
        pj = s.project
        if personCheck.project != pj:
            context['person'] = personCheck
            return context
            
        context['person1'] = personCheck
        context['pbi_list'] = Item.objects.filter(sprint__pk = sprint, project = s.project)
        context['task_list']= Task.objects.filter(sprint__pk = sprint)
        context['sprint'] = Sprint.objects.get(pk = sprint, project = s.project)
        
        
        nys = 0
        ip = 0
        done = 0
        total = []
        
        for i in context['task_list']:
            if i.item.added == True and i.item.project == s.project:
                if i.status=="Completed":
                    done = done + i.hour
                elif i.status=="In Progress":
                    ip = ip + i.hour
                else:
                    nys = nys + i.hour
                
        for i in context['pbi_list']:
            for j in context['task_list']:
                if j.item.added == True and j.item.project == s.project:
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
                        #i.estimate_of_story_point = j["CNC"]
                        if j["allDone"] == 1:
                            i.status = "Completed"
                        elif j["allDone"] == 0:
                            if i.sprint.status == "Completed":
                                i.status = "Not finished"
                            else:
                                i.status = "In Progress"
                            megaDone = 0
                        i.save()
            
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
    
    u = request.user
    personCheck = Person.objects.get(user = u)
    if obj.project != personCheck.project or personCheck.role == "Scrum Master":
        return render(request, 'alert.html', {"message" : "Restricted Access"})
    
    obj.status = 'In Progress'
    
    j = obj.project
    j.last_sprint = obj.number
    j.save()
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.id)

@login_required(login_url='/pbi/login/')
def SprintToCompletedView(request, sprint_pk):

    obj = get_object_or_404(Sprint, pk=sprint_pk)
    
    u = request.user
    personCheck = Person.objects.get(user = u)
    if obj.project != personCheck.project or personCheck.role == "Scrum Master":
        return render(request, 'alert.html', {"message" : "Restricted Access"})
    
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

class TaskCreateView(LoginRequiredMixin, CreateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'
    model = Task
    fields = ['name', 'description', 'hour']
    template_name = 'task_create.html'
    def dispatch(self, request, *args, **kwargs):
        self.item = get_object_or_404(Item, pk=kwargs['item_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.item = self.item
        return super().form_valid(form)
        
    def get_success_url(self):
        obj = get_object_or_404(Task, pk=self.object.pk) ## original
        u = self.request.user
        person1 = Person.objects.get(user = u)
        pro = person1.project
        s = Sprint.objects.get(project = pro, number = pro.last_sprint)
        obj.sprint = s
        if obj.sprint.project == obj.item.project:
            obj.save()
    
        #return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % self.object.sprint_id)
        #return reverse_lazy('TaskAddDetail', kwargs={'task_pk': self.object.pk})
        return reverse_lazy('sprintbacklog', kwargs={'sprint': obj.sprint.id})

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
        
        u = self.request.user
        personCheck = Person.objects.get(user = u)
        if obj.item.project != personCheck.project or personCheck.role == "Scrum Master":
            obj = None
            return obj
            
        return obj
            
class TaskView(LoginRequiredMixin, TemplateView):
    login_url = '/pbi/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'task_view.html'
        
    def get_context_data(self, **kwargs):
        task = self.kwargs['task']
        context = super().get_context_data(**kwargs)
        t = Task.objects.get(pk=task)
        u = self.request.user
        personCheck = Person.objects.get(user = u)
        if t.item.project != personCheck.project:
            context['person'] = personCheck
            return context
        
        context['task'] = t
        
        context['person1'] = personCheck
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
        u = self.request.user
        personCheck = Person.objects.get(user = u)
        if obj.item.project != personCheck.project or personCheck.role == "Scrum Master":
            obj = None
            return obj
        return obj

@login_required(login_url='/pbi/login/')
def TaskToNotYetStartedView(request, task_pk):

    obj = get_object_or_404(Task, pk=task_pk)
    
    u = request.user
    personCheck = Person.objects.get(user = u)
    if obj.item.project != personCheck.project or personCheck.role == "Scrum Master":
        return render(request, 'alert.html', {"message" : "Restricted Access"})
    
    obj.status = 'Not yet started'
    k = obj.sprint
    k.status = "In Progress"
    k.save()
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.sprint.id)

@login_required(login_url='/pbi/login/')
def TaskToInProgressView(request, task_pk):

    obj = get_object_or_404(Task, pk=task_pk)
    
    u = request.user
    personCheck = Person.objects.get(user = u)
    if obj.item.project != personCheck.project or personCheck.role == "Scrum Master":
        return render(request, 'alert.html', {"message" : "Restricted Access"})
    
    obj.status = 'In Progress'
    k = obj.sprint
    k.status = "In Progress"
    k.save()
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.sprint.id)

@login_required(login_url='/pbi/login/')
def TaskToCompletedView(request, task_pk):

    obj = get_object_or_404(Task, pk=task_pk)
    
    u = request.user
    personCheck = Person.objects.get(user = u)
    if obj.item.project != personCheck.project or personCheck.role == "Scrum Master":
        return render(request, 'alert.html', {"message" : "Restricted Access"})
    
    obj.status = 'Completed'
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.sprint.id)
    
@login_required(login_url='/pbi/login/')
def TaskOwnView(request, task_pk):
    obj = get_object_or_404(Task, pk=task_pk)
    
    u = request.user
    personCheck = Person.objects.get(user = u)
    if obj.item.project != personCheck.project or personCheck.role == "Scrum Master":
        return render(request, 'alert.html', {"message" : "Restricted Access"})
    
    u = request.user
    person1 = Person.objects.get(user = u)
    obj.person = person1
    obj.save()
    
    return HttpResponseRedirect('/pbi/viewSprintBacklog/%i/' % obj.sprint.id)