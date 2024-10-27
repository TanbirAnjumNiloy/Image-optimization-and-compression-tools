from django.db import models

# Create your models here.


from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    optimized_image = models.ImageField(upload_to='optimized/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    optimized_at = models.DateTimeField(auto_now=True)
    original_size = models.IntegerField(blank=True, null=True) 
    optimized_size = models.IntegerField(blank=True, null=True)  

