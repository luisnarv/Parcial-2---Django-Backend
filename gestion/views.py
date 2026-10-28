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
