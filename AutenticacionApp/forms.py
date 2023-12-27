from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,Empresa  # Importa tu modelo personalizado


from django.shortcuts import render, redirect,  get_object_or_404
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

##Formulario creación de usuarios personalizados
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user', None)  # Obtener el usuario actual
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        

        # Filtrar las opciones de empresa si el usuario es un administrador
        if user and user.tipo_usuario == 'Administrador':
            self.fields['tipo_usuario'].choices = [
                ('Alumno', 'Alumno')  # Solo permitir la creación de usuarios del tipo "Alumno"
            ]
            self.fields['nombre_empresa'].queryset = Empresa.objects.filter(id=user.empresa_id)
        else:
            self.fields['nombre_empresa'].queryset = Empresa.objects.all()

    class Meta:
        model = CustomUser  # Usa tu modelo personalizado en lugar de User
        fields = ['email', 'username', 'tipo_usuario', 'first_name', 'last_name', 'profile_picture', 'password1', 'password2']


##tarjeta ver perfil##
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_picture', 'first_name', 'last_name',]

##formulario crear empresa
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


from django import forms
from .models import CustomUser

class CustomUserUpdateForm(forms.ModelForm):
    nombre_empresa = forms.CharField(required=False)  # Campo adicional para el nombre de la empresa

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'profile_picture', 'nombre_empresa']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)

        # Configurar el valor inicial para nombre_empresa si existe
        if self.instance and self.instance.empresa:
            self.fields['nombre_empresa'].initial = self.instance.empresa.nombre_empresa

        # Restringir la edición del campo nombre_empresa si el usuario actual no es 'Administrador Kabasis'
        if current_user and current_user.tipo_usuario != 'Administrador Kabasis':
            self.fields['nombre_empresa'].disabled = True

    def save(self, commit=True):
        user = super(CustomUserUpdateForm, self).save(commit=False)
        
        # Actualizar la empresa relacionada si es necesario
        empresa_nombre = self.cleaned_data.get('nombre_empresa')
        if empresa_nombre:
            empresa, created = Empresa.objects.get_or_create(nombre_empresa=empresa_nombre)
            user.empresa = empresa

        if commit:
            user.save()

        return user


from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Empresa  # Asegúrate de importar los modelos adecuados



class UserAndEmpresaForm(forms.ModelForm):
    # Tus campos de formulario van aquí
    email = forms.EmailField(label='Correo electrónico', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'}))
    username = forms.CharField(label='Nombre de usuario', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre de usuario'}))
    first_name = forms.CharField(label='Nombre', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'}))
    last_name = forms.CharField(label='Apellidos', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su apellido'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}), required=True)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Confirme su contraseña'}), required=True)
    nombre_empresa = forms.CharField(label='Nombre de la empresa', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de su empresa'}))
    descripcion = forms.CharField(label='Descripción', widget=forms.Textarea(attrs={'placeholder': 'Descripción de su empresa'}), required=True)
    numero_empleados = forms.IntegerField(label='Número de empleados', required=True, widget=forms.NumberInput(attrs={'placeholder': 'Número de empleados'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'profile_picture', 'password1', 'password2', 
                  'nombre_empresa', 'descripcion', 'numero_empleados']
        labels = {
            'email': 'Correo electrónico',
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
            'nombre_empresa': 'Nombre de la empresa',
            'descripcion': 'Descripción',
            'numero_empleados': 'Número de empleados',
            'profile_picture': 'Imagen de perfil',
        }

    
    def __init__(self, *args, **kwargs):
        super(UserAndEmpresaForm, self).__init__(*args, **kwargs)

        # Añadir instrucciones de contraseña
        self.fields['password1'].help_text = password_validators_help_text_html()


    def clean_nombre_empresa(self):
        nombre_empresa = self.cleaned_data.get('nombre_empresa')

        # Verificar si el nombre de la empresa ya está registrado
        if Empresa.objects.filter(nombre_empresa=nombre_empresa).exists():
            raise forms.ValidationError("Esta empresa ya está registrada.")

        # Cambiar la primera letra del nombre de la empresa a mayúscula
        if nombre_empresa:
            nombre_empresa = nombre_empresa.capitalize()  # Cambia la inicial a mayúscula

        return nombre_empresa

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden")

        # Llama al método clean_nombre_empresa y actualiza los datos limpios
        cleaned_data['nombre_empresa'] = self.clean_nombre_empresa()

        return cleaned_data

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        try:
            # Validar la fortaleza de la contraseña
            validate_password(password1, self.instance)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password1

    def save(self, commit=True):
        user = super(UserAndEmpresaForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        user.tipo_usuario = 'Administrador'

        if commit:
            empresa = Empresa(
                nombre_empresa=self.cleaned_data['nombre_empresa'],
                descripcion=self.cleaned_data['descripcion'],
                numero_empleados=self.cleaned_data['numero_empleados']
            )
            empresa.save()
            user.empresa = empresa
            user.save()
        
        return user

    

###Invitación por correo
    
from django import forms

class EmailInvitationForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Ingrese el correo electrónico del destinatario'}))


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Empresa
from django.contrib.auth.password_validation import password_validators_help_text_html


class UserAndEmpresaEmailForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'}))
    username = forms.CharField(label='Nombre de usuario', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre de usuario'}))
    first_name = forms.CharField(label='Nombre', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'}))
    last_name = forms.CharField(label='Apellidos', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su apellido'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}), required=True)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Confirme su contraseña'}), required=True)
    nombre_empresa = forms.CharField(label='Nombre de la empresa', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de su empresa'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'profile_picture', 'password1', 'password2', 'nombre_empresa']
        labels = {
            'email': 'Correo electrónico',
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
            'nombre_empresa': 'Nombre de la empresa',
            'profile_picture': 'Imagen de perfil',
        }

    def __init__(self, *args, **kwargs):
        self.empresa_id = kwargs.pop('empresa_id', None)
        super(UserAndEmpresaEmailForm, self).__init__(*args, **kwargs)
        if self.empresa_id:
            try:
                empresa = Empresa.objects.get(id=self.empresa_id)
                self.fields['nombre_empresa'].initial = empresa.nombre_empresa
                self.fields['nombre_empresa'].widget.attrs['readonly'] = True
            except Empresa.DoesNotExist:
                pass
        
        self.fields['password1'].help_text = password_validators_help_text_html()


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        # Asignar tipo_usuario a 'Alumno'
        user.tipo_usuario = 'Alumno'

        if self.empresa_id:
            user.empresa = Empresa.objects.get(id=self.empresa_id)

        if commit:
            user.save()
            # Si hay un archivo en profile_picture, guárdalo después de haber guardado el usuario
            if 'profile_picture' in self.files:
                user.profile_picture = self.files['profile_picture']
                user.save()  # Guarda de nuevo para almacenar la imagen

            self.save_m2m()  # Guarda las relaciones many-to-many si las hay

        return user

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        try:
            validate_password(password1, self.instance)
        except ValidationError as e:
            self.add_error('password1', e)
        return password1

    # No necesitas el método clean_nombre_empresa, si solo estás pre-cargando este campo

    
    