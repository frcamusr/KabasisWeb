from django.db import models
from django.conf import settings

# Create your models here.

class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to="cursos", null=False, blank=False)
    descripcion = models.TextField(max_length=500)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nombre
    

# Modelo para la tabla de Unidades de un Curso
class UnidadCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField()

    def __str__(self):
        return self.titulo

# Modelo para la tabla de Videos relacionados con las unidades
from django.db import models
from urllib.parse import urlparse, parse_qs

class Video(models.Model):
    unidad = models.ForeignKey(UnidadCurso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    video_url = models.URLField()
    descripcion = models.TextField()

    #Función que transforma la url completa del video de youtube en una url embebida
    def get_embedded_url(self):
        video_id = self.get_video_id()
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return ""

    def get_video_id(self):
        url = urlparse(self.video_url)
        if 'v' in parse_qs(url.query):
            return parse_qs(url.query)['v'][0]
        return ""




##################################

class QuestionContent(models.Model):
    QUESTION_TYPES = [
        ('option', 'Opción múltiple'),
        ('text', 'Texto'),
    ]
    
    quiz = models.ForeignKey('QuizContent', on_delete=models.CASCADE, null=True)
    question_type = models.CharField(max_length=255, choices=QUESTION_TYPES)
    text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255, null=True)
    option_b = models.CharField(max_length=255, null=True)
    option_c = models.CharField(max_length=255, null=True)
    option_d = models.CharField(max_length=255, null=True)
    correct_answer = models.CharField(max_length=1, null=False)

    def __str__(self):
        return self.text
    
# crear el modelo Answer con los campos question, user, text_answer y option_answer
class AnswerContent(models.Model):
    id=models.AutoField(primary_key=True)
    question = models.ForeignKey(QuestionContent, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text_answer = models.CharField(max_length=255, null=True)
    #option answer puede ser nulo
    option_answer = models.CharField(max_length=1, null=True)
    def __str__(self):
        return self.id
    
# crear el modelo contenido con los campos id, titulo, contenido, unidad, curso y una relación uno a muchos entre unidad y contenido


class QuizContent(models.Model):
    #relacion uno a muchos entre question y quiz, además tiene los atributos id, question_id curso, unidad
    id=models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    unidad = models.ForeignKey(UnidadCurso, on_delete=models.CASCADE)
    def __str__(self):
        return self.id

    


