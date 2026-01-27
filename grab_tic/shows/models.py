from django.db import models

import uuid

from multiselectfield import MultiSelectField

# Create your models here.

class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True,default=uuid.uuid4) #used to generate unique codes

    active_status = models.BooleanField(default=True)

    create_at = models.DateTimeField(auto_now_add=True)
    
    update_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True

class CertificationChoices(models.TextChoices):

    U = 'U','U'

    A = 'A','A'

    U_OR_A = 'U/A','U/A'

    S = 'S','S'

class LanguagesChoices(models.TextChoices):

    MALAYALAM = 'Malayalam','Malayalam'

    ENGLISH = 'English','English'

    TAMIL = 'Tamil','Tamil'

    TELUGU = 'Telugu','Telugu'

    HINDI = 'Hindi','Hindi'

    KANNADA = 'Kannada','Kannada'

class CastChoices(models.TextChoices):

    MOHANLAL = 'Mohanlal','Mohanlal'

    MAMMOOTTY = 'Mammootty','Mammootty'

    NIVIN_PAULY = 'Nivin Pauly','Nivin Pauly'

    SHOBANA = 'SHOBANA','SHOBANA'

    KALYANI_PRIYAN = 'Kalyani Priyan','Kalyani Priyan'

class GenreChoices(models.TextChoices):

    ACTION ='ACTION','ACTION'

    CRIME = 'CRIME','CRIME'

    THRILLER ='THRILLER','THRILLER'

    ROMANCE = 'ROMANCE','ROMANCE'

    COMEDY = 'COMEDY','COMEDY'

    HORROR = 'HORROR','HORROR' 

class Certification(BaseClass):

    name = models.CharField(max_length=50)

    class Meta:

        verbose_name = 'Certifications'

        verbose_name_plural = 'Certifications'

    def __str__(self):

        return f'{self.name}'

class Language(BaseClass):

    name = models.CharField(max_length=50)

    class Meta:

        verbose_name = 'Languages'

        verbose_name_plural = 'Languages'

    def __str__(self):

        return f'{self.name}'

class Cast(BaseClass):

    name = models.CharField(max_length=50)

    photo = models.ImageField(upload_to='cast-images')

    class Meta:

        verbose_name = 'casts'

        verbose_name_plural = 'casts'
    
    def __str__(self):

        return f'{self.name}'

class Genre(BaseClass):

    name = models.CharField(max_length=50)

    class Meta:

        verbose_name = 'Genre'

        verbose_name_plural = 'Genre'

    def __str__(self):

        return f'{self.name}'

class Movie(BaseClass):

    name = models.CharField(max_length=50)

    description = models.TextField()

    runtime = models.TimeField()

    photo = models.ImageField(upload_to='movie-images')

    release_date = models.DateField()

    # certificate = models.CharField(max_length=20,choices=CertificationChoices.choices)
    certificate = models.ForeignKey('Certification',on_delete=models.CASCADE)
    #we can use 'Authentication.Profile' instead of importing Profile

    # language = MultiSelectField(choices=LanguagesChoices.choices)
    language = models.ManyToManyField('Language')

    # cast = MultiSelectField(choices=CastChoices.choices)
    cast = models.ManyToManyField('Cast')

    # genre = MultiSelectField(choices=GenreChoices.choices)
    genre = models.ManyToManyField('Genre')

    class Meta:

        verbose_name = 'Movies'

        verbose_name_plural = 'Movies'

    def __str__(self):

        return f'{self.name}---{self.release_date}'