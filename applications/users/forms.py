# django
from django import forms
from django.contrib.auth import authenticate
#
from .models import User


class UserRegisterForm(forms.ModelForm):
    '''
        Formulario para el registro de usuarios
    '''

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'input-group-field',
            }
        )
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmar Contraseña',
                'class': 'input-group-field',
            }
        )
    )

    class Meta:
        """Form settings."""

        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'ocupation',
            'genero',
            'date_birth',
            'is_active',
            'is_staff',
            'is_superuser',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre de usuario',
                    'class': 'input-group-field',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Correo electrónico',
                    'class': 'input-group-field',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'placeholder': 'Nombres',
                    'class': 'input-group-field',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'placeholder': 'Apellidos',
                    'class': 'input-group-field',
                }
            ),
            'genero': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'date_birth': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
            'is_staff': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
            'is_superuser': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }

    def clean_password2(self):
        """Password verification."""
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'La contraseña no coincide')

    # def save(self):
    #     """Save method."""
    #     data = self.cleaned_data
    #     data.pop('password2')
    #     user = User.objects.create_user(**data)
    #     return user
    
    
class LoginForm(forms.Form):
    """Login form."""
    username = forms.CharField(
        label='Nombre de usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre de usuario',
                'class': 'input-group-field',
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'input-group-field',
            }
        )
    )

    def clean(self):
        """Verify credentials."""
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data['username']
        password = cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')
        return self.cleaned_data
    
    
class UserUpdateForm(forms.ModelForm):
    '''
        Formulario para el registro de usuarios
    '''

    class Meta:
        """Form settings."""

        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'ocupation',
            'genero',
            'date_birth',
            'is_active',
            'is_staff',
            'is_superuser',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre de usuario',
                    'class': 'input-group-field',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Correo electrónico',
                    'class': 'input-group-field',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'placeholder': 'Nombres',
                    'class': 'input-group-field',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'placeholder': 'Apellidos',
                    'class': 'input-group-field',
                }
            ),
            'ocupation': forms.TextInput(
                attrs={
                    'placeholder': 'Ocupación',
                    'class': 'input-group-field',
                }
            ),
            'genero': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'date_birth': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
            'is_staff': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
            'is_superuser': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }
        
        
class UpdatePasswordForm(forms.Form):
    """Update password form."""
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña actual',
                # 'class': 'input-group-field',
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña nueva',
                'class': 'input-group-field',
            }
        )
    )
    password3 = forms.CharField(
        label='Confirmar Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmar contraseña nueva',
                'class': 'input-group-field',
            }
        )
    )

    def clean_password3(self):
        """Password verification."""
        if self.cleaned_data['password2'] != self.cleaned_data['password3']:
            self.add_error('password3', 'La contraseña no coincide')