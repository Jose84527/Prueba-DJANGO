from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def bienvenida(request):
    return render(request, 'Bienvenida.html')


# "Base de datos" en memoria
usuarios = [
    {"id": 1, "nombre": "Juan Perez", "email": "juan@example.com", "rol": "admin"},
    {"id": 2, "nombre": "Maria Lopez", "email": "maria@example.com", "rol": "admin"},
    {"id": 3, "nombre": "Carlos Ramirez", "email": "carlos@example.com", "rol": "invitado"},
    {"id": 4, "nombre": "Ana Torres", "email": "ana@example.com", "rol": "invitado"},
    {"id": 5, "nombre": "Luis Mendoza", "email": "luis@example.com", "rol": "invitado"},
]


def _siguiente_id():
    return max([u["id"] for u in usuarios], default=0) + 1


@csrf_exempt
def usuarios_lista(request):
    if request.method == "GET":
        nombre_query = request.GET.get("nombre")
        resultado = usuarios
        if nombre_query:
            resultado = [u for u in usuarios if nombre_query.lower() in u["nombre"].lower()]
        return JsonResponse(resultado, safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON invalido"}, status=400)

        nombre = data.get("nombre")
        email = data.get("email")
        rol = data.get("rol", "invitado")  # si no mandan rol, por defecto es invitado
        if not nombre or not email:
            return JsonResponse({"error": "nombre y email son requeridos"}, status=400)

        nuevo_usuario = {"id": _siguiente_id(), "nombre": nombre, "email": email, "rol": rol}
        usuarios.append(nuevo_usuario)
        return JsonResponse(nuevo_usuario, status=201)

    return JsonResponse({"error": "Metodo no permitido"}, status=405)


@csrf_exempt
def usuarios_detalle(request, usuario_id):
    usuario = next((u for u in usuarios if u["id"] == usuario_id), None)

    if usuario is None:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    if request.method == "GET":
        return JsonResponse(usuario)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON invalido"}, status=400)

        usuario["nombre"] = data.get("nombre", usuario["nombre"])
        usuario["email"] = data.get("email", usuario["email"])
        usuario["rol"] = data.get("rol", usuario["rol"])
        return JsonResponse(usuario)

    elif request.method == "DELETE":
        usuarios.remove(usuario)
        return JsonResponse({"mensaje": "Usuario eliminado"}, status=200)

    return JsonResponse({"error": "Metodo no permitido"}, status=405)