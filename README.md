# Taller Peticiones en Django

Materia: Desarrollo de Aplicaciones Web I  
Docente: Jose Javier Torres  
Estudiante: Luis Narvaez  

## 1. Endpoints en Django nativo

Para este taller se pidio crear endpoints usando Django basico, sin instalar Django REST Framework ni librerias externas. 

Django permite manejar peticiones HTTP y responder en formato JSON directamente. Para organizar el codigo usamos una vista basada en clase heredando de View (`class ProyectoView(View)`). Esto permite separar cada verbo HTTP en su propia funcion (`get`, `post`, `put`, `delete`) dentro de la misma clase, sin tener que llenar una sola funcion de condicionales con `if request.method == 'GET'`.

## 2. Verbos HTTP y su relacion con CRUD

Los cuatro verbos solicitados se conectan con las operaciones basicas de base de datos (CRUD):

* **GET (Read - Consultar):** Lo usamos para consultar la informacion. Si no se pasa ningun id, devuelve la lista de todos los proyectos guardados. Si se pasa un id en la URL (`/proyectos/1/`), busca ese proyecto especifico y lo devuelve en JSON. Si no existe, retorna error 404.
* **POST (Create - Crear):** Lo usamos para registrar un nuevo proyecto. Lee los datos en formato JSON que vienen en el cuerpo de la peticion (`request.body`), valida que no falten campos (`nombre`, `descripcion`, `fecha_inicio`) y guarda el registro con codigo 201.
* **PUT (Update - Actualizar):** Lo usamos para modificar un proyecto existente pasandole el id. Lee los datos nuevos, actualiza los campos del modelo y guarda los cambios devolviendo codigo 200.
* **DELETE (Delete - Eliminar):** Lo usamos para borrar un proyecto por su id. Si lo encuentra, lo elimina de la base de datos y confirma la eliminacion.

## 3. Modulos, funciones y decoradores utilizados

* **json (libreria de Python):** Se utiliza `json.loads(request.body)` para convertir el texto JSON que envia el cliente en un diccionario de Python y poder leer sus campos.
* **View (django.views):** Es la clase base de Django para vistas basadas en clases. Se encarga de recibir la peticion y llamar automaticamente al metodo que coincida con el verbo (`get`, `post`, etc.).
* **JsonResponse (django.http):** Se usa para retornar la respuesta al cliente en formato JSON con su codigo de estado HTTP (200, 201, 400 o 404) y el encabezado `application/json`.
* **csrf_exempt (django.views.decorators.csrf):** Desactiva la verificacion del token CSRF en esta vista, ya que las peticiones se prueban desde programas como Postman o cURL y no desde un formulario web tradicional de Django.
* **method_decorator (django.utils.decorators):** Permite aplicar el decorador `csrf_exempt` a una vista basada en clase sobre el metodo `dispatch`.
* **path (django.urls):** Permite registrar las rutas en `urls.py` usando `ProyectoView.as_view()`, tanto para la ruta general como para la ruta que recibe el id del proyecto (`<int:pk>`).

## 4. Archivos modificados

* **gestion/views.py:** Se creo la clase `ProyectoView` con las funciones `get`, `post`, `put` y `delete`.
* **gestion/urls.py:** Se crearon las rutas `/proyectos/` y `/proyectos/<int:pk>/`.
* **backend/urls.py:** Se incluyeron las rutas de la aplicacion con `path('api/', include('gestion.urls'))`.

## 5. Como probar los endpoints

Con el servidor iniciado mediante `python manage.py runserver`, las rutas para probar son:

* Listar proyectos: GET http://127.0.0.1:8000/api/proyectos/
* Ver un proyecto: GET http://127.0.0.1:8000/api/proyectos/1/
* Crear proyecto: POST http://127.0.0.1:8000/api/proyectos/
* Actualizar proyecto: PUT http://127.0.0.1:8000/api/proyectos/1/
* Eliminar proyecto: DELETE http://127.0.0.1:8000/api/proyectos/1/

## 6. Fuentes consultadas

* Documentacion oficial de Django sobre Class-Based Views:  
  https://docs.djangoproject.com/en/5.1/topics/class-based-views/intro/
* Documentacion de JsonResponse:  
  https://docs.djangoproject.com/en/5.1/ref/request-response/#jsonresponse-objects
* Uso de decoradores en vistas basadas en clase:  
  https://docs.djangoproject.com/en/5.1/topics/class-based-views/intro/#decorating-the-class
* Metodos de peticion HTTP en MDN Web Docs:  
  https://developer.mozilla.org/es/docs/Web/HTTP/Methods
