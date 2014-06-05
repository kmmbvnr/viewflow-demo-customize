from django.db import models
from django.contrib.auth.models import User
from viewflow.models import Process
from django_fsm import FSMField


class Country(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=150)


class City(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    country = models.ForeignKey(Country)


class Currency(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    is_local_currency = models.BooleanField(default=False)


class ExpenseType(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)


class Airline(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)


class Hotel(models.Model):
    name = models.CharField(max_length=150)
    telephone = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    comments = models.TextField()
    nights = models.IntegerField()
    checkin_date = models.DateTimeField()
    checkout_date = models.DateField()
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)


class TravelRequest(models.Model):
    class STATUS:
        NEW = 'NEW'

    applicant = models.ForeignKey(User, related_name='+')
    authorier = models.ForeignKey(User, null=True, related_name='+')

    purpose = models.CharField(max_length=250)
    commencts = models.TextField()

    request_date = models.DateTimeField(auto_now_add=True)
    departure_date = models.DateTimeField()
    return_date = models.DateTimeField()
    approval_date = models.DateTimeField(null=True)
    advance_issued_date = models.DateTimeField(null=True)

    need_book_hotel = models.BooleanField(default=False)
    need_book_flight_tickets = models.BooleanField(default=False)

    total_advance = models.DecimalField(null=True,max_digits=6, decimal_places=2)
    local_currency = models.ForeignKey(Currency)
    exchange_rate = models.DecimalField(null=True, max_digits=10, decimal_places=4)

    departure_city = models.ForeignKey(City, related_name='+')
    destination_city = models.ForeignKey(City, related_name='+')
    
    hotel = models.ForeignKey(Hotel, null=True)
    cach_advance_receipt = models.FileField(upload_to='receipts')

    status = FSMField(max_length=3, default=STATUS.NEW)
    
    @property
    def total_advance_local(self):
        return self.total_advance * self.exchange_rate


class Expense(models.Model):
    request = models.ForeignKey(TravelRequest)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=150)
    expense_type = models.ForeignKey(ExpenseType)


class FlightTicket(models.Model):
    request = models.ForeignKey(TravelRequest)
    flight_number = models.CharField(max_length=50)
    arrival_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    arrival_city = models.ForeignKey(City, related_name='+')
    departure_city = models.ForeignKey(City, related_name='+')
    airline = models.ForeignKey(Airline)


class ApprovalProcess(Process):
    request = models.ForeignKey(TravelRequest)
