from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages

from .models import Post
from .forms import CommentForm


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
        print('About to render template')

        # Get the default context data from the DetailView
        context = super().get_context_data(**kwargs)
        
        # Retrieve the post object
        post = self.get_object()

        # add comment form 
        comment_form = CommentForm()
        
        # Get the comments and comment count
        comments = post.comments.all().order_by("-created_on")
        comment_count = post.comments.filter(approved=True).count()
        
        # Add the comments and comment count to the context
        context['comments'] = comments
        context['comment_count'] = comment_count
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        print('Received POST request')
        # Retrieve the post object
        post = self.get_object()

        # Process the comment form
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
                )

            # Redirect to the same post detail page after saving the comment
            return redirect('post_detail', slug=post.slug)
        else:
            # If the form is not valid, re-render the detail view with the form errors
            context = self.get_context_data()
            context['comment_form'] = comment_form
            return self.render_to_response(context)

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