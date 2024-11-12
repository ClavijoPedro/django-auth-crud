from django.contrib import admin
from .models import Task

# con esta clase heredo lo metodos del modelo admin para mostrar en el panel admin los campos de task que quiero ver como solo lectura
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )#ponerle coma al final porqur es una tupla

# Register your models here.
admin.site.register(Task, TaskAdmin) #registro el modelo y le paso los campos solo lectura



# panel admin superuser:
#     usuario: asus
#     pass: asus2024@