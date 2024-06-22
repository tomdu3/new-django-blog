from django.shortcuts import render, redirect
from .models import About
from django.views.generic import DetailView
from .forms import CollaborateRequestForm
from django.contrib import messages
class AboutMeView(DetailView):
    model = About
    template_name = "about/about.html"
    context_object_name = "about"

    def get_object(self):
        # Return the latest About object based on the updated_on field
        return About.objects.all().order_by('-updated_on').first()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collaborate_form'] = CollaborateRequestForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CollaborateRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, 'Thank you for your collaboration request!',
            )
            # Redirect to the same about page after saving the form
            return redirect('about')
        else:
            context = self.get_context_data()
            context['collaborate_form'] = form
            return self.render_to_response(context)


# # original function view code
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
