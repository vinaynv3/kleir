from django.db import models
from PropertyDocs.models import ClientInfo, BankRef
from django.shortcuts import get_object_or_404
from django.urls import reverse
import datetime

"""
Property Images database table
"""

def get_image_filename(instance, filename):
    import datetime
    today = datetime.date.today()
    year,month,day = datetime.date.today().year, datetime.date.today().month, datetime.date.today().day

    try:
        if 'Maps' == type(instance.maps).__name__:
            BankKey = get_object_or_404(type(instance.maps),pk = instance.maps_id)
            Ref_num = get_object_or_404(BankRef,pk = BankKey.connection_id)
            return 'images/{0}/{1}/{2}/{3}/2/{4}'.format(year,month,day,Ref_num.Reference_Number,filename)

    except AttributeError :

        BankKey = get_object_or_404(type(instance.photos),pk = instance.photos_id)
        Ref_num = get_object_or_404(BankRef,pk = BankKey.connection_id)
        return 'images/{0}/{1}/{2}/{3}/1/{4}'.format(year,month,day,Ref_num.Reference_Number,filename)

    else:
        raise Exception('Please check upload_to  attribute ')


class Photos(models.Model):
    # Models attributes (Database columns)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


    #get absolute URL
    def get_absolute_url(self):
        bank = get_object_or_404(BankRef,pk=self.connection_id)
        customer = get_object_or_404(ClientInfo,pk=bank.client_info_id)
        return reverse('doc-maps', kwargs={'slug': customer.Slug,'pk':customer.Client_ID,
                                                'bank_type':bank.Bank_Type,'bank_id':bank.id})


class Images(models.Model):
    photos = models.ForeignKey(Photos, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')

    def __str__(self):
        return str(self.id)



"""
Property maps database table
"""

class Maps(models.Model):
    # Models attributes (Database columns)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    #get absolute URL
    def get_absolute_url(self):
        bank = get_object_or_404(BankRef,pk=self.connection_id)
        customer = get_object_or_404(ClientInfo,pk=bank.client_info_id)
        return reverse('Detail-Page', kwargs={'slug': customer.Slug,'pk':customer.Client_ID,})

class ImageMaps(models.Model):
    maps = models.ForeignKey(Maps, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')


    def __str__(self):
        return str(self.id)
