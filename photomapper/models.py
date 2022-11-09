from django.db import models
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

import boto3
import requests


def transfer_s3_to_RDS():
    """
    Function used to download existing images from an AWS S3 bucket
    and transfer image information into the project database as 
    GeoImage objects
    """
    s3_resource = boto3.resource('s3')
    BUCKET_NAME = 'silicaowl-website-photos'
    AWS_REGION = 'us-east-2'
    pct_photo_bucket = s3_resource.Bucket(BUCKET_NAME)
    print("Loading objects from: ", pct_photo_bucket.name)

    for s3_object in pct_photo_bucket.objects.all():
        s3_object_url = "https://{}.s3.{}.amazonaws.com/{}".format(BUCKET_NAME, AWS_REGION, s3_object.key)
        image_name = "{}".format(s3_object.key)

        # create new GeoImage object, to be stored in database
        GeoImage.objects.create_geo_image(s3_object_url, image_name)
        print("Created GeoImage object from", image_name)
        
        
class GeoImageManager(models.Manager):
    """
    Given a url and name (string) of an image, get GPS latitude and 
    longitude data and create new GeoImage object
    """
    def create_geo_image(self, url, name):
        response = requests.get(url, stream=True)
        image = Image.open(response.raw)
        exif_data = self._get_exif_data(image)
        lat, lon = self._get_coordinates(exif_data)
        geo_image = self.create(url=url, name=name, lat=lat, lon=lon)
        return geo_image

    def _get_exif_data(self, image):
        """
        Returns a dictionary from the exif data of a PIL Image item.
        Also converts the GPS Tags
        """
        exif_data = {}
        info = image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for gps_tag in value:
                        sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                        gps_data[sub_decoded] = value[gps_tag]
                    
                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value

        return exif_data

    def _convert_to_degrees(self, value):
        """
        Helper function to convert GPS coordinates stored in EXIF data to degrees in float format
        """
        print("Value given to _convert_to_degrees: ", value)
        d = value[0]
        m = value[1]
        s = value[2]
        return d + (m / 60.0) + (s / 3600.0)

    def _get_coordinates(self, exif_data):
        """
        Returns the latitude and longitude, if available, from provided exif_data
        obtained through get_exif_data above
        """
        # If no exif data, lat and lon set to 0.00
        lat = 0.00
        lon = 0.00

        if "GPSInfo" in exif_data:
            gps_info = exif_data["GPSInfo"]
            gps_latitude = gps_info.get("GPSLatitude")
            gps_latitude_ref = gps_info.get("GPSLatitudeRef")
            gps_longitude = gps_info.get("GPSLongitude")
            gps_longitude_ref = gps_info.get("GPSLongitudeRef")

            # print GPS latitude for testing
            print("GPS Latitude: ", gps_latitude)
            print("GPS Longitude: ", gps_longitude)

            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = self._convert_to_degrees(gps_latitude)
                if gps_latitude_ref != "N":
                    lat *= -1

                lon = self._convert_to_degrees(gps_longitude)
                if gps_longitude_ref != "E":
                    lon *= -1

        print("CONVERTED LAT: ", lat)
        print("CONVERTED LON: ", lon)
        return (lat, lon)


class GeoImage(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()

    objects = GeoImageManager()       

    def __str__(self):
        return self.name

    def get_gps_lat(self):
        return self.lat

    def get_gps_lon(self):
        return self.lon
