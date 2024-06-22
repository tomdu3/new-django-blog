from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Comment
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

class CommentEditView(generic.UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/post_detail.html"

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.object.post.slug})

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.approved = False  # Mark the comment as unapproved after editing
        comment.save()
        messages.success(self.request, 'Comment updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating comment!')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=post_slug)
        context['post'] = post
        return context

    def get_object(self, queryset=None):
        comment_id = self.kwargs['comment_id']
        post_slug = self.kwargs['slug']
        queryset = queryset or self.get_queryset()
        return get_object_or_404(queryset, pk=comment_id, post__slug=post_slug)

    def get_queryset(self):
        return Comment.objects.all()
    

def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))