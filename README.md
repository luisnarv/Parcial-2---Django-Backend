# Taller: Creacion de Endpoints en Django Nativo

**Curso:** Desarrollo de aplicaciones Web I · 4E  
**Docente:** Jose Javier Torres Vanstrahlen  

## 1. Introduccion a Endpoints Nativos en Django

En el desarrollo web con Django, es habitual utilizar librerias externas como Django REST Framework (DRF) para construir APIs. Sin embargo, el nucleo de Django cuenta de forma nativa con todas las herramientas necesarias para procesar solicitudes HTTP, estructurar endpoints RESTful y retornar respuestas en formato JSON.

Para implementar este comportamiento de manera limpia y mantenible, se utilizan las Vistas Basadas en Clases (Class-Based Views o CBV) heredando de `django.views.View`. Una CBV permite desacoplar la logica de cada verbo HTTP en metodos independientes dentro de una misma clase (`get`, `post`, `put`, `delete`), evitando estructuras condicionales extensas (`if request.method == 'GET'`) y facilitando la reutilizacion de codigo.

## 2. Los Cuatro Verbos HTTP y su Relacion con CRUD

El protocolo HTTP define un conjunto de metodos o verbos que indican la accion deseada sobre un recurso. En una arquitectura REST nativa, estos verbos se mapean directamente con las operaciones fundamentales de persistencia de datos (CRUD):

| Verbo HTTP | Operacion CRUD | Metodo en la Vista | Descripcion y Caso de Uso | Codigo HTTP Tipico |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | Read (Consultar) | `get(self, request, pk=None)` | Consulta y recupera informacion de los recursos sin alterar el estado del servidor. Se utiliza para listar todos los registros o para consultar el detalle de un registro especifico a traves de su identificador (`pk`). | 200 OK / 404 Not Found |
| **POST** | Create (Crear) | `post(self, request)` | Envia datos en el cuerpo de la peticion (`request.body`) para crear un nuevo registro en la base de datos. Se valida la presencia de los campos requeridos y se almacena la nueva entidad. | 201 Created / 400 Bad Request |
| **PUT** | Update (Actualizar) | `put(self, request, pk)` | Envia informacion actualizada para modificar un recurso existente identificado por su clave primaria (`pk`). Permite sustituir o actualizar los valores de los atributos del modelo. | 200 OK / 400 Bad Request / 404 Not Found |
| **DELETE** | Delete (Eliminar) | `delete(self, request, pk)` | Solicita la eliminacion fisica o logica del recurso identificado por su `pk`. Si el registro existe, se elimina de la base de datos y se notifica el resultado. | 200 OK / 404 Not Found |

## 3. Modulos, Funciones y Decoradores de Django Utilizados

Para la implementacion de los endpoints nativos se emplean los siguientes componentes de la biblioteca estandar de Python y del nucleo de Django:

### Modulo `json` (Biblioteca estandar de Python)
* **`json.loads()`**: Funcion utilizada para deserializar la cadena de texto o bytes que viaja en `request.body` y transformarla en un diccionario de Python, permitiendo acceder a los campos enviados en peticiones POST y PUT.
* **`json.JSONDecodeError`**: Excepcion capturada para manejar de forma segura los casos en que el cliente envia un cuerpo con formato JSON invalido, retornando un error HTTP 400 en lugar de provocar un fallo interno del servidor.

### Modulo `django.views`
* **`View`**: Clase base de Django para vistas basadas en clases. Proporciona el mecanismo de despacho (`dispatch`) que inspecciona el metodo HTTP de la solicitud entrante y redirige la ejecucion automaticamente al metodo correspondiente de la clase (`get`, `post`, `put`, `delete`).

### Modulo `django.http`
* **`JsonResponse`**: Subclase de `HttpResponse` especializada en serializar diccionarios de Python a formato JSON, configurando automaticamente la cabecera `Content-Type: application/json`. Acepta el parametro `status` para emitir codigos de estado HTTP semanticos (200, 201, 400, 404) y el parametro `safe=False` cuando se serializan listas en lugar de diccionarios.

### Modulo `django.views.decorators.csrf`
* **`csrf_exempt`**: Decorador que exime a una vista de la validacion del token CSRF. En aplicaciones web tradicionales donde el navegador procesa formularios HTML, el token CSRF es obligatorio. No obstante, en endpoints de API consumidos mediante JSON por clientes externos (Postman, aplicaciones moviles o frontend desacoplado), se requiere eximir la vista para permitir solicitudes POST, PUT y DELETE sin dicho token.

### Modulo `django.utils.decorators`
* **`method_decorator`**: Utilidad que permite transformar decoradores disenados para vistas basadas en funciones (FBV) y aplicarlos sobre clases o metodos de vistas basadas en clases (CBV). Al aplicarlo con `@method_decorator(csrf_exempt, name='dispatch')`, se protege o exime todo el ciclo de resolucion de la vista.

### Modulo `django.urls`
* **`path`**: Funcion de enrutamiento que define la estructura de las URLs del sistema. En conjunto con el metodo `as_view()` de la clase `ProyectoView`, conecta la ruta declarada con la logica ejecutable del endpoint, permitiendo capturar parametros dinamicos en la ruta como `<int:pk>`.

## 4. Codigo Fuente Implementado

### `gestion/views.py`

```python
import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Proyecto

@method_decorator(csrf_exempt, name='dispatch')
class ProyectoView(View):

    def get(self, request, pk=None):
        if pk is not None:
            proyecto = Proyecto.objects.filter(pk=pk).first()
            if not proyecto:
                return JsonResponse({'error': 'Proyecto no encontrado'}, status=404)
            data = {
                'id': proyecto.id,
                'nombre': proyecto.nombre,
                'descripcion': proyecto.descripcion,
                'fecha_inicio': str(proyecto.fecha_inicio)
            }
            return JsonResponse(data, status=200)

        proyectos = list(Proyecto.objects.values('id', 'nombre', 'descripcion', 'fecha_inicio'))
        for p in proyectos:
            p['fecha_inicio'] = str(p['fecha_inicio'])
        return JsonResponse(proyectos, safe=False, status=200)

    def post(self, request):
        try:
            datos = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Cuerpo JSON invalido'}, status=400)

        nombre = datos.get('nombre')
        descripcion = datos.get('descripcion')
        fecha_inicio = datos.get('fecha_inicio')

        if not nombre or not descripcion or not fecha_inicio:
            return JsonResponse({'error': 'Faltan campos obligatorios: nombre, descripcion, fecha_inicio'}, status=400)

        try:
            proyecto = Proyecto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio
            )
            data = {
                'id': proyecto.id,
                'nombre': proyecto.nombre,
                'descripcion': proyecto.descripcion,
                'fecha_inicio': str(proyecto.fecha_inicio)
            }
            return JsonResponse(data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, pk):
        proyecto = Proyecto.objects.filter(pk=pk).first()
        if not proyecto:
            return JsonResponse({'error': 'Proyecto no encontrado'}, status=404)

        try:
            datos = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Cuerpo JSON invalido'}, status=400)

        if 'nombre' in datos:
            proyecto.nombre = datos['nombre']
        if 'descripcion' in datos:
            proyecto.descripcion = datos['descripcion']
        if 'fecha_inicio' in datos:
            proyecto.fecha_inicio = datos['fecha_inicio']

        try:
            proyecto.save()
            data = {
                'id': proyecto.id,
                'nombre': proyecto.nombre,
                'descripcion': proyecto.descripcion,
                'fecha_inicio': str(proyecto.fecha_inicio)
            }
            return JsonResponse(data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, pk):
        proyecto = Proyecto.objects.filter(pk=pk).first()
        if not proyecto:
            return JsonResponse({'error': 'Proyecto no encontrado'}, status=404)

        proyecto.delete()
        return JsonResponse({'mensaje': f'Proyecto con id {pk} eliminado correctamente'}, status=200)
```

### `gestion/urls.py`

```python
from django.urls import path
from .views import ProyectoView

urlpatterns = [
    path('proyectos/', ProyectoView.as_view()),
    path('proyectos/<int:pk>/', ProyectoView.as_view()),
]
```

### `backend/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gestion.urls')),
]
```

## 5. Pruebas de los Endpoints

Con el servidor ejecutandose mediante `python manage.py runserver`, las rutas disponibles son:

* Listar proyectos: `GET http://127.0.0.1:8000/api/proyectos/`
* Consultar detalle de proyecto: `GET http://127.0.0.1:8000/api/proyectos/1/`
* Crear nuevo proyecto: `POST http://127.0.0.1:8000/api/proyectos/`
* Actualizar proyecto existente: `PUT http://127.0.0.1:8000/api/proyectos/1/`
* Eliminar proyecto: `DELETE http://127.0.0.1:8000/api/proyectos/1/`

## 6. Fuentes Consultadas

* Documentacion Oficial de Django · Class-Based Views:  
  https://docs.djangoproject.com/en/5.1/topics/class-based-views/intro/
* Documentacion Oficial de Django · Request and Response Objects (`JsonResponse`):  
  https://docs.djangoproject.com/en/5.1/ref/request-response/#jsonresponse-objects
* Documentacion Oficial de Django · CSRF Protection (`csrf_exempt` y `method_decorator`):  
  https://docs.djangoproject.com/en/5.1/topics/class-based-views/intro/#decorating-the-class
* Documentacion Oficial de Python · Modulo `json`:  
  https://docs.python.org/3/library/json.html
* MDN Web Docs · Metodos de peticion HTTP:  
  https://developer.mozilla.org/es/docs/Web/HTTP/Methods
