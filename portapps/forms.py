from django import forms
from .models import ContactModel



class ContactForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name', }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' Last Name', }))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-tag', 'placeholder':'Enter your Email Address',}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-tag',' cols':'20', 'rows':'5', 'placeholder':'Enter your msg',}))

    print('fir--',first_name)
    class Meta():
        model = ContactModel
        fields = ['first_name','last_name', 'email', 'message']

