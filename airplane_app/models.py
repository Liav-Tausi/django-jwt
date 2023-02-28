from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator


# Create your models here.

class Flight(models.Model):
    class Meta:
        db_table = 'flight'

    flight_number = models.PositiveIntegerField(unique=True, db_column='flight_number')

    origin_country = CountryField(db_column='origin_country')

    origin_city = models.CharField(max_length=128, db_column='origin_city')

    origin_airport_code = models.CharField(max_length=4, db_column='origin_airport_code')

    destination_country = CountryField(db_column='destination_country')

    destination_city = models.CharField(max_length=128, db_column='destination_city')

    destination_airport_code = models.CharField(max_length=4, db_column='destination_airport_code')

    date_and_time_at_origin = models.DateTimeField(verbose_name="Departure Time", db_column='date_and_time_at_origin')

    date_and_time_at_destination = models.DateTimeField(verbose_name="Arrival Time", db_column='date_and_time_at_destination')

    total_num_of_seats = models.PositiveSmallIntegerField(db_column='total_num_of_seats')

    seats_left = models.PositiveSmallIntegerField(db_column='seats_left', blank=True, null=True)

    is_cancelled = models.BooleanField(db_column='is_cancelled')

    seats_price = models.PositiveSmallIntegerField(db_column='seats_price')

    def save(self, *args, **kwargs):
        if not self.seats_left:
            self.seats_left = self.total_num_of_seats
        return super().save(*args, **kwargs)


class Order(models.Model):
    class Meta:
        db_table = 'order'

    flight = models.ForeignKey(Flight,
                               on_delete=models.CASCADE,
                               related_name='orders',
                               blank=True,
                               null=True)

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    number_of_seats = models.PositiveSmallIntegerField(db_column='number_of_seats')
    order_date = models.DateTimeField(auto_now_add=True, db_column='order_date')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, db_column='total_price')




