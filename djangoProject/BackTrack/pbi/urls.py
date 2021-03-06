from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('register/', 
		views.register, 
		name='register'),
	path('login/', 
		auth_views.LoginView.as_view(), 
		name='login'),
	path('logout/', 
		auth_views.LogoutView.as_view(), 
		name='logout'),
	path('password_reset/', 
		auth_views.PasswordResetView.as_view(), 
		name='password_reset'),
	path('password_reset_done/', 
		auth_views.PasswordResetDoneView.as_view(), 
		name='password_reset_done'),
	path('password_reset_confirm/<uidb64>/<token>/', 
		auth_views.PasswordResetConfirmView.as_view(), 
		name='password_reset_confirm'),
	path('password_reset_complete/', 
		auth_views.PasswordResetCompleteView.as_view(), 
		name='password_reset_complete'),
	path('profile/', 
		views.ProfileView.as_view(),
		name='profile'),
	#path('updatePerson/<int:personUpdate_pk>/',
	#	views.PersonUpdateView.as_view(),
	#	name='updatePerson'),
	#path('viewProfile/<int:person>/',
	#	views.RedirectedProfileView.as_view(),
	#	name='viewProfile'),
	path('joinProject/', 
		views.JoinProjectView, 
		name='joinProject'),
	path('BeDeveloper/', 
		views.BeDeveloperView, 
		name='BeDeveloper'),
	path('BeManager/', 
		views.BeManagerView, 
		name='BeManager'),
	path('Invite/', 
		views.InviteView.as_view(), 
		name='Invite'),
	path('SendMail/<emails>', 
		views.SendMailView, 
		name='SendMail'),
	path('SendMailToManager/<emails>', 
		views.SendMailToManagerView, 
		name='SendMailToManager'),
	path('SendMailToAllManager/', 
		views.SendMailToAllManagerView, 
		name='SendMailToAllManager'),

	path('SendMailToAll/', 
		views.SendMailToAllView, 
		name='SendMailToAll'),
	path('changePassword/',
		views.change_password,
		name='change_password'),

	path('', 
		views.index, 
		name='index'),
	#---------------Product Backlog---------------------------------------------------#
	path('viewPBIdetail/<int:item>/',
		views.PbiDetailView.as_view(),
		name='viewPBIdetail'),
	path('createPBI/',
		views.PbiCreateView.as_view(),
		name='createPBI'),
	path('updatePBI/<int:pbiUpdate_pk>/',
		views.PbiUpdateView.as_view(),
		name='updatePBI'),
	path('updatePBIsprint/<int:pbiUpdate_pk>/',
		views.PbiUpdateSprintView,
		name='updatePBIsprint'),
	path('deletePBI/<int:pbiDelete_pk>/',
		views.PbiDeleteView.as_view(),
		name='deletePBI'),
	path('viewProductbacklog/<int:project>/',
		views.PbiProjectView.as_view(),
		name='viewProductbacklog'),
	path('viewCurrentProductbacklog/<int:project>/',
		views.PbiProjectCurrentView.as_view(),
		name='viewCurrentProductbacklog'),
	path('PbiAddToSprintView/<int:pbi_pk>/',
		views.PbiAddToSprintView,
		name='PbiAddToSprintView'),
	path('PbiRemoveFromSprintView/<int:pbi_pk>/',
		views.PbiRemoveFromSprintView,
		name='PbiRemoveFromSprintView'),

	#---------------person---------------------------------------------------#
	#path('PersonHomePage/<int:person>/',
	#	views.PersomHomepage.as_view(),
	#	name='PersonHomepage'),
		
	#-----------project--------------------------------------------------#
	path('ProjectList/',
		views.ProjectList.as_view(),
		name='ProjectList'),
	path('viewProject/<int:project>/',
		views.ProjectView.as_view(),
		name='ProjectView'),
	path('ProjectToInProgress/<int:project_pk>/',
		views.ProjectToInProgressView,
		name='ProjectToInProgress'),
	path('ProjectToCompleted/<int:project_pk>/',
		views.ProjectToCompletedView,
		name='ProjectToCompleted'),
	path('createProject/',
		views.ProjectCreateView.as_view(),
		name='createProject'),
	#path('ProjectAddPO/<int:project_pk>/',
	#	views.ProjectAddPOView,
	#	name='ProjectAddPO'),

	#-------sprintbacklog--------------------------------------------------------#
	path('viewSprintBacklog/<int:sprint>/',
		views.viewSprintBacklog.as_view(),
		name='sprintbacklog'),
	path('createSprint/',
		views.SprintCreateView.as_view(),
		name='createSprint'),
	#path('SprintAddDetail/<int:sprint_pk>/',
	#	views.SprintAddDetailView,
	#	name='SprintAddDetail'),

	path('deleteSprint/<int:sprintDelete_pk>/',
		views.SprintDeleteView.as_view(),
		name='deleteSprint'),
	path('updateSprint/<int:sprintUpdate_pk>/',
		views.SprintUpdateView.as_view(),
		name='updateSprint'),
	path('SprintToInProgress/<int:sprint_pk>/',
		views.SprintToInProgressView,
		name='SprintToInProgress'),
	path('SprintToCompleted/<int:sprint_pk>/',
		views.SprintToCompletedView,
		name='SprintToCompleted'),
	path('createTask/<int:item_pk>/',
		views.TaskCreateView.as_view(),
		name='createTask'),
	#path('TaskAddDetail/<int:task_pk>/',
	#	views.TaskAddDetailView,
	#	name='TaskAddDetail'),

	path('viewTask/<int:task>/',
		views.TaskView.as_view(),
		name='viewTask'),
	path('deleteTask/<int:taskDelete_pk>/',
		views.TaskDeleteView.as_view(),
		name='deleteTask'),
	path('updateTask/<int:taskUpdate_pk>/',
		views.TaskUpdateView.as_view(),
		name='updateTask'),
	path('TaskToNotYetStarted/<int:task_pk>/',
		views.TaskToNotYetStartedView,
		name='TaskToNotYetStarted'),
	path('TaskToInProgress/<int:task_pk>/',
		views.TaskToInProgressView,
		name='TaskToInProgress'),
	path('TaskToCompleted/<int:task_pk>/',
		views.TaskToCompletedView,
		name='TaskToCompleted'),
	path('TaskOwn/<int:task_pk>/',
		views.TaskOwnView,
		name='TaskOwn'),

]
