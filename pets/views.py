import base64
import uuid

import numpy as np
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from pets.models import Finder, Searcher, FinderEmbedding, SearcherEmbedding
from pets.serializers import FinderSerializer, FinderCreateIncomingSerializer, SearcherSerializer, \
    SearcherCreateIncomingSerializer
from pets.services import create_embeddings, rank_findings


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
            200: {"id": uuid.uuid4()},
            400: {"description": "desc"}
        }
    )
    def post(request, *args, **kwargs):
        #incoming_data = FinderCreateIncomingSerializer(data=request.data)
        #incoming_data.is_valid(raise_exception=False)
        # val_data = incoming_data.validated_data
        emb = create_embeddings(request.data['photo'])
        request.data['photo'] = base64.b64encode(request.data['photo'].encode("ascii"))
        finder = Finder(**request.data)
        finder.save()
        embedding = FinderEmbedding(finder=finder, embedding="|".join(list(map(str, emb))))
        embedding.save()
        return Response(data={'id': finder.id}, status=status.HTTP_200_OK)


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
        emb = create_embeddings(request.data['photo'])
        request.data['photo'] = base64.b64encode(request.data['photo'].encode("ascii"))
        finder = Searcher(**request.data)
        finder.save()
        embedding = SearcherEmbedding(searcher=finder, embedding="|".join(list(map(str, emb))))
        embedding.save()
        return Response(data={'id': finder.id}, status=status.HTTP_200_OK)


class GetMatchesSearcher(APIView):

    @staticmethod
    @extend_schema()
    def get(request, *args, **kwargs):
        searcher_id = kwargs.get("searcher_id")
        if searcher_id is None:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        elif Searcher.objects.filter(id=searcher_id).first() is None:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        searcher = Searcher.objects.filter(id=searcher_id).first()
        finder_embeddings = list(FinderEmbedding.objects.all())
        search_vector = searcher.searcherembedding_set.first().embedding
        search_vector = np.array(list(map(float, search_vector.split("|"))))
        finder_embeddings = rank_findings(search_vector, finder_embeddings)
        related_finders = [emb.finder for emb in finder_embeddings]
        return Response(
            data=FinderSerializer(related_finders, many=True).data,
            status=status.HTTP_200_OK
        )


class GetMatchesFinder(APIView):
    @staticmethod
    @extend_schema()
    def get(request, *args, **kwargs):
        finder_id = kwargs.get("finder_id")
        if finder_id is None:
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
        elif Finder.objects.filter(id=finder_id).first() is None:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        finder = Finder.objects.filter(id=finder_id).first()
        searcher_embeddings = list(SearcherEmbedding.objects.all())
        search_vector = finder.finderembedding_set.first().embedding
        search_vector = np.array(list(map(float, search_vector.split("|"))))
        finder_embeddings = rank_findings(search_vector, searcher_embeddings)
        related_searchers = [emb.searcher for emb in finder_embeddings]
        return Response(
            data=SearcherSerializer(related_searchers, many=True).data,
            status=status.HTTP_200_OK
        )


finder_view = FinderAPI.as_view()
searcher_view = SearcherAPI.as_view()
searching_matches = GetMatchesSearcher.as_view()
finding_matches = GetMatchesFinder.as_view()
