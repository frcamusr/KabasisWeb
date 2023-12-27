from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import cerrar_sesion, registro



urlpatterns = [

    path('cerrar_sesion',cerrar_sesion, name="cerrar_sesion"),
    


    path('', registro, name= "registro"),

    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),


    path('usuarios_personalizados/', views.lista_usuarios_personalizados, name='lista_usuarios_personalizados'),
    path('usuarios_personalizados/crear/', views.crear_usuario_personalizado, name='crear_usuario_personalizado'),
    path('usuarios_personalizados/<int:id_usuario>/actualizar/', views.actualizar_usuario_personalizado, name='actualizar_usuario_personalizado'),
    path('usuarios_personalizados/<int:id_usuario>/eliminar/', views.eliminar_usuario_personalizado, name='eliminar_usuario_personalizado'),


    path('menu_administracion/', views.menu_administracion, name='menu_administracion'),

    ###empresas##
    path('empresas/', views.listar_empresa, name='listar_empresa'),
    path('empresas/crear_empresa/', views.crear_empresa, name='crear_empresa'),
    path('empresas/<int:id>/actualizar/', views.actualizar_empresa, name='actualizar_empresa'),
    path('empresas/<int:id>/eliminar/', views.eliminar_empresa, name='eliminar_empresa'),

    ##carga de usuarios masivo##
    path('carga_masiva/', views.carga_masiva, name='carga_masiva'),

    ##Invitación por email
    path('invitacion_email/', views.invitacion_email, name='invitacion_email'),

    path('form_invitacion/', views.form_invitacion, name='form_invitacion'),


    
    


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL[1:], document_root=settings.MEDIA_ROOT)
