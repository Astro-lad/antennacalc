from django.db import models
from django.urls import reverse
#from supabase_storage import upload_file

class Antenna(models.Model):
    ANTENNA_TYPES = [
        ('yagi', "Yagi"),
        ('dipole', 'Dipole'),
        ('spiral', 'Spiral'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ANTENNA_TYPES)
    detail = models.TextField()
#    image = models.URLField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('antennas:antenna_detail', args=[self.id])

