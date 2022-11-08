from django import forms    

class CadastroForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=150)
    email = forms.EmailField(label="Email")
    bairro = forms.CharField(label="Bairro")
    carona = forms.RadioSelect()