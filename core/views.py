from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario


def bienvenida(request):
    return render(request, 'bienvenida.html')


@csrf_exempt
def usuarios_lista(request):
    if request.method == "GET":
        nombre_query = request.GET.get("nombre")
        if nombre_query:
            usuarios = Usuario.objects.filter(nombre__icontains=nombre_query)
        else:
            usuarios = Usuario.objects.all()
        
        resultado = [usuario.to_dict() for usuario in usuarios]
        return JsonResponse(resultado, safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        nombre = data.get("nombre")
        email = data.get("email")
        rol = data.get("rol", "invitado")

        if not nombre or not email:
            return JsonResponse({"error": "nombre y email son requeridos"}, status=400)

        # Validar que el email no exista
        if Usuario.objects.filter(email=email).exists():
            return JsonResponse({"error": "El email ya está registrado"}, status=400)

        usuario = Usuario.objects.create(nombre=nombre, email=email, rol=rol)
        return JsonResponse(usuario.to_dict(), status=201)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def usuarios_detalle(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    if request.method == "GET":
        return JsonResponse(usuario.to_dict())

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        if "nombre" in data:
            usuario.nombre = data["nombre"]
        if "email" in data:
            # Validar que el nuevo email no exista en otro usuario
            if Usuario.objects.filter(email=data["email"]).exclude(id=usuario_id).exists():
                return JsonResponse({"error": "El email ya está registrado"}, status=400)
            usuario.email = data["email"]
        if "rol" in data:
            usuario.rol = data["rol"]

        usuario.save()
        return JsonResponse(usuario.to_dict())

    elif request.method == "DELETE":
        usuario.delete()
        return JsonResponse({"mensaje": "Usuario eliminado correctamente"}, status=200)

    return JsonResponse({"error": "Método no permitido"}, status=405)