from django.db import models

# Create your models here.

from shows.models import BaseClass

from theatre.models import PaymentStatusChoices

class Payment(BaseClass):

    booking = models.ForeignKey('theatre.Bookings',on_delete=models.CASCADE)

    amount = models.FloatField(default=0)

    payment_status = models.CharField(max_length=20,choices=PaymentStatusChoices)

    paid_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):

        return f'{self.booking.profile.first_name}--{self.booking.movie.name}--{self.booking.screen_date_time.theatre.name}--{self.booking.screen_date_time.screen.name}--{self.booking.screen_date_time.date.date}--payment'

    class Meta:

        verbose_name = 'Payments'

        verbose_name_plural = 'Payments'


class Transactions(BaseClass):

    payment = models.ForeignKey('Payment',on_delete=models.CASCADE)

    rzp_order_id = models.SlugField()

    amount = models.FloatField()

    status = models.CharField(max_length=20,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    transactions_at = models.DateTimeField(null=True,blank=True)

    rzp_payment_id = models.SlugField(null=True,blank=True)

    rzp_signature = models.TextField() 

    def __str__(self):

        return f'{self.payment.booking.profile.first_name}--{self.payment.booking.movie.name}--transaction-{self.create_at}'

    class Meta:

        verbose_name = 'Transactions'

        verbose_name_plural = 'Transactions'
