#################################
# Programmer: Kenneth Sinder
# Date: 2017-02-04
# Filename: core/models.py
# Description: Business logic
#################################

from django.db import models
from django.contrib.auth.models import User

class Textbook(models.Model):
    """
    Represents a single textbook item.
    """

    name = models.CharField(max_length=120)
    author = models.CharField(max_length=96)
    sku = models.CharField(max_length=96)
    new_price = models.DecimalField(decimal_places=2, max_digits=10)
    used_price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    is_required = models.BooleanField()

    def __str__(self):
        return "{0}: {1}".format(self.author, self.name)

    class Meta:
        verbose_name_plural = "Textbooks"
        ordering = ["name"]

class Course(models.Model):
    """
    Represents a single UW course.
    """

    title = models.CharField(max_length=96)
    subject = models.CharField(max_length=5)
    catalog_number = models.IntegerField()
    books = models.ManyToManyField(Textbook)

    def __str__(self):
        return "{0} {1}".format(self.subject, self.catalog_number)

    class Meta:
        verbose_name_plural = "Courses"
        ordering = ["catalog_number"]

class Rating(models.Model):
    """
    Represents a rating for a particular course and its textbook.
    """

    book = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_useful = models.BooleanField()
