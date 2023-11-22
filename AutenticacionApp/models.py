from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    TIPO_USUARIO_CHOICES = (
        ('', 'Selecciona el tipo de usuario'),  # Opción en blanco
        ('Editor_contenido', 'Editor de contenido'),
        ('Revisor', 'Revisor'),
        ('Estudiante', 'Estudiante'),
        ('Visualizador', 'Visualizador'),
        ('Reporteria', 'Reporteria'),
        ('Administrador_empresa', 'Administrador empresa'),
    )

    tipo_usuario = models.CharField(
        max_length=50,
        choices=TIPO_USUARIO_CHOICES,
        default='',
        blank=True,
        verbose_name="Tipo de Usuario"
    )
    
    # Nuevo campo para la imagen de perfil
    profile_picture = models.ImageField(
        upload_to='usuarios/',  # Define la carpeta donde se guardarán las imágenes
        null=True,
        blank=True,
        verbose_name="Imagen de Perfil"
    )

    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuario Personalizado"
        verbose_name_plural = "Usuarios Personalizados"

    


class Empresa(models.Model):
    nombre_empresa = models.CharField(max_length=50)
    descripcion = models.TextField()
    numero_empleados = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    ESTADOS_DE_CUENTA = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        # Puedes añadir más estados aquí
    ]

    estado_cuenta = models.CharField(max_length=20, choices=ESTADOS_DE_CUENTA, default='Activo')

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nombre_empresa