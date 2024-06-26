from django.db import models
from django.urls import reverse
from datetime import datetime, date
from django.contrib.auth.models import User

class VolunteeringEvent(models.Model):

    def default_time():
        return datetime.now().time()

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(default=date.today)
    time = models.TimeField(default=default_time)
    location = models.CharField(max_length=255)
    volunteers_needed = models.PositiveIntegerField(default=1)
    donation_goal = models.PositiveIntegerField('Donation goal $', default=0)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    volunteers = models.ManyToManyField(User, related_name='volunteering_events', blank=True)

    def __str__(self):
        return self.title

    def volunteer_count(self):
        return self.volunteers.count()
    
    def donation_amount(self):
        donations = Donation.objects.filter(event_id=self.id).all()
        total_donation=sum(donation.amount for donation in donations)
        return total_donation
    
    def donations(self):
        donations = Donation.objects.filter(event_id=self.id).all()
        return [donation for donation in donations]
    
    def donor_count(self):
        donations = Donation.objects.filter(event_id=self.id).all()
        number_of_donors = donations.count()
        return number_of_donors

    def donation_percentage_reached(self):
        donations = Donation.objects.filter(event_id=self.id).all()
        total_donation=sum(donation.amount for donation in donations)
        if total_donation == 0: 
            percentage = 0 
        elif self.donation_goal == 0:
            percentage = "No goal set"
        else: 
            percentage = round((total_donation / self.donation_goal) * 100)
        return percentage
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.id})

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('VolunteeringEvent', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.event.title}"

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(VolunteeringEvent, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} donated ${self.amount} to {self.event.title}"