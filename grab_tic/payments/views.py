from django.shortcuts import render,redirect

from django.views import View

from .models import Payment,Transactions

import razorpay

from decouple import config

from django.utils import timezone

from django.contrib import messages
# Create your views here.

class RazorpayView(View):

    template = 'payments/razorpay.html'

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        payment = Payment.objects.get(uuid=uuid)

        client = razorpay.Client(auth=(config('RZP_KEY_ID'), config('RZP_KEY_SECRET')))

        data = { "amount": payment.amount*100, "currency": "INR", "receipt": "order_rcptid_11" }

        rzp_payment = client.order.create(data=data) 

        rzp_order_id = rzp_payment.get('id')

        Transactions.objects.create(payment=payment,rzp_order_id=rzp_order_id,amount=payment.amount)

        data = {'RZP_KEY_ID':config('RZP_KEY_ID'),'amount':rzp_payment.get('amount'),'rzp_order_id':rzp_order_id}

        return render(request,self.template,context=data)
    

class PaymentVerifyView(View):

    def post(self,request,*args,**kwargs):

        razorpay_payment_id = request.POST.get('razorpay_payment_id')

        razorpay_order_id = request.POST.get('razorpay_order_id')

        razorpay_signature = request.POST.get('razorpay_signature')

        transaction = Transactions.objects.get(rzp_order_id=razorpay_order_id)
 
        paid = client = razorpay.Client(auth=(config('RZP_KEY_ID'), config('RZP_KEY_SECRET')))

        client.utility.verify_payment_signature({
                                                'razorpay_order_id': razorpay_order_id,
                                                'razorpay_payment_id': razorpay_payment_id,
                                                'razorpay_signature': razorpay_signature
                                                })
        
        transaction.rzp_payment_id = razorpay_payment_id

        transaction.rzp_signature = razorpay_signature
        
        if paid :

            transaction.status = 'Success'

            transaction.transactions_at = timezone.now()

            transaction.payment.payment_status = 'Success'

            transaction.payment.paid_at = timezone.now()

            transaction.payment.booking.booked = True

            transaction.payment.booking.payment_status = 'Success'

            transaction.save()

            transaction.payment.save()

            transaction.payment.booking.save()

            messages.success(request,'Movie tickets Successfully Booked')





        else:

            transaction.status = 'Failed'

            transaction.transaction_at = timezone.now()

            transaction.payment.payment_status = 'Failed'

            transaction.payment.paid_at = timezone.now()

            transaction.save()

            transaction.payment.save()

        


        return redirect('home')
    
