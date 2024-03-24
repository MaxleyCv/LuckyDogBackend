from django.contrib import admin

from pets.models import Finder, Searcher, SearcherEmbedding, FinderEmbedding

# Register your models here.

admin.site.register(Finder)
admin.site.register(Searcher)
admin.site.register(FinderEmbedding)
admin.site.register(SearcherEmbedding)
