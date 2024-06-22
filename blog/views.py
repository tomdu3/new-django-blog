from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post


class Postlist(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6

class PostDetailView(generic.DetailView):
    model = Post
    query_set = Post.objects.filter(status=1)
    template_name = "blog/post_detail.html"

    def get_object(self):
        return get_object_or_404(
            self.query_set,
            slug=self.kwargs['slug']
            )

    def get_context_data(self, **kwargs):
        # Get the default context data from the DetailView
        context = super().get_context_data(**kwargs)
        
        # Retrieve the post object
        post = self.get_object()
        
        # Get the comments and comment count
        comments = post.comments.all().order_by("-created_on")
        comment_count = post.comments.filter(approved=True).count()
        
        # Add the comments and comment count to the context
        context['comments'] = comments
        context['comment_count'] = comment_count
        
        return context

## original function view code
# def post_detail(request, slug):
#     """
#     Display an individual :model:`blog.Post`.

#     **Context**

#     ``post``
#         An instance of :model:`blog.Post`.

#     **Template:**

#     :template:`blog/post_detail.html`
#     """
#     queryset = Post.objects.filter(status=1)
#     post = get_object_or_404(queryset, slug=slug)
#     return render(request, "blog/post_detail.html", {"post": post},)