from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.register, name="register"),
    path("login/",views.user_login,name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name="home"),
    path('predmetiStudent/<int:student_id>',views.predmetiStudent, name="predmetiStudent"),
    path('predmetiProfesor/',views.predmetiProfesor, name="predmetiProfesor"),
    path('predmetiAdmin/',views.predmetiAdmin, name="predmetiAdmin"),
    path('studenti/',views.studenti, name="studenti"),
    path('profesori/',views.profesori, name="profesori"),
    path('dodajKorisnika/',views.dodajKorisnika ,name="dodajKorisnika"),
    path('dodajPredmet/',views.dodajPredmet ,name="dodajPredmet"),
    path("urediProfesor/<int:profesor_id>", views.urediProfesor, name="urediProfesor"),
    path("urediStudent/<int:student_id>", views.urediStudent, name="urediStudent"),
    path("urediPredmet/<int:predmet_id>", views.urediPredmet, name="urediPredmet"),
    path("upisiPredmet/<int:student_id>/<int:predmet_id>",views.upisiPredmet, name="upisiPredmet"),
    path("ispisiPredmet/<int:student_id>/<int:predmet_id>",views.ispisiPredmet, name="ispisiPredmet"),
    path("studentiPredmet/<int:predmet_id>", views.studentiPredmet, name="studentiPredmet"),
    path("promjeniStatusProfesor/<int:student_id>/<int:predmet_id>", views.promjeniStatusProfesor, name="promjeniStatusProfesor"),
    path("promjeniStatusAdmin/<int:student_id>/<int:predmet_id>", views.promjeniStatusAdmin, name="promjeniStatusAdmin"),
    path("urediUpisniList/<int:student_id>", views.urediUpisniList, name="urediUpisniList"),
    path("IzradiUpis/<int:student_id>/<int:predmet_id>", views.IzradiUpis, name="IzradiUpis"),
    path("studentiIspis/<int:student_id>", views.studentiIspis, name="studentiIspis"),
    path("filtriranje/<int:student_id>", views.filtriranje, name="filtriranje"),
    path("statistika/<int:student_id>", views.statistika, name="statistika"),
]