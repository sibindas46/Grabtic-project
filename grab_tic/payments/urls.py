from django.urls import path

from . import views

urlpatterns = [

    path('razorpay/<str:uuid>/',views.RazorpayView.as_view(),name='razorpay'),

    path('payment-verify/',views.PaymentVerifyView.as_view(),name='payment-verify'),

    path('ticket/<str:uuid>/',views.TicketView.as_view(),name='ticket'),

    path('ticket-pdf/<str:uuid>/',views.TicketPDFGenerate.as_view(),name='ticket-pdf'),
]