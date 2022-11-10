from django.shortcuts import render

from .models import GeoImage

def index(request):
    # get all GeoImage objects from db
    geo_image_queryset = GeoImage.objects.all()
    geo_image_list = list(geo_image_queryset.values())

    # return request, path, and context dict (to pass in objects)
    return render(request, 'photomapper/index.html', {
        'geo_image_queryset': geo_image_queryset,
        'geo_image_list': geo_image_list,
    })
