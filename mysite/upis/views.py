from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistracijaForma, Dodaj_Korisnika, Dodaj_Predmet, Izradi_Upis, Izradi_Upis_Profesor
from .models import Predmeti, Upisi, Korisnici, Uloga
from django.contrib.auth.decorators import login_required

def register(request):  
    if request.method == 'POST':  
        form = RegistracijaForma(request.POST)  
        if form.is_valid():  
            user = form.save()
            login(request, user)  
            messages.success(request, 'Korisnik stvoren')
            return redirect('login')  
    else:  
        form = RegistracijaForma()  

    context = {'form':form} 
    return render(request, 'register.html', context) 


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Ulogirali ste se!')
                return redirect('home')
            else:
                messages.error(request, 'Pogresno ime ili lozinka!')
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, 'Izlogirali ste se!')
    return redirect('login') 

@login_required
def home(request):
    korisnik = request.user
    predmeti = Predmeti.objects.all()
    if korisnik.uloga_id == 4:
        return render(request, 'home.html', {'predmeti' : predmeti, 'status' : korisnik.status} )
    else:
        return render(request, 'home.html', {'predmeti' : predmeti} )

@login_required
def predmetiStudent(request,student_id):
    predmeti = Predmeti.objects.all()
    id_predmeta=Upisi.objects.values_list('predmet_id', flat=True).filter(korisnik_id=student_id)
    upisi = Upisi.objects.filter(korisnik_id=student_id)
    return render(request, 'predmetiStudent.html', {'predmeti' : predmeti, 'upisi' : upisi, 'id_predmeta' : id_predmeta})



@login_required
def predmetiProfesor(request):
    predmeti = Predmeti.objects.all()
    id_predmeta=Upisi.objects.values_list('predmet_id', flat=True)
    upisi = Upisi.objects.all()
    return render(request, 'predmetiProfesor.html', {'predmeti' : predmeti, 'upisi' : upisi, 'id_predmeta' : id_predmeta})

@login_required
def predmetiAdmin(request):
    predmeti = Predmeti.objects.all()
    id_predmeta=Upisi.objects.values_list('predmet_id', flat=True)
    upisi = Upisi.objects.all()
    return render(request, 'predmetiAdmin.html', {'predmeti' : predmeti, 'upisi' : upisi, 'id_predmeta' : id_predmeta})

@login_required
def studenti(request):
    korisnici = Korisnici.objects.all()
    upisi = Upisi.objects.all()
    return render(request, 'studenti.html', {'korisnici' : korisnici, 'upisi' : upisi})

@login_required
def profesori(request):
    korisnici = Korisnici.objects.all()
    return render(request, 'profesori.html', {'korisnici' : korisnici })

@login_required
def dodajKorisnika(request):
    if request.method == 'POST':
        form = Dodaj_Korisnika(request.POST)
        if form.is_valid():
            korisnik = form.save(commit=False)
            korisnik.set_password(korisnik.password)
            korisnik.author = request.user
            if (korisnik.status != 'none' and korisnik.uloga_id == 5) or (korisnik.status == 'none' and korisnik.uloga_id == 4):
                messages.error(request, "Korisnik nije stvoren!")
            else:
                korisnik.save()
                messages.error(request, "Korisnik stvoren!")
                return redirect('home') 
    else:
        form = Dodaj_Korisnika()
    return render(request, 'dodajKorisnika.html',{'form' : form})

@login_required
def dodajPredmet(request):
    if request.method == 'POST':
        form = Dodaj_Predmet(request.POST)
        if form.is_valid():
            form.save()
            messages.error(request, "Predmet stvoren!")
            return redirect("predmetiAdmin")
    else:
        form = Dodaj_Predmet()
    return render(request, 'dodajPredmet.html', {'form' : form})

@login_required
def urediProfesor(request, profesor_id):
    profesor=get_object_or_404(Korisnici, id=profesor_id)
    form=Dodaj_Korisnika(request.POST or None, instance=profesor)
    if form.is_valid():
        korisnik = form.save(commit=False)
        korisnik.set_password(korisnik.password)
        korisnik.save()
        return redirect("profesori")
    return render(request, "urediProfesor.html", {"form" : form})

@login_required
def urediStudent(request, student_id):
    student=get_object_or_404(Korisnici, id=student_id)
    form = Dodaj_Korisnika(request.POST or None, instance=student)
    if form.is_valid():
        korisnik = form.save(commit=False)
        korisnik.set_password(korisnik.password)
        korisnik.save()
        return redirect("studenti")
    return render(request, "urediStudent.html", {"form" : form})

@login_required
def urediPredmet(request, predmet_id):
    predmet=get_object_or_404(Predmeti, id=predmet_id)
    form=Dodaj_Predmet(request.POST or None, instance=predmet)
    if form.is_valid():
        form.save()
        return redirect("predmetiAdmin")
    return render(request, "urediPredmet.html", {"form" : form})

@login_required
def upisiPredmet(request, predmet_id, student_id):
    if Korisnici.objects.filter(id=student_id, status='red'):
        if Predmeti.objects.filter(id=predmet_id, sem_red=5) or Predmeti.objects.filter(id=predmet_id, sem_red=6):
            id_predmeta=Predmeti.objects.values_list('id',flat=True).filter(sem_red=1)|Predmeti.objects.values_list('id',flat=True).filter(sem_red=2)
            for id in id_predmeta:
                if not Upisi.objects.filter(predmet_id=id, korisnik_id=student_id, status='pass').exists():
                    return HttpResponse("Niste polozili sve s prve!")
                elif not Upisi.objects.filter(predmet_id=id, korisnik_id=student_id).exists():
                    return HttpResponse("Niste polozili sve s prve!")
                
            if Upisi.objects.filter(predmet_id=predmet_id, korisnik_id=student_id, status='not'):
                form = Upisi.objects.get(predmet_id=predmet_id, korisnik_id=student_id)
                form.delete()
            upis = Upisi(predmet_id=predmet_id, korisnik_id=student_id, status="enr")
            upis.save()
            return redirect("predmetiStudent", student_id=student_id) 
        else: 
            if Upisi.objects.filter(predmet_id=predmet_id, korisnik_id=student_id, status='not'):
                form = Upisi.objects.get(predmet_id=predmet_id, korisnik_id=student_id)
                form.delete()
            upis = Upisi(predmet_id=predmet_id, korisnik_id=student_id, status="enr")
            upis.save()
            return redirect("predmetiStudent", student_id=student_id)
    
    elif Korisnici.objects.filter(id=student_id, status='izv'):
        if Predmeti.objects.filter(id=predmet_id, sem_izv=7) or Predmeti.objects.filter(id=predmet_id, sem_izv=8):
            id_predmeta=Predmeti.objects.values_list('id',flat=True).filter(sem_red=1)|Predmeti.objects.values_list('id',flat=True).filter(sem_red=2)
            for id in id_predmeta:
                if not Upisi.objects.filter(predmet_id=id, korisnik_id=student_id, status='pass').exists():
                    return HttpResponse("Niste polozili sve s prve!")
                elif not Upisi.objects.filter(predmet_id=id, korisnik_id=student_id).exists():
                    return HttpResponse("Niste polozili sve s prve!")
                
            if Upisi.objects.filter(predmet_id=predmet_id, korisnik_id=student_id, status='not'):
                form = Upisi.objects.get(predmet_id=predmet_id, korisnik_id=student_id)
                form.delete()
            upis = Upisi(predmet_id=predmet_id, korisnik_id=student_id, status="enr")
            upis.save()
            return redirect("predmetiStudent", student_id=student_id)
        else:
            if Upisi.objects.filter(predmet_id=predmet_id, korisnik_id=student_id, status='not'):
                form = Upisi.objects.get(predmet_id=predmet_id, korisnik_id=student_id)
                form.delete()
            upis = Upisi(predmet_id=predmet_id, korisnik_id=student_id, status="enr")
            upis.save()
            return redirect("predmetiStudent", student_id=student_id)
    """ if Upisi.objects.filter(predmet_id=predmet_id, korisnik_id=student_id, status="not"):
        form = Upisi.objects.get(predmet_id=predmet_id, korisnik_id=student_id)
        form.delete()
    upis = Upisi(predmet_id=predmet_id, korisnik_id=student_id, status="enr")
    upis.save()
    return redirect("predmetiStudent", student_id=student_id) """

@login_required
def ispisiPredmet(request, predmet_id, student_id):
    upis = Upisi.objects.get(predmet_id=predmet_id, korisnik_id=student_id)
    upis.predmet_id=predmet_id
    upis.student_id=student_id
    if upis.status=='enr':
        upis.delete()
    return redirect("predmetiStudent", student_id=student_id)

@login_required
def studentiPredmet(request, predmet_id):
    odabir = request.POST.get('odabir')
    upisi = Upisi.objects.filter(predmet_id=predmet_id)
    studenti = Korisnici.objects.filter(uloga_id=4)

    if odabir:
        if odabir=="1":
            upisi = Upisi.objects.filter(predmet_id = predmet_id)
        elif odabir=="2":
            upisi = Upisi.objects.filter(predmet_id = predmet_id, status='pass')
        elif odabir=="3":
            upisi = Upisi.objects.filter(predmet_id = predmet_id, status='lst')
        return render(request, "studentiPredmet.html", {'upisi': upisi, 'studenti': studenti, 'predmet_id' : predmet_id, 'odabir': odabir}) 
    
    return render(request, 'studentiPredmet.html', {'upisi' : upisi, 'studenti' : studenti, 'predmet_id' : predmet_id}) 

