import uuid

from django.db import models


class Searcher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet_type = models.CharField(max_length=40, default='cat')
    pet_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200, null=True)
    photo = models.BinaryField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=12, null=True)
    description = models.TextField(null=True)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.pet_name + " " + self.location


class Finder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet_name = models.CharField(max_length=200, null=True)
    pet_type = models.CharField(max_length=40, default='cat')
    photo = models.BinaryField()
    name = models.CharField(max_length=200, null=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=12, null=True)
    description = models.TextField(null=True)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.pet_name + " " + self.location


class SearcherEmbedding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    embedding = models.CharField(max_length=30000, null=False)
    searcher = models.ForeignKey(Searcher, on_delete=models.CASCADE)


class FinderEmbedding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    embedding = models.CharField(max_length=30000, null=False)
    finder = models.ForeignKey(Finder, on_delete=models.CASCADE)
