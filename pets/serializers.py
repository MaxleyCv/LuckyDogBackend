import base64

from rest_framework import serializers

from pets.models import Finder, Searcher


class FinderSerializer(serializers.ModelSerializer):

    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        return base64.b64decode(obj.photo).decode('ascii')

    class Meta:
        model = Finder
        fields = '__all__'


class SearcherSerializer(serializers.ModelSerializer):

    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        return base64.b64decode(obj.photo).decode('ascii')

    class Meta:
        model = Searcher
        fields = '__all__'



class FinderCreateIncomingSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    pet_name = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    email = serializers.EmailField(allow_null=True)
    phone_number = serializers.CharField(max_length=12, allow_null=True)
    location = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    photo = serializers.CharField(required=True, max_length=2000000)


class SearcherCreateIncomingSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    pet_name = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    email = serializers.EmailField(allow_null=True)
    phone_number = serializers.CharField(max_length=12, allow_null=True)
    location = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    photo = serializers.CharField(required=True, max_length=2000000)

