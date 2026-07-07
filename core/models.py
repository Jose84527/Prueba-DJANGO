from django.db import models

class Usuario(models.Model):
    ROLES = [
        ('admin', 'Admin'),
        ('invitado', 'Invitado'),
    ]
    
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='invitado')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.email})"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol,
            "fecha_creacion": self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            "fecha_actualizacion": self.fecha_actualizacion.strftime("%Y-%m-%d %H:%M:%S"),
        }