#from django.db import models
from django.contrib.auth import models
from django.db import models as mod

# Create your models here.
class User(models.User, models.PermissionsMixin):
    
    def __str__(self):
        return "@{}".format(self.username)