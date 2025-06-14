import os
from django.db import models
from django.core.files.base import ContentFile
from mutagen import File as MutagenFile
from mutagen.id3 import ID3, APIC, error as ID3Error

class Song(models.Model):
    audio_file = models.FileField(upload_to='songs/')
    title = models.CharField(max_length=200, blank=True)
    artist = models.CharField(max_length=200, blank=True)
    album = models.CharField(max_length=200, blank=True)
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Only parse if it's a new file
        super().save(*args, **kwargs)  # Save file first (required for path)

        if is_new and self.audio_file:
            audio_path = self.audio_file.path
            audio = MutagenFile(audio_path, easy=True)

            if audio:
                self.title = audio.get('title', [self.title])[0]
                self.artist = audio.get('artist', [self.artist])[0]
                self.album = audio.get('album', [self.album])[0]

            # Extract album cover image if MP3 and has ID3 tags
            try:
                tags = ID3(audio_path)
                for tag in tags.values():
                    if isinstance(tag, APIC):
                        image_data = tag.data
                        image_name = os.path.basename(self.audio_file.name).replace('.mp3', '.jpg')
                        self.cover_image.save(image_name, ContentFile(image_data), save=False)
                        break
            except ID3Error:
                pass  # Ignore if no ID3 tags or image

            # Save updated metadata
            super().save(update_fields=['title', 'artist', 'album', 'cover_image'])

    def __str__(self):
        return self.title or os.path.basename(self.audio_file.name)
    


