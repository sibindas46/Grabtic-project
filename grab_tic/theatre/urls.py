from django.urls import path

from . import views

urlpatterns = [

    path('places/',views.ShowPlace.as_view(),name='places'),

    path('add-place/<str:uuid>/',views.AddPlace.as_view(),name='add-place'),

    path('theatre-list/<str:uuid>/',views.TheatreListView.as_view(),name='theatre-list'),

    path('screen-seats/<str:screen_uuid>/<str:movie_uuid>/<str:screen_date_time_uuid>/',views.ScreenSeatsView.as_view(),name='screen-seats'),

    path('booking/<str:movie_uuid>/<str:screen_date_time_uuid>/',views.BookingView.as_view(),name='booking'),

    path('confirm-and-pay/<str:uuid>/',views.ConfirmAndPayView.as_view(),name='confirm-and-pay'),

    

]