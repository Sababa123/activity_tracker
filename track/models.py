from django.db import models

class Activity(models.Model):
    name = models.CharField(max_length=100, default="xyz")
    bar_color = models.CharField(max_length=50, default="black")
    group_num = models.CharField(max_length=25, default="1")
    rank = models.IntegerField(default=9999)

    def __str__(self):
        return self.name + '/' + str(self.rank)

class ActivityTracker(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    category_name = models.CharField(max_length=100, default="xyz")
    category_bar_color = models.CharField(max_length=50, default="black")
    category_group_num = models.CharField(max_length=25, default="1")
    elapsed_time = models.FloatField()
    def __str__(self):
        return self.category_name  + '/' + str(self.date) + '/' + str(self.start_time) + '/' + str(self.end_time)
