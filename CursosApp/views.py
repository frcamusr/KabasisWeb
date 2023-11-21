from django.shortcuts import render, redirect, get_object_or_404

from .forms import CursoForm, UnidadForm, VideoForm

from .models import Curso, UnidadCurso

from django.contrib import messages


from django.shortcuts import render, HttpResponse
from CursosApp.models import Curso, UnidadCurso
from django.http import JsonResponse
# importar los modelos de la app SurveyApp

# Create your views here.

def cursos(request):
    cursos = Curso.objects.all()
    data = {

        'cursos': cursos
    }
    return render(request, "CursosApp/cursos.html", data)

def agregar_curso(request):

    data = {
        'form': CursoForm()

    }

    if request.method == 'POST':
        formulario = CursoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Curso creado con éxito.')
        else: 
            data["form"] = formulario
    
    return render(request, "CursosApp/agregar_curso.html", data)

def listar_curso(request):
    cursos = Curso.objects.all()

    data = {
        'cursos': cursos
    }

    return render(request, "CursosApp/listar_curso.html", data)


def modificar_curso(request, id):

    curso = get_object_or_404(Curso, id=id)

    data= {
        'form': CursoForm(instance = curso)
    }

    if request.method == 'POST':
        formulario = CursoForm(data=request.POST, instance=curso, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Curso actualizado correctamente")
            return redirect(to="listar_curso")
        
        data["form"] = formulario
    
    return render(request, "CursosApp/modificar_curso.html", data)

def eliminar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    curso.delete()
    messages.success(request, 'Curso eliminado con éxito.')
    return redirect(to="listar_curso")



def ver_curso(request, id):
    curso = Curso.objects.get(pk=id)
    unidades = UnidadCurso.objects.filter(curso=curso).order_by('orden')
    
    data = {
        'curso': curso,
        'unidades': unidades,
    }
    
    return render(request, 'CursosApp/ver_curso.html', data)



############################## UNIDADES ######################################

from .forms import UnidadForm

def agregar_unidad(request):
    if request.method == 'POST':
        formulario = UnidadForm(request.POST, request.FILES)
        if formulario.is_valid():
            unidad = formulario.save(commit=False)  # No guardar inmediatamente para asignar curso
            curso_id = request.POST.get('curso')  # Asumiendo que el campo del formulario se llama 'curso'
            curso = Curso.objects.get(pk=curso_id)  # Obtén el curso correspondiente desde la base de datos
            # Concatenar el nombre del curso al título de la unidad
            unidad.titulo = f"{curso.nombre} - {unidad.titulo}"
            unidad.curso = curso  # Asignar el curso al que pertenece esta unidad
            unidad.save()  # Ahora guarda la unidad con el curso asignado y el nombre modificado
            messages.success(request, 'Unidad creada con éxito.')
            formulario = UnidadForm() 
        else:
            messages.error(request, 'Error al crear la unidad. Por favor, verifica el formulario.')
    else:
        formulario = UnidadForm()

    data = {'form': formulario}
    return render(request, "unidades/agregar_unidad.html", data)

    
def listar_unidad(request, id):
    curso = Curso.objects.get(pk=id)
    unidades = UnidadCurso.objects.filter(curso=curso).order_by('orden')
    
    data = {
        'curso': curso,
        'unidades': unidades,
    }
    
    return render(request, 'unidades/listar_unidad.html', data)


def eliminar_unidad(request, id):
    unidad = get_object_or_404(UnidadCurso, pk=id)
    curso_id = unidad.curso.id  # Obtiene el ID del curso al que pertenece la unidad
    unidad.delete()
    
    # Modifica la siguiente línea para pasar el ID correctamente
    return redirect('listar_unidad', id=curso_id)




def modificar_unidad(request, id):
    unidad = get_object_or_404(UnidadCurso, id=id)
    curso_id = unidad.curso.id  # Obtiene el ID del curso al que pertenece la unidad

    data = {
        'form': UnidadForm(instance=unidad)
    }

    if request.method == 'POST':
        formulario = UnidadForm(data=request.POST, instance=unidad, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Unidad actualizada correctamente")
            
            # Redirige a la vista 'listar_unidad' con el ID del curso como parámetro
            return redirect('listar_unidad', id=curso_id)

        data["form"] = formulario

    return render(request, "unidades/modificar_unidad.html", data)


from .models import Video

def ver_videos(request, unidad_id):
    videos = Video.objects.filter(unidad_id=unidad_id)
    return render(request, 'video/ver_videos.html', {'videos': videos})


#################CONTENIDO#################




from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import QuestionForm, AnswerForm
from .models import QuestionContent, AnswerContent, QuizContent
from django.contrib.auth.decorators import login_required
from django.urls import reverse




# Preguntas: crear, eliminar y actualizar
def create_question(request, id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Crear una nueva instancia de Question y asignar el quiz
            question = QuestionContent(quiz_id=id)
            question.question_type = form.cleaned_data['question_type']
            question.text = form.cleaned_data['text']
            question.option_a = form.cleaned_data['option_a']
            question.option_b = form.cleaned_data['option_b']
            question.option_c = form.cleaned_data['option_c']
            question.option_d = form.cleaned_data['option_d']
            question.correct_answer = form.cleaned_data['correct_answer']
            question.save()
            # Redirigir a la página del quiz
            return redirect(reverse('listar_quiz', args=[id]))
    else:
        form = QuestionForm()
    return render(request, 'crear_pregunta.html', {'form': form, 'id_quiz': id})



def delete_question(request, id):
    question = QuestionContent.objects.get(quiz_id=id)

    question.delete()
    return redirect(reverse('listar_quiz', args=[id]))


# def update_question, este tendra un formulario para actualizar la pregunta
def update_question(request, id):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        question = QuestionContent.objects.get(quiz_id=id)
        tipo = question.question_type

        if form.is_valid():
            # guardar la pregunta y sus opciones, usando el id de la pregunta

            if tipo == 'text':
                #form = QuestionForm(initial={'text': question.text})
                # guardar las preguntas con el formulario de texto
                question.text = form.cleaned_data['text']
                question.save()
                return redirect(reverse('listar_quiz', args=[id]))

            else:
                #form = QuestionForm(initial={'text': question.text, 'option_a': question.option_a, 'option_b': question.option_b, 'option_c': question.option_c, 'option_d': question.option_d, 'correct_answer': question.correct_answer})

                question.text = form.cleaned_data['text']
                question.option_a = form.cleaned_data['option_a']
                question.option_b = form.cleaned_data['option_b']
                question.option_c = form.cleaned_data['option_c']
                question.option_d = form.cleaned_data['option_d']
                question.correct_answer = form.cleaned_data['correct_answer']
                question.save()
                return redirect(reverse('listar_quiz', args=[id]))
        else:
            if tipo == 'text':
                form = QuestionForm(initial={'text': question.text})
            else:
                form = QuestionForm(initial={'text': question.text, 'option_a': question.option_a, 'option_b': question.option_b, 'option_c': question.option_c, 'option_d': question.option_d, 'correct_answer': question.correct_answer})
        
   
    return render(request, 'update_question.html', {'form': form, 'question': question, 'tipo': tipo})



# mostrar los enlaces de todos los quiz creados para cada unidad y curso:
def listar_material(request, idCurso, unidad):
    quizzes = QuizContent.objects.filter(curso_id=idCurso, unidad_id=unidad)
    # agregar variable para texto y video


    idCurso = idCurso
    unidad = unidad


    return render(request, 'listar_material.html', {'quizzes': quizzes, 'idCurso': idCurso, 'unidad': unidad})




#Quiz: crear, editar, eliminar y listar

def crear_quiz(request, idCurso, unidad):
    # creamos el quiz sin formulario directamente en la vista usando el modelo Quiz y idCurso y unidad como parametros
    quiz = QuizContent()
    quiz.curso_id = idCurso
    quiz.unidad_id = unidad
    quiz.save()
    # redireccionamos a listar_contenido
    return redirect(reverse('listar_material', args=[idCurso, unidad]))

# edit_quiz solo envia a la lista de quiz
def edit_quiz(request, id):
    quiz = QuizContent.objects.get(id=id)
    idCurso = quiz.curso_id
    unidad = quiz.unidad_id
    return redirect(reverse('listar_quiz', args=[quiz.id]))

# Eliminar quiz y sus preguntas
def delete_quiz(request, id):
    quiz = QuizContent.objects.get(id=id)
    quiz.delete()
    return redirect(reverse('listar_material', args=[quiz.curso_id, quiz.unidad_id]))

def listar_quiz(request, id):
    quiz = QuizContent.objects.get(id=id)
    idCurso = quiz.curso_id
    unidad = quiz.unidad_id
    questions = QuestionContent.objects.filter(quiz_id=id)
    return render(request, 'listar_quiz.html', {'questions': questions, 'quiz':quiz ,'idCurso': idCurso, 'unidad': unidad})





def create_question2(request, id): ##pertenece a la actividad?
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():

            # Crear una nueva instancia de Question sin ningun parametro
            question = QuestionContent()
            question.question_type = form.cleaned_data['question_type']
            question.text = form.cleaned_data['text']
            question.option_a = form.cleaned_data['option_a']
            question.option_b = form.cleaned_data['option_b']
            question.option_c = form.cleaned_data['option_c']
            question.option_d = form.cleaned_data['option_d']
            question.correct_answer = form.cleaned_data['correct_answer']
            question.save()
            # Obtener la instancia de la actividad
            
            # Agregar la pregunta a la lista de preguntas de la actividad
            

            # Redirigir a la página del listar actividades
            return redirect(reverse('listar_actividad', args=[id]))

    else:
        form = QuestionForm()
    return render(request, 'crear_pregunta.html', {'form': form, 'id': id})



@login_required 
def formulario(request, idCurso, unidad):
    # Obtener todas las preguntas
    questions = QuestionContent.objects.filter(curso_id=idCurso, unidad_id=unidad)
    if request.method == 'POST':
        
        for pregunta in questions:
            question_id = request.POST.get(f'question_id_{pregunta.id}')
            text_answer = request.POST.get(f'text_answer_{pregunta.id}')
            option_answer = request.POST.get(f'option_answer_{pregunta.id}')
            # if form.is_valid():
            # Guardar la respuesta
            answer = AnswerContent()
            # answer question es id de la pregunta
            answer.question = QuestionContent.objects.get(id=question_id)
            # answer user es el usuario que esta respondiendo la pregunta
            answer.user = request.user
            answer.text_answer = text_answer
            # answer option_answer es la opcion que el usuario selecciono, puede ser null
            # si es nulo y por lo tanto diferente de a, b, c, d, entonces no se guarda
            if option_answer in ['a', 'b', 'c', 'd']:
                answer.option_answer = option_answer

            answer.save()



        return redirect('agradecimientos')
    else:
        form = AnswerForm()

    return render(request, 'formulario.html', {'form': form, 'questions': questions})



# def agradecimientos, este tendra un mensaje de agradecimiento por haber respondido la encuesta
def agradecimientos(request):
    return render(request, 'agradecimientos.html')



def editContenido(request):
    cursos = Curso.objects.all()
    Unidad = UnidadCurso.objects.all()
    
    data = {

        'cursos': cursos,
        'unidad': Unidad,
    }
    return render(request, "admContenido/editContenido.html" , data)

def obtener_unidades(request, curso_id):
    unidades = UnidadCurso.objects.filter(curso_id=curso_id).values('id','titulo')
    curso_nombre = Curso.objects.get(id=curso_id).nombre
    
    data = {
        'cursoNombre': curso_nombre,
        'unidades': list(unidades)
    }
    
    return JsonResponse(data)


# por cada unidad y curso enlistar los contenidos, quiz, videos y actividades desde la base de datos y modelos
def obtener_contenido(request, unidad_id):
    # obtener el contenido de la unidad
    # obtener los videos de la unidad
    # obtener los quiz de la unidad
    quiz = QuizContent.objects.filter(unidad_id=unidad_id).values('id','question_id')
    # listar lo anterior para mostrarlo en la vista
    data = {
        
        'quiz': list(quiz),
    }
    # retornar la data en formato json para que pueda ser leida por javascript
    return JsonResponse(data)



############Video######################

def agregar_video(request):
    if request.method == 'POST':
        formulario = VideoForm(request.POST, request.FILES)
        if formulario.is_valid():
            video = formulario.save(commit=False)  # No guardar inmediatamente para asignar curso
            unidad_id = request.POST.get('unidad')  # Asumiendo que el campo del formulario se llama 'curso'
            unidad = UnidadCurso.objects.get(pk=unidad_id)  # Obtén el curso correspondiente desde la base de datos
            # Concatenar el nombre del curso al título de la unidad
            video.titulo = f"{unidad.titulo} - {video.titulo}"
            video.unidad = unidad  # Asignar el curso al que pertenece esta unidad
            video.save()  # Ahora guarda la unidad con el curso asignado y el nombre modificado
            messages.success(request, 'video creado con éxito.')
            formulario = VideoForm() 
        else:
            messages.error(request, 'Error al crear el video. Por favor, verifica el formulario.')
    else:
        formulario = VideoForm()

    data = {'form': formulario}
    return render(request, "video/agregar_video.html", data)



from .models import Curso, UnidadCurso, Video

def listar_video(request, id=None):
    if id:
        videos = Video.objects.filter(unidad__curso_id=id)
    else:
        videos = Video.objects.all()

    data = {
        'videos': videos,
    }

    return render(request, 'video/listar_video.html', data)



def eliminar_video(request, id):
    video = get_object_or_404(Video, pk=id)
    unidad_id = video.unidad.id  # Obtiene el ID del curso al que pertenece la unidad
    video.delete()
    messages.success(request, "video eliminado correctamente")
    # Modifica la siguiente línea para pasar el ID correctamente
    return redirect('listar_video', id=unidad_id)




def modificar_video(request, id):
    video = get_object_or_404(Video, id=id)
    unidad_id = video.unidad.id  # Obtiene el ID del curso al que pertenece la unidad

    data = {
        'form': VideoForm(instance=video)
    }

    if request.method == 'POST':
        formulario = VideoForm(data=request.POST, instance=video, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Video actualizado correctamente")
            
            # Redirige a la vista 'listar_unidad' con el ID del curso como parámetro
            return redirect('listar_video', id=unidad_id)

        data["form"] = formulario

    return render(request, "video/modificar_video.html", data)
