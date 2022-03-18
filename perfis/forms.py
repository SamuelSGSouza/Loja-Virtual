from django import forms
from django import forms
from . import models
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirme sua senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'username', 'password',
                  'password2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_messages = {}

        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        print(password2_data)

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_existe = 'Usuário já existe.'
        error_msg_email_existe = 'Email já cadastrado.'
        error_msg_passwords_dont_match = 'As senhas não conferem.'
        error_msg_passwords_too_short = 'A senha deve conter no mínimo 6 caracteres.'

        # usuarios logados
        if self.usuario:

            if usuario_data != usuario_db.username:
                if usuario_db:
                    validation_error_messages['username'] = error_msg_user_existe

            if email_data != email_db.email:
                validation_error_messages['email'] = error_msg_email_existe

            if password_data:
                if password_data != password2_data:
                    validation_error_messages['password'] = error_msg_passwords_dont_match
                    validation_error_messages['password2'] = error_msg_passwords_dont_match

                if len(password_data):
                    validation_error_messages['password'] = error_msg_passwords_too_short

        # usuarios não logados. Cadastro.
        else:
            validation_error_messages['username'] = 'balblbalblabla'

        if validation_error_messages:
            raise(forms.ValidationError(validation_error_messages))


class PerfilForm(forms.ModelForm):

    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario', )
