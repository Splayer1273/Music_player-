from django.db import models

# Create your models here.





class song(models.Model):
    title = models.TextField()
    artist = models.TextField()
    image = models.ImageField(upload_to='images/')
    audio_file = models.FileField(upload_to='audio/')
    audio_link=models.CharField( max_length=200, blank=True, null=True)
    lyrics= models.TextField( blank=True, null=True)
    duration= models.CharField(max_length=20, blank=True, null=True) 
    paginate_by = 2

    def __str__(self):
        return self.title
    

class playlist(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(song, related_name='playlists')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Playlists" 
