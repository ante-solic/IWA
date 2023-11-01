from django.db import models
from django.contrib.auth.models import AbstractUser

class Uloga(models.Model):
    uloga = models.CharField(max_length=50)

    def __str__(self):
        return self.uloga
    
class Korisnici(AbstractUser):
    STATUS = (('none','None'),('izv','izvanredni'),('red','redovni'))
    uloga=models.ForeignKey(Uloga, on_delete=models.CASCADE,  null=True, blank=True)
    status=models.CharField(max_length=50, choices=STATUS)

class Predmeti(models.Model):
    IZBORNI = (('da', 'da'), ('ne', 'ne'))
    name = models.CharField(max_length=100)
    kod = models.CharField(max_length=20)
    program = models.TextField()
    ects = models.PositiveIntegerField()
    sem_red = models.PositiveIntegerField()
    sem_izv = models.PositiveIntegerField()
    izborni = models.CharField(max_length=10, choices=IZBORNI)
    nositelj_predmeta=models.ForeignKey(Korisnici, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.name, self.kod, self.program, self.ects, self.sem_red, self.sem_izv, self.izborni, self.nositelj_predmeta)

class Upisi(models.Model):
    STATUS = (('not','Neupisan'),('enr','Upisan'),('pass','Polozen'),('lst','Izgubio potpis'))
    korisnik=models.ForeignKey(Korisnici, on_delete=models.CASCADE)
    predmet=models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status=models.CharField(max_length=50, choices=STATUS,  null=True, blank=True)
    
    def __str__(self):
            return '%s %s %s' % (self.korisnik,self.predmet,self.status)