from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # importo formularios de django para crear usario y formulario para autenticarse 
from django.contrib.auth.models import User # importo modelo User (clase) de django para registrar usuarios
from django.contrib.auth import login,authenticate, logout #importo el metodo login - crea cookie en la sesion del navegador 
from django.db import IntegrityError
from .forms import TaskForm
from.models import Task
from django.utils import timezone # metodo timezone de django, no es de python
from django.contrib.auth.decorators import login_required # decorator para proteccion de rutas - en settingS.py agregar variable LOGIN_URL = 'ruta donde quiero redirigir?

# Create your views here.

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html',{
            'form':UserCreationForm,
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            
            # manejo de errores con try except (equivalente a try catch de JS)
            try:
                #intento registro del usuario con el modelo User de django. (este metodo ya cifra la contraseña)
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user) #guardo sesion de usuario en el navegador para usar sus datos y dar permisos - ver con inspect seccion almacenamiento cookies del navegador
                return redirect('tasks') #redirijo a la vista de tareas
            
            # si falla el guardado de usuario capturo el error para que no crashee la app - integrity error para marcar errores de restriccion de la base de datos(ej cuando una actualizacion o insercion de datos en una db viola las reglas)
            except IntegrityError as error: # con integritiy le digo que django considere esto como un error de integridad y luego puedo procesarlo(con as le doy el nombre que quiero) 
                # ejemplo de manejo de error de integrity
                print(f"error de integridad: {error}")
                
                return render(request,'signup.html',{
                    'form':UserCreationForm,
                    'error':'El nombre de usuario ya existe'
                })

        # si el if no se cumple porque las passwords no coinciden envio error
        return render(request,'signup.html',{
            'form':UserCreationForm,
            'error':'La contraseña no coincide'
                })
        
# proteccion de rutas para que si no estas logueado ni entre a la ruta        
@login_required      
def tasks(request):
    # traigo las tareas del usuario con filter y user como parametro
    
    # tasks = Task.objects.filter(user=request.user) # muestra todas las tareas, completadas o  no del usuario
    
    # parametro user y datecompleated__null validan que las tareas sean del usaurio autenticado y traiga solo las tareas que NO estan completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) 
    return render(request,'tasks.html', {
        'tasks':tasks
    })

@login_required     
def tasks_completed(request):
    # parametro user y datecompleated__null validan que las tareas sean del usaurio autenticado y traiga solo las tareas que NO estan completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') 
    # uso el mismo template para renderizar la tareas completadas pero con otra url
    return render(request,'tasks.html', {
        'tasks':tasks
    })

@login_required 
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form':TaskForm
        })
    else:
        try:
            # Recibimos los datos del formulario (request.POST) y Creos una instancia del formulario (TaskForm) con esos datos.
            form = TaskForm(request.POST)
            # Guardo el objeto de task en una instancia,pero sin guardarlo en la db aún para poder seguir manipulandolo(usando commit=False).
            new_task = form.save(commit=False) 
            # guardo el usuario en la instancia de task -request.user: proporcionado automáticamente por Django cuando el usuario está autenticado
            new_task.user = request.user   
            # guardo la task en la db
            new_task.save()
            return redirect('tasks')
        
        except ValueError: # valueError --> cuando una función o operación recibe un valor de un tipo o formato incorrecto, pero no necesariamente relacionado con la base de datos. Es un error común en Python cuando un valor no es adecuado para la operación que se está intentando realizar.
            return render(request, 'create_task.html', {
                'form':TaskForm,
                'error': 'por favor ingresa datos validos'
            })
            
@login_required             
def task_detail(request, task_id):
    if request.method == 'GET':
        # traigo la instancia actual de task de la db con primrykey = task_id y que sea del user autenticado (user = request.user)
        task = get_object_or_404(Task, pk=task_id, user=request.user) # request.user para que solo muestre mis tareas y no de otros usuarios
        # paso la instancia actual de Task al TaskForm para completar sus campos (instance=Task  asociar el formulario con una instancia existente de Task. Le indica a Django que el formulario debe actualizar los campos de esa instancia con los datos del formulario en lugar de crear una nueva instancia).
        form = TaskForm(instance=task)
  
        # le paso la task y el formulario para actualizar al html
        return render(request, 'task_detail.html', {
            'task':task,
            'form':form
        })
    else:
        try:
            # traigo la tarea de la db para actualizarla
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            # traigo los datos actualizados del metodo POST  del formulario luego del submit  y se los paso a la instancia actual de task para actualizarla
            form = TaskForm(request.POST, instance=task)
            # guardo los datos del formulario task acutalizados en la db
            form.save()
            return redirect('tasks')
        
        except ValueError:
            return render(request, 'task_detail.html', {
            'task':task,
            'form':form,
            'error':'Error al actualizar tarea'
            })
            
@login_required         
def complete_task(request, task_id):
    # traigo la task de la db
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    # si hizo submit con boton completado
    if request.method == 'POST':
        # asigno fecha de completado a la variable datecompleated
        task.datecompleted = timezone.now()
        # guardo la task en la db
        task.save()
        return redirect('tasks')
    

@login_required     
def delete_task(request, task_id):
    # traigo la task de la db
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    # si hizo submit con boton delete
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
 
    
@login_required 
def signout(request): # no ponerme mismo nombre a la funcion que al metodo logout porque da conflicto
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form':AuthenticationForm,

        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form':AuthenticationForm,
                'error': 'usario o contraseña invalidos'

            })
        else:
            login(request,user)
            return redirect('tasks')
            

                



