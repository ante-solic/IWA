from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Korisnici, Uloga, Predmeti, Upisi

class RegistracijaForma(UserCreationForm):
    uloga = forms.ModelChoiceField(queryset=Uloga.objects.all())
    status = forms.ChoiceField(choices=Korisnici.STATUS)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = Korisnici
        fields = ['username', 'email', 'password1', 'password2', 'uloga', 'status']

class Dodaj_Predmet(forms.ModelForm):
    class Meta:
        model = Predmeti
        fields = ['name','kod','program', 'ects', 'sem_red', 'sem_izv', 'izborni', 'nositelj_predmeta']
    
    def __init__(self,*args,**kwargs):
        super (Dodaj_Predmet,self ).__init__(*args,**kwargs)
        self.fields['nositelj_predmeta'].queryset = Korisnici.objects.filter(uloga_id=5)

class Dodaj_Korisnika(forms.ModelForm):
    class Meta:
        model = Korisnici
        fields = ['username', 'email', 'password', 'uloga', 'status']

class Izradi_Upis(forms.ModelForm):
    STATUS = [
        ('not','Neupisan'),
        ('enr','Upisan'),
        ('pass', 'Polozen'),
        ('lst', 'Izgubio potpis'),
    ]
    status=forms.ChoiceField(choices=STATUS)
    class Meta:
        model = Upisi
        fields = ['status']

class Izradi_Upis_Profesor(forms.ModelForm):
    STATUS = [
        ('pass', 'Polozen'),
        ('lst', 'Izgubio potpis'),
    ]
    status=forms.ChoiceField(choices=STATUS)

    class Meta:
        model = Upisi
        fields = ['status']