@login_required
def filtriranje(request, student_id):
    semestar= request.POST.get('semestar')
    ects= request.POST.get('ects')
    predmeti = Predmeti.objects.all()
    if Korisnici.objects.filter(id=student_id, status='red'):
        if semestar and ects:
            predmeti = Predmeti.objects.filter(ects__gt=ects, sem_red=int(semestar))
        elif semestar:
            predmeti = Predmeti.objects.filter(sem_red=int(semestar))
        elif ects:
            predmeti = Predmeti.objects.filter(ects__gt=ects)
    elif Korisnici.objects.filter(id=student_id, status='izv'):
        if semestar and ects:
            predmeti = Predmeti.objects.filter(ects__gt=ects, sem_red=int(semestar))
        elif semestar:
            predmeti = Predmeti.objects.filter(sem_izv=int(semestar))
        elif ects:
            predmeti = Predmeti.objects.filter(ects__gt=ects)

    return render(request, "filtriranje.html", {'predmeti': predmeti})

@login_required
def statistika(request, student_id):
    id_predmeta_polozeni=Upisi.objects.values_list('predmet_id', flat=True).filter(korisnik_id=student_id, status="pass")
    id_predmeta_upisani =Upisi.objects.values_list('predmet_id', flat=True).filter(korisnik_id=student_id, status="enr")
    predmeti = Predmeti.objects.all()

    polozioObavezni=0
    upisanipreko6ECTS=0
    for predmet in predmeti:
        if predmet.id in id_predmeta_polozeni and predmet.izborni=='ne':
            polozioObavezni+=1
        if predmet.id in id_predmeta_upisani and predmet.ects > 6:
            upisanipreko6ECTS+=1

    return render(request, "statistika.html", {"polozeniObavezni": polozioObavezni, "upisanipreko6ECTS": upisanipreko6ECTS}) 


@login_required
def promjeniStatusProfesor(request, student_id, predmet_id):
    upis=get_object_or_404(Upisi, korisnik_id=student_id, predmet_id=predmet_id)
    form=Izradi_Upis_Profesor(request.POST, instance=upis)
    if form.is_valid():
        form.save()
        return redirect("predmetiProfesor")
    return render(request, "promjeniStatusProfesor.html", {"form" : form})

@login_required
def promjeniStatusAdmin(request, student_id, predmet_id):
    upis=get_object_or_404(Upisi, korisnik_id=student_id, predmet_id=predmet_id)
    form=Izradi_Upis(request.POST or None, instance=upis)
    if form.is_valid():
        form.save()
        return redirect("studenti")
    return render(request, "promjeniStatusAdmin.html", {"form" : form})

@login_required
def IzradiUpis(request,student_id,predmet_id):
    upis = Upisi(predmet_id=predmet_id, korisnik_id=student_id, status="enr")
    form=Izradi_Upis(request.POST or None, instance=upis)
    if form.is_valid():
        form.save()
        return redirect("studenti")
    return render(request, "promjeniStatusAdmin.html", {"form" : form})

@login_required
def urediUpisniList(request, student_id):
    predmeti = Predmeti.objects.all()
    student = Korisnici.objects.get(id=student_id)
    id_predmeta=Upisi.objects.values_list('predmet_id', flat=True).filter(korisnik_id=student_id)
    id_studenata=Upisi.objects.values_list("korisnik_id", flat=True)
    upisi = Upisi.objects.all()
    return render(request, "urediUpisniList.html", {'student' : student, 'predmeti': predmeti, 'upisi' : upisi , 'id_predmeta' : id_predmeta, 'id_studenata' : id_studenata })

@login_required
def studentiIspis(request, student_id):
    upisi=Upisi.objects.filter(korisnik_id=student_id, status="enr")|Upisi.objects.filter(korisnik_id=student_id, status="pass")
    predmeti=Predmeti.objects.all()
    PolozeniECTS=0
    UpisaniECTS=0

    for upis in upisi:
        if upis.status=="enr":
            predmet_ects=Predmeti.objects.values_list('ects', flat=True).get(id=upis.predmet_id)
            UpisaniECTS+=predmet_ects
        elif upis.status=="pass":
            predmet_ects=Predmeti.objects.values_list('ects', flat=True).get(id=upis.predmet_id)
            PolozeniECTS+=predmet_ects
    
    return render(request, "studentiIspis.html", {"upisi":upisi, "UpisaniECTS":UpisaniECTS,"PolozeniECTS":PolozeniECTS, "predmeti":predmeti})