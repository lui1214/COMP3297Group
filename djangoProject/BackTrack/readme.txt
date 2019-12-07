Hello user, you may not familiar with django or python but you just
need to make sure you follow the steps below before you start the 
program:

1. Install or update Django by the following command in the terminal 
	or command prompt:
	For installation:		pip install Django
	For update:				pip install Django --upgrade
	
2. Install Crispy Forms by the following command:
			pip install django-crispy-forms
			
3. Install pipenv by the following command:
			pip install pipenv
	
4. After you unzip the project (e.g. BackTrack in this time), type
	the following command and wait patiently when executing:
	
	4.1 First you need to make sure the path is like C:\...\BackTrack
		in the terminal or command prompt, if not then change the
		directory to BackTrack
			
	4.2 Install Django to the virtual environment by the 
		following command:
				pipenv install django
				
	4.3 After that, type the following command to start the virtual
		environment:
				pipenv shell
				
5. Finally, you can run the program by the following command:
			python manage.py runserver

Important Notes:
	If you want to send emails to invite people to join your project,
make sure the SMTP setting in \BackTrack\config\settings.py is correct.
The lines 131-134 are the configuration referring to your SMTP server,
username, password, and the SMTP port number.

	As the development time schedule is tight, we did not deal with the
concurrent update issue to provide the most valuable product to the 
customer. Besides, the permission of adding, modifying, and deleting the
objects may not be well set since the model and user model are already 
defined in the early stage, it is too time consuming to change the models
with dependencies with other models.