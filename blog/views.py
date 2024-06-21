from django.shortcuts import render
from django.views import generic
from .models import Post


class Postlist(generic.ListView):
    model = Post
    