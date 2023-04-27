from .models import User, Profile, DirectMessage
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms


#override User Model
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('staff_id', 'phone_number', 'email',  'username')

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exists')
        return email

    def clean_id(self):
        staff_id = self.cleaned_data['staff_id']
        user = User.objects.filter(staff_id=staff_id).exists()
        if user:
            raise ValidationError('this email already exists')
        return staff_id

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('this phone number already exists')
        if len(phone_number)!=11:
            raise ValidationError('unsupported number')
        return phone_number

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

#override User Model
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change password using <a href=\'../password/\'> this form</a>.', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('staff_id', 'phone_number', 'email', 'username', 'password', 'last_login')


class UserLoginForm(forms.Form):

    staff_id = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class EditUserForm(forms.ModelForm):
    phone_number = forms.CharField()
    email = forms.EmailField()
    username = forms.CharField()

    class Meta:
	    model = Profile
	    fields = ('bio', 'img')


class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }