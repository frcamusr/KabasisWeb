from django.urls import path

from CursosApp import views

urlpatterns = [
    
    path('',views.cursos, name="Cursos"),
    
    path('agregar_curso/', views.agregar_curso, name="agregar_curso"),

    path('listar_curso/', views.listar_curso, name="listar_curso"),

    path('modificar_curso/<id>/', views.modificar_curso, name="modificar_curso"),

    path('eliminar_curso/<id>/', views.eliminar_curso, name="eliminar_curso"),

    path('ver_curso/<id>/', views.ver_curso, name='ver_curso'),



    path('agregar_unidad/', views.agregar_unidad, name="agregar_unidad"),

    path('listar_unidad/<id>/', views.listar_unidad, name="listar_unidad"),

    path('eliminar_unidad/<id>/', views.eliminar_unidad, name="eliminar_unidad"),

    path('modificar_unidad/<id>/', views.modificar_unidad, name="modificar_unidad"),



    path('ver_videos/<int:unidad_id>/', views.ver_videos, name='ver_videos'),




    ##Survey##

     # por el momento no uso este url:path('preguntas/', views.preguntas, name='preguntas'),


    # URL para Pregunta
    # crear pregunta solo usando el id del quiz
    path('crear_pregunta/<int:id>/', views.create_question, name='crear_pregunta'),  
    #crear pregunta usando la vista create_question2 y enviando el id de la actividad
    path('crear_pregunta2/<int:id>/', views.create_question2, name='crear_pregunta2'),


    path('delete_question/<int:id>/', views.delete_question, name='delete_question'),
    # actualizar pregunta usando el mismo formulario de crear pregunta
    path('update_question/<int:id>/', views.update_question, name='update_question'),    



    # URL para Quiz
    # path para crear_quiz
    path('crear_quiz/<int:idCurso>/<int:unidad>/', views.crear_quiz, name='crear_quiz'),
    # path para editar quiz
    path('editar_quiz/<int:id>/', views.edit_quiz, name='editar_quiz'),
    # path para eliminar quiz
    path('eliminar_quiz/<int:id>/', views.delete_quiz, name='eliminar_quiz'),
    # quiz con id como parametro para listar las preguntas
    path('listar_quiz/<int:id>/', views.listar_quiz, name='listar_quiz'),

 
    # Responder Usuario
    # formulario y agradecimientos
    path('formulario/<int:idCurso>/<int:unidad>/', views.formulario, name='formulario'),
    path('agradecimientos/', views.agradecimientos, name='agradecimientos'),


    #  path para listar todo el material de la unidad
    path('listar_material/<int:idCurso>/<int:unidad>/', views.listar_material, name='listar_material'),




    path('editContenido',views.editContenido, name="editContenido"),
    path('obtener_unidades/<int:curso_id>/', views.obtener_unidades, name="obtener_unidades"),



    path('agregar_video/', views.agregar_video, name="agregar_video"),

    path('listar_video/<id>/', views.listar_video, name="listar_video"),

    path('eliminar_video/<id>/', views.eliminar_video, name="eliminar_video"),

    path('modificar_video/<id>/', views.modificar_video, name="modificar_video"),


]

