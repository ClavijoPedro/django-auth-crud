from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True) # crea la efecha automaticamente
    datecompleted = models.DateField(null=True, blank=True) # la fecha la tenemos que poner manual y con blanck true para que sea opcional
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # relaciono la task con el user a traves del id foreing_key y cuando se elimina el usuario se elimina todo lo relacionado a el

    
    # para que muestre nombre en panel admin y no object
    def __str__(self):
        return self.title + ' - by ' + self.user.username

# editar tablas desde la terminal: comando python manage.py shell ---> abre el shell de python con los modelos de tablas creados en django

# usario admin 
# user: asus
# pass: asus2024@ 