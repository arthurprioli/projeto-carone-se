import datetime
from django import forms    

def _placeholder_widget(clazz, placeholder: str):
    return clazz(attrs={'placeholder': placeholder})

class CadastroForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=150)
    email = forms.EmailField(label="Email")
    bairro = forms.CharField(label="Bairro")
    carona = forms.RadioSelect()


# from https://stackoverflow.com/a/69965027
class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"
 
class DateTimeLocalField(forms.DateTimeField):
    # Set DATETIME_INPUT_FORMATS here because, if USE_L10N 
    # is True, the locale-dictated format will be applied 
    # instead of settings.DATETIME_INPUT_FORMATS.
    # See also: 
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Date_and_time_formats
     
    input_formats = [
        "%Y-%m-%dT%H:%M:%S", 
        "%Y-%m-%dT%H:%M:%S.%f", 
        "%Y-%m-%dT%H:%M"
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")

class CriarCaronaForm(forms.Form):
    inicio = forms.CharField(
        label="Partida", max_length=100,
        widget=_placeholder_widget(forms.TextInput, "Insira rua de origem")
    )
    data_hora = DateTimeLocalField(
        label="Horário de saída", initial=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    )

    destino = forms.CharField(
        label="Destino", initial="PUC-Rio", max_length=200, disabled=True,
        widget=_placeholder_widget(forms.TextInput, "Insira o destino")
    )
    valor = forms.FloatField(
        label="Valor por pessoa", initial=0, min_value=0, max_value=1000,
        widget=_placeholder_widget(forms.NumberInput, "Qual o valor por pessoa?")
    )
    vagas = forms.IntegerField(
        label="Pessoas por carro", initial=2, min_value=1, max_value=10,
        widget=_placeholder_widget(forms.NumberInput, "Quantas pessoas no carro?")
    )