from django.shortcuts import render,redirect

from django.views import View

from .models import Place

from django.utils.decorators import method_decorator

from authentication.permissions import user_role_permission

from shows.models import Movie

from . models import OngoingShows,ShowDate,ScreensDateTime,Seat,Bookings

from payments.models import Payment

from django.utils import timezone

from datetime import datetime

from django.db.models import Sum

from django.contrib import messages

# Create your views here.

@method_decorator(user_role_permission(roles=['Admin','User'],redirect_url='home'),name='dispatch')
class ShowPlace(View):

    template = 'theatre/places.html'

    def get(self,request,*args,**kwargs):

        places = Place.objects.all()

        query = request.GET.get('query')
        
        next = request.GET.get('next')

        uuid = request.GET.get('uuid')

        if query :

            places = places.filter(name__icontains=query)

        data = {'places':places,'query':query}

        if next and uuid :

            data.update({'next':next,'uuid':uuid})

        return render(request,self.template,context=data)
    

@method_decorator(user_role_permission(roles=['User'],redirect_url='user-login'),name='dispatch')    
class AddPlace(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        next =request.GET.get('next')

        movie_uuid = request.GET.get('uuid')

        place = Place.objects.get(uuid=uuid)

        user = request.user

        user.place = place

        user.save()

        if next and movie_uuid:

            return redirect(next,uuid=movie_uuid)

        return redirect('home')

class TheatreListView(View):

    template = 'theatre/theatre-list.html' 

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        date = request.GET.get('date')

        today = timezone.now().date()

        place = request.user.place

        if date :

            date = datetime.strptime(date, "%Y-%m-%d").date()

        else:

            date = today

        print(date)
        ongoing_shows = OngoingShows.objects.filter(active_status=True,movie=movie,screen_date_time__date__date=date,screen_date_time__theatre__place=place)

        all_dates = ShowDate.objects.filter(screensdatetime__ongoingshows__in = ongoing_shows,date__gte=today).distinct().order_by('date')

        theatres_screens_times = {}

        for show in ongoing_shows :

            for screen_date_time in show.screen_date_time.filter(date__date=date,theatre__place=place):

                theatre = screen_date_time.theatre

                screen = screen_date_time.screen

                time = screen_date_time.time

                if theatre not in theatres_screens_times:

                    theatres_screens_times[theatre]={}

                if screen not in theatres_screens_times[theatre]:

                    theatres_screens_times[theatre][screen] = []

                if time not in theatres_screens_times[theatre][screen]:

                    theatres_screens_times[theatre][screen].append(time)

        # print(theatres_screens_times)

        data={'theatres_screens_times':theatres_screens_times,'all_dates':all_dates,'date':date,'movie':movie}

        return render(request,self.template,context=data)
    

class ScreenSeatsView(View):

    template = 'theatre/screen-seats.html'

    def get(self,request,*args,**kwargs):

        screen_uuid = kwargs.get('screen_uuid')

        movie_uuid= kwargs.get('movie_uuid')

        screen_date_time_uuid = kwargs.get('screen_date_time_uuid')

        movie = Movie.objects.get(uuid=movie_uuid)

        screen_date_time = ScreensDateTime.objects.get(uuid = screen_date_time_uuid)

        all_seats = Seat.objects.filter(screen__uuid=screen_uuid).order_by('-row','seat_num',)

        price = all_seats.first().price

        all_seats_dict = {}

        for seat in all_seats:

            if seat.row not in all_seats_dict :

                all_seats_dict[seat.row] = []

            all_seats_dict[seat.row].append(seat)

        data = {'all_seats_dict':all_seats_dict,'movie':movie,'screen_date_time':screen_date_time,'price':price}
        
        return render(request,self.template,context=data)
    
class BookingView(View):

    def post(self,request,*args,**kwargs):

        movie_uuid = kwargs.get('movie_uuid')

        screen_date_time_uuid = kwargs.get('screen_date_time_uuid')

        movie = Movie.objects.get(uuid=movie_uuid)

        screen_date_time = ScreensDateTime.objects.get(uuid=screen_date_time_uuid)

        selected_seats = request.POST.getlist('selected_seats')

        if not selected_seats:

            messages.error(request,'No Seats Selected')

            return redirect('screen-seats',screen_uuid=screen_date_time.screen.uuid,movie_uuid=movie_uuid,screen_date_time_uuid=screen_date_time_uuid)

        booking,_ = Bookings.objects.get_or_create(profile=request.user,movie=movie,screen_date_time=screen_date_time)

        seats = Seat.objects.filter(uuid__in = selected_seats)

        booking.seats.set(seats)

        payment,_ =  Payment.objects.get_or_create(booking=booking)

        amount = booking.seats.aggregate(total=Sum('price'))['total']

        amount = amount+amount*0.18

        payment.amount = amount

        payment.save()         

        return redirect('confirm-and-pay',uuid = payment.uuid)

class ConfirmAndPayView(View):

    template ='theatre/confirm-and-pay.html'

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        payment = Payment.objects.get(uuid=uuid)

        data = {'payment':payment}

        return render(request,self.template,context=data)
    
