from django.forms import ModelForm
from .models import Task
from django import forms


class TaskForm(ModelForm):
    class Meta: # proporciona opciones que controlan el comportamiento del modelo, cómo se mapea a la base de datos, y otras configuraciones.
        model = Task # modelo a asociar para crear instancia 
        fields = ['title','description','important'] # campos que quiero mostrar
        widgets = { # con widgets le digo que le de estilos a los inputs pasandole el atributo class y la clase de bootstrap
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'agregar título'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'agregar descripción'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input ms-1'}),
        }
        
        

# NOTA: 
# diferencia entre usar Form y ModelForm como parametro en la clase
# forms.Form      ---> no esta vinculado a ningun modelo de base de datos.  Los campos del formulario se definen explícitamente en el formulario y no están relacionados con ninguna tabla en la base de datos
# ModelForm ---> esta vinculado a un modelo de base de datos(los que cree en models.py). le paso el modelo Task por ej y me crea una instancia de el. le puedo decir que campos del modelo mostrar y luego me permite editarlos con sus metodos 
# ModelForm es mas seguro y aplica validaciones adicionales de django