'''
Created on Aug 4, 2013

@author: antipro
'''
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class Rating(models.Model):
    book = models.OneToOneField('book.Book')
    rating_count = models.IntegerField(default=0)
    average_result = models.DecimalField(default=0.0, max_digits=3, decimal_places=2)

    rating_range = range(1, 6)

    def add_rating(self, user, number):
        try:
            ratingLog = RatingLog.objects.get(book=self.book, user=user)
        except ObjectDoesNotExist:
            self.average_result = (self.average_result * self.rating_count + number) / (self.rating_count + 1)
            self.rating_count += 1

            ratingLog = RatingLog(book=self.book, user=user, rating=number)
            ratingLog.save()
        self.save()

    class Meta:
        app_label = 'book'

class RatingLog(models.Model):
    book = models.ForeignKey('book.Book')
    user = models.ForeignKey(User)
    rating = models.IntegerField(default=0)
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:

        app_label = 'book'
