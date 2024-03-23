import base64

from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from pets.models import Finder, Searcher
from pets.serializers import FinderSerializer, FinderCreateIncomingSerializer, SearcherSerializer, \
    SearcherCreateIncomingSerializer


# Create your views here.

class FinderAPI(APIView):

    #parser_classes = (FileUploadParser,)

    @staticmethod
    @extend_schema(
        request=None,
        responses={

        }
    )
    def get(*args, **kwargs):
        finder_objects = FinderSerializer(Finder.objects.all(), many=True)
        return Response(data=finder_objects.data, status=status.HTTP_200_OK)

    @staticmethod
    @extend_schema(
        request=FinderCreateIncomingSerializer,
        responses={
            200: {},
            400: {"description": "desc"}
        }
    )
    def post(request, *args, **kwargs):
        #incoming_data = FinderCreateIncomingSerializer(data=request.data)
        #incoming_data.is_valid(raise_exception=False)
        # val_data = incoming_data.validated_data
        request.data['photo'] = base64.b64encode(request.data['photo'].encode("ascii"))
        finder = Finder(**request.data)
        finder.save()
        return Response(data={}, status=status.HTTP_200_OK)


class SearcherAPI(APIView):

    #parser_classes = (FileUploadParser,)

    @staticmethod
    @extend_schema(
        request=None,
        responses={

        }
    )
    def get(*args, **kwargs):
        finder_objects = SearcherSerializer(Searcher.objects.all(), many=True)
        return Response(data=finder_objects.data, status=status.HTTP_200_OK)

    @staticmethod
    @extend_schema(
        request=SearcherCreateIncomingSerializer,
        responses={
            200: {},
            400: {"description": "desc"}
        }
    )
    def post(request, *args, **kwargs):
        request.data['photo'] = base64.b64encode(request.data['photo'].encode("ascii"))
        finder = Searcher(**request.data)
        finder.save()
        return Response(data={}, status=status.HTTP_200_OK)


finder_view = FinderAPI.as_view()
searcher_view = SearcherAPI.as_view()