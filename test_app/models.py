from PIL import Image
from io import BytesIO
from base64 import b64encode
from django.db import models

from utils.arvan_bucket_conf import bucket
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=155)
    price = models.IntegerField()
    main_image = models.BinaryField(null=True,editable=True)
    other_image = models.ImageField(null=True)

    def __str__(self):
        return self.name
    
    def get_main_image(self):
        return b64encode(self.main_image).decode('utf-8')
    
    @staticmethod
    def compress_image(image,thumbnail_size=(400, 400)):
        im = Image.open(image)
        im_io = BytesIO()  # A BytesIO object to hold the image data
        im = im.convert('RGB')  # Ensure image is in RGB mode
        if thumbnail_size:
            im.thumbnail(thumbnail_size)
        im.save(im_io, 'JPEG', quality=40)  # Save the image with specified quality
        return im_io.getvalue()  # Get the bytes of the compressed image
    
    def delete(self,*args,delete_files=False,**kwargs):
        if delete_files:
            bucket.delete_object(self.other_image.name)
        return super().delete(*args,**kwargs)