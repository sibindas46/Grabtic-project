from django import template

from .models import ScreensDateTime,Bookings

register = template.Library()


@register.simple_tag
def get_screen_date_time_uuid(screen,date,time):

    return ScreensDateTime.objects.get(screen=screen,time=time,date__date=date).uuid

@register.simple_tag
def movie_booked(movie,sdt,seat):

    bookings = Bookings.objects.filter(movie=movie,screen_date_time=sdt,booked=True,payment_status='Success')

    booked = False

    for booking in bookings:

        if booking.seats.filter(id=seat.id).exists():

            booked = True

            break

    return booked

