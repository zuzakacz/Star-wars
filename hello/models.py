from django.db import models
from django.utils import timezone


'''
class LogMessage(models.Model):
    message = models.CharField(max_length=300)
'''

class listOfDownloads(models.Model):
    singleDownload = models.URLField(max_length=300)
    file_name = models.CharField(max_length=300, default='')
    #NOTE change time zone to Polish one
    date = models.DateTimeField(default=timezone.now, null=True )



'''
to remove all the data from all tables:command in cmd with venv activated'''
#  python manage.py flush
'''This will delete all of the data in tables,
but the tables themselves will still exist'''

''' after changing models'''
#  python manage.py makemigrations
#  python manage.py migrate