from typing import Any
from django.shortcuts import render, get_object_or_404
from .models import About
from django.views.generic import DetailView

class AboutMeView(DetailView):
    model = About
    template_name = "about/about.html"
    context_object_name = "about"

    def get_object(self):
        # Return the latest About object based on the updated_on field
        return About.objects.all().order_by('-updated_on').first()

## original function view code
# def about_me(request):
#     """
#     Renders the About page
#     """
#     about = About.objects.all().order_by('-updated_on').first()

#     return render(
#         request,
#         "about/about.html",
#         {"about": about},
#     )