from django.shortcuts import render, get_object_or_404
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .forms import *
from django.contrib import messages
from PropertyDocs.models import *
from .models import *

"""
View functions below create and update property images
"""

#Property interior images creation
@login_required
def PhotoView(request,*args,**kwargs):

    #Create Formset object
    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm, extra=4)

    if request.method == 'POST':
        photos = PhotoForm(request.POST)
        images = ImageFormSet(request.POST,request.FILES)

        #Below condition saves new images to customer database
        if photos.is_valid() and images.is_valid():
            photo_instance = photos.save(commit=False)
            photo_instance.connection_id = kwargs['bank_id']
            photo_instance.save()

            for image in images.cleaned_data:
                if image:
                    get_image = image['image']
                    image_instance = Images(photos = photo_instance, image = get_image)
                    image_instance.save()
            messages.success(request, 'Images uploaded successfully')
            return HttpResponseRedirect(reverse('doc-maps',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))
        else:
            messages.error(request, 'Oops!! Something went wrong, please try again.')

    else:
        postForm = PhotoForm()
        formset = ImageFormSet(queryset=Images.objects.none())
        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        return render(request, 'ImageUpload/Photo.html',
                  {'postForm': postForm, 'formset': formset,'customer':customer,'bank':bank,})


# Update Property interior images
@login_required
def PhotoUpdate(request,*args,**kwargs):
    photo = get_object_or_404(Photos,pk =kwargs['photo_id'])
    images = photo.images_set.all()

    ImageFormSet = modelformset_factory(Images,
                                form=ImageForm, extra=0)

    if request.method == 'POST':
        photos = PhotoForm(request.POST, instance = photo)
        images = ImageFormSet(request.POST or None,request.FILES or None)

        #Below condition update & saves new images to customer database
        if photos.is_valid() and images.is_valid():
            photo_instance = photos.save(commit=False)
            photo_instance.save()


            for image in images.cleaned_data:
                if image:
                    request_image = image['image']
                    Image_object = Images.objects.get(pk = image['id'].id)
                    Image_object.image = request_image
                    Image_object.save()

            messages.success(request, 'Images updated successfully')
            return HttpResponseRedirect(reverse('Detail-Page',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],}))
        else:
            messages.error(request, 'Oops!! Something went wrong, please try again.')
    else:
        postForm = PhotoForm(instance = photo)
        formset = ImageFormSet(queryset = images)
        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        return render(request, 'ImageUpload/Photo.html',
              {'postForm': postForm,'formset': formset, 'customer':customer,'bank':bank,'document':photo})

#Property exterior images creation
@login_required
def MapsView(request,*args,**kwargs):

    ImageFormSet = modelformset_factory(ImageMaps,
                                        form=ImageMapsForm, extra=4)

    if request.method == 'POST':
        photos = MapsForm(request.POST)
        images = ImageFormSet(request.POST,request.FILES,)

        #Below condition saves new images to customer database
        if photos.is_valid() and images.is_valid():
            photo_instance = photos.save(commit=False)
            photo_instance.connection_id = kwargs['bank_id']
            photo_instance.save()

            for image in images.cleaned_data:
                if image:
                    get_image = image['image']
                    image_instance = ImageMaps(maps = photo_instance, image = get_image)
                    image_instance.save()
            messages.success(request, 'Images uploaded successfully')
            return HttpResponseRedirect(reverse('Detail-Page',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],}))
        else:
            messages.error(request, 'Oops!! Something went wrong, please try again.')

    else:
        postForm = MapsForm()
        formset = ImageFormSet(queryset=Images.objects.none())
        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        return render(request, 'ImageUpload/maps.html',
                  {'postForm': postForm, 'formset': formset,'customer':customer,'bank':bank,})


# Update Property exterior images
@login_required
def MapsUpdate(request,*args,**kwargs):

    #Create Formset object
    map = get_object_or_404(Maps,pk =kwargs['map_id'])
    images = map.imagemaps_set.all()
    ImageFormSet = modelformset_factory(ImageMaps,
                                        form=ImageMapsForm, extra=0)

    if request.method == 'POST':
        maps = MapsForm(request.POST, instance = map)
        map_images = ImageFormSet(request.POST or None,request.FILES or None)

        #Below condition saves new images to customer database
        if maps.is_valid() and map_images.is_valid():
            maps_instance = maps.save(commit=False)
            maps_instance.connection_id = kwargs['bank_id']
            maps.save()

            for image in map_images.cleaned_data:
                if image:
                    request_image = image['image']
                    Image_object = ImageMaps.objects.get(pk = image['id'].id)
                    Image_object.image = request_image
                    Image_object.save()

            messages.success(request, 'Images updated successfully')
            return HttpResponseRedirect(reverse('Detail-Page',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],}))
        else:
            messages.error(request, 'Oops!! Something went wrong, please try again.')

    else:
        postForm = MapsForm(instance = map)
        formset = ImageFormSet(queryset=images)
        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        return render(request, 'ImageUpload/maps.html',
                  {'postForm': postForm, 'formset': formset,'customer':customer,'bank':bank,'document':map})
