from django import forms
from ImageUpload.models import *

"""
Images Upload model form
"""

#PHOTOS
class PhotoForm(forms.ModelForm):

    title = forms.CharField(max_length=200)

    class Meta:
        model = Photos
        fields = ('title',)

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Images
        fields = ('image', )


#MAPS
class MapsForm(forms.ModelForm):

    title = forms.CharField(max_length=200)

    class Meta:
        model = Maps
        fields = ('title',)

class ImageMapsForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = ImageMaps
        fields = ('image', )
