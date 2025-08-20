from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #cascade means that if the user is deleted then the profile will be deleted
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics') # this is the image field for the profile
    

    def __str__(self):
        return f'{self.user.get_full_name()} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Only process image if it exists and is not the default
        if self.image and self.image.name != 'default.jpg' and os.path.exists(self.image.path):
            try:
                img = Image.open(self.image.path) #this will open the image of the current instance

                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except Exception as e:
                # If there's an error processing the image, just continue
                pass