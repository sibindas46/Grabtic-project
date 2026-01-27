from django.db import models

from shows.models import BaseClass

# Create your models here.

class Place(BaseClass):

    name = models.CharField(max_length=20)

    class Meta:

        verbose_name = 'Places'

        verbose_name_plural = 'Places'
    
    def __str__(self):
        
        return self.name
    
class Theatre(BaseClass):

    name = models.CharField(max_length=50)

    place = models.ForeignKey('Place',on_delete=models.CASCADE)


    def __str__(self):

        return f'{self.name}--{self.place.name}'
    
    class Meta:

        verbose_name = 'Theatre'

        verbose_name_plural = 'Theatre'

class Screens(BaseClass):

    name = models.CharField(max_length=50)

    theatre = models.ForeignKey('Theatre',on_delete=models.CASCADE)

    no_of_seats = models.IntegerField()

    def __str__(self):

        return f'{self.name}-{self.theatre.name}'

    class Meta:

        verbose_name = 'Screens'

        verbose_name_plural = 'Screens'

class ShowDate(BaseClass):

    date = models.DateField()

    

    def __str__(self):

        return f'{self.date}'
    
    class Meta:

        verbose_name = 'Show Dates'

        verbose_name_plural = 'Show Dates'

class ShowTime(BaseClass):

    time = models.TimeField()

    def __str__(self):

        return f'{self.time}'
    
    class Meta:

        verbose_name = 'Show Times'

        verbose_name_plural = 'Show Times'

class ScreensDateTime(BaseClass):

    theatre = models.ForeignKey('Theatre',on_delete=models.CASCADE)

    screen = models.ForeignKey('Screens',on_delete=models.CASCADE)

    date = models.ForeignKey('ShowDate',on_delete=models.CASCADE)

    time = models.ForeignKey('ShowTime',on_delete=models.CASCADE)

    def __str__(self):

        return f'{self.theatre.name}-{self.screen.name}-{self.date.date}-{self.time.time}'
    
    class Meta:

        verbose_name = 'Screen Date Time'

        verbose_name_plural = 'Screen Date Time'

class OngoingShows(BaseClass):

    movie = models.ForeignKey('shows.Movie',on_delete=models.CASCADE) 

    screen_date_time = models.ManyToManyField('ScreensDateTime')

    # theatre = models.ManyToManyField('Theatre')

    # screens = models.ManyToManyField('Screens')

    # show_date = models.ManyToManyField('ShowDate')

    # show_time = models.ManyToManyField('ShowTime')

    def __str__(self):

        return f'{self.movie.name}--ongoing'
    
    class Meta:

        verbose_name = 'Ongoing Shows'

        verbose_name_plural = 'Ongoing Shows'

class RowChoices(models.TextChoices):

    A = 'A','A'

    B = 'B', 'B'
    C = 'C', 'C'
    D = 'D', 'D'
    E = 'E', 'E'
    F = 'F', 'F'
    G = 'G', 'G'
    H = 'H', 'H'
    I = 'I', 'I'
    J = 'J', 'J'
    K = 'K', 'K'
    L = 'L', 'L'
    M = 'M', 'M'
    N = 'N', 'N'
    O = 'O', 'O'
    P = 'P', 'P'
    Q = 'Q', 'Q'
    R = 'R', 'R'
    S = 'S', 'S'
    T = 'T', 'T'
    U = 'U', 'U'
    V = 'V', 'V'
    W = 'W', 'W'
    X = 'X', 'X'
    Y = 'Y', 'Y'
    Z = 'Z', 'Z'


class Seat(BaseClass):

    screen = models.ForeignKey('Screens',on_delete=models.CASCADE)

    row = models.CharField(max_length=1,choices=RowChoices.choices)

    seat_num = models.IntegerField()

    price = models.FloatField()

    def __str__(self):

        return f'{self.screen.theatre.name}--{self.screen.name}---{self.row}--{self.seat_num}'
    
    class Meta:

        verbose_name = 'Seats'

        verbose_name_plural = 'Seats'


class PaymentStatusChoices(models.TextChoices):

    PENDING = 'Pending','Pending'

    SUCCESS = 'Success','Success'

    FAILED = 'Failed','Failed'



class Bookings(BaseClass):

    profile = models.ForeignKey('authentication.Profile',on_delete=models.CASCADE)

    movie = models.ForeignKey('shows.Movie',on_delete=models.CASCADE)

    screen_date_time = models.ForeignKey('ScreensDateTime',on_delete=models.CASCADE)

    seats = models.ManyToManyField('Seat')

    booked = models.BooleanField(default=False)

    payment_status = models.CharField(max_length=20,choices=PaymentStatusChoices.choices)


    def __str__(self):

        return f'{self.profile.first_name}--{self.movie.name}---{self.screen_date_time.date.date}--{self.screen_date_time.time.time}'
    
    class Meta:

        verbose_name = 'Bookings'

        verbose_name_plural = 'Bookings'



