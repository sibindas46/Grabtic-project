from django import forms

from phonenumber_field.formfields import PhoneNumberField

from re import fullmatch

from .models import Profile

#we define the things we want inside form class

class AdminLoginForm(forms.Form):

    # username = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.CharField(max_length=50,widget=forms.EmailInput(attrs={'class':'form-control',
                                                                         'placeholder':'Email'}))
    
    password = forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                               'placeholder':'Password'}))

    def clean(self):

        data = super().clean()

        email = data.get('email')

        email_domain_list = ['gmail.com','yahoo.com','outlook.com','hotmail.com','icloud.com','live.com','mailinator.com']

        _,domain = email.split('@')

        if domain not in email_domain_list :

            self.add_error('email','invalid email')

class PhoneForm(forms.Form):

    phone = forms.CharField(max_length=13,widget=forms.TextInput(attrs={'class':'form-control col-lg-12 ',
                                                                        'placeholder':'enter phone number'}))

    def clean(self):

        data = super().clean()
        
        phone = data.get('phone')

        pattern = '(\\+?91)?[789]\\d{9}'

        valid = fullmatch(pattern,phone)

        if not valid :

            self.add_error('phone',' invalid phone number')

        if not Profile.objects.filter(phone=phone).exists():

            self.add_error('phone','not a registered phone number')


class verifyOTPForm(forms.Form):

    otp = forms.CharField(max_length=4,widget=forms.TextInput(attrs={'class':'form-control',
                                                                     'placeholder':'enter OTP'}))

class SignUpPhoneForm(forms.Form):

    phone = forms.CharField(max_length=13,widget=forms.TextInput(attrs={'class':'form-control col-lg-12 ',
                                                                        'placeholder':'enter phone number'}))

    def clean(self):

        data = super().clean()

        phone = data.get('phone')

        pattern = '(\\+?91)?[789]\\d{9}'

        valid = fullmatch(pattern,phone)

        if not valid :

            self.add_error('phone','Invalid phone number')
        
        if Profile.objects.filter(phone=phone).exists():

            self.add_error('phone','This Phone number is already registered')

class AddUserNameForm(forms.Form):

    name = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'class':'form-control col-lg-12 ',
                                                                       'placeholder':'enter name'}))
