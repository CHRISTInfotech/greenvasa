from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator



# from .models import Order


# class OrderForm(ModelForm):
# 	class Meta:
# 		model = Order
# 		fields = '__all__'

class CreateUserForm(UserCreationForm):
   phone_regex = RegexValidator(regex=r'^[6-9]\d{9}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
   phone = forms.CharField(validators=[phone_regex], max_length=17)


   def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'name', 
            'id':'floatingInput', 
            'type':'text', 
            'placeholder':'John Doe', 
            'maxlength': '36', 
            'minlength': '4', 
            }) 
        self.fields['email'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'email_address', 
            'id':'floatingInput', 
            'type':'email', 
            'placeholder':'JohnDoe@mail.com', 
            }) 
        self.fields['phone'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'mobile_number', 
            'id':'floatingInput', 
            'type':'number', 
            'placeholder':'JohnDoe@mail.com', 
            }) 
        self.fields['password1'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'password', 
            'id':'floatingInput', 
            'type':'password', 
            'placeholder':'password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'confirm_password', 
            'id':'password2', 
            'type':'floatingInput', 
            'placeholder':'password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
 
 
   username = forms.CharField(max_length=20, label=False) 
   email = forms.EmailField(max_length=100) 


   class Meta:
      model = User
      fields = ('username', 'email', 'phone', 'password1', 'password2')

      # widgets = {
      #    'username': forms.TextInput(attrs={'class': 'form-control'}),
      #    'email': forms.EmailInput(attrs={'class': 'form-control'}),
      #    'phone': forms.NumberInput(attrs={'class': 'form-control'}),
      #    'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
      #    'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
      # }