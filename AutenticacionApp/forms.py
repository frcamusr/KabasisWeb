from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Empresa  # Importa tu modelo personalizado

class CustomUserCreationForm(UserCreationForm):

    tipo_usuario = forms.ChoiceField(
        choices=CustomUser.TIPO_USUARIO_CHOICES,
        label="Tipo de Usuario",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select'}),
    )

    # Nuevo campo para la imagen de perfil
    profile_picture = forms.ImageField(
        required=False,  # Esto permite que el campo sea opcional
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        label="Imagen de Perfil"
    )


    nombre_empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),  # Queryset para obtener todas las empresas
        label="Empresa",
        required=False,  # Puede ser opcional si lo prefieres
        widget=forms.Select(attrs={'class': 'custom-select'}),
    )


    class Meta:
        model = CustomUser  # Usa tu modelo personalizado en lugar de User
        fields = ['username', 'tipo_usuario', 'first_name', 'last_name', 'nombre_empresa', 'profile_picture', 'email', 'password1', 'password2']



class UserProfileForm(forms.ModelForm):

    

    class Meta:
        model = CustomUser
        fields = ['username', 'tipo_usuario',  'profile_picture', 'first_name', 'last_name', 'email']


class EmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = ['nombre_empresa', 'descripcion',  'numero_empleados', 'estado_cuenta']


    def __init__(self, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  # Agregar la clase 'form-control' a cada campo

            if field_name == 'nombre_empresa':
                field.widget.attrs['placeholder'] = 'Nombre de la empresa'  # Agregar un marcador de posición para el campo 'nombre'


from django import forms

class CSVUploadForm(forms.Form):
    archivo_csv = forms.FileField()
