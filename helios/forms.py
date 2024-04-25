"""
Forms for Helios
"""

from django import forms
from django.conf import settings

from .fields import SplitDateTimeField
from .models import Election
from .widgets import SplitSelectDateTimeWidget


class ElectionForm(forms.Form):
  short_name = forms.SlugField(label="Nome curto", max_length=40, help_text='Digite sem espaços, fará parte do URL da sua eleição, por ex: meu-clube-2024')
  name = forms.CharField(label="Nome longo", max_length=100, widget=forms.TextInput(attrs={'size':60}), help_text='Nome para sua eleição, por ex: Eleição do Meu Clube 2024')
  description = forms.CharField(label="Descrição", max_length=4000, widget=forms.Textarea(attrs={'cols': 70, 'wrap': 'soft'}), required=False)
  election_type = forms.ChoiceField(label="Tipo da eleição", choices = Election.ELECTION_TYPES)
  use_voter_aliases = forms.BooleanField(label="Pseudônimos de eleitor?", required=False, initial=False, help_text='Se selecionado, as identidades dos eleitores serão substituídas por pseudônimos, por exemplo. "V12", no centro de rastreamento de votos')
  #use_advanced_audit_features = forms.BooleanField(required=False, initial=True, help_text='disable this only if you want a simple election with reduced security but a simpler user interface')
  randomize_answer_order = forms.BooleanField(label="Opções em ordem aleatória?", required=False, initial=False, help_text='Habilite isto se quiser que as opções apareçam em ordem aleatória para cada eleitor')
  private_p = forms.BooleanField(required=False, initial=False, label="Privada?", help_text='Uma eleição privada só é visível para eleitores registrados')
  help_email = forms.CharField(required=False, initial="", label="E-mail de ajuda", help_text='Um endereço de e-mail que os eleitores devem entrar em contato se precisarem de ajuda')
  
  if settings.ALLOW_ELECTION_INFO_URL:
    election_info_url = forms.CharField(required=False, initial="", label="URL de download de informações eleitorais", help_text="URL de um documento PDF que contém informações eleitorais extras, por exemplo: biografias e declarações de candidatos")
  
  # times
  voting_starts_at = SplitDateTimeField(label="Início da votação", help_text = 'Data e hora UTC em que a votação começa',
                                   widget=SplitSelectDateTimeWidget, required=False)
  voting_ends_at = SplitDateTimeField(label="Fim da votação", help_text = 'Data e hora UTC em que a votação termina',
                                   widget=SplitSelectDateTimeWidget, required=False)

class ElectionTimeExtensionForm(forms.Form):
  voting_extended_until = SplitDateTimeField(label="Extensão da votação", help_text = 'Data e hora UTC em que a votação é extendida',
                                   widget=SplitSelectDateTimeWidget, required=False)
  
class EmailVotersForm(forms.Form):
  subject = forms.CharField(max_length=80)
  body = forms.CharField(max_length=4000, widget=forms.Textarea)
  send_to = forms.ChoiceField(label="Enviar para", initial="all", choices= [('all', 'all voters'), ('voted', 'eleitores que votaram'), ('not-voted', 'eleitores que ainda não votaram')])

class TallyNotificationEmailForm(forms.Form):
  subject = forms.CharField(max_length=80)
  body = forms.CharField(max_length=2000, widget=forms.Textarea, required=False)
  send_to = forms.ChoiceField(label="Enviar para", choices= [('all', 'all voters'), ('voted', 'apenas eleitores que votaram'), ('none', 'ninguém - você tem certeza disso?')])

class VoterPasswordForm(forms.Form):
  voter_id = forms.CharField(max_length=50, label="ID de Eleitor")
  password = forms.CharField(widget=forms.PasswordInput(), max_length=100)

