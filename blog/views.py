from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm
from django.shortcuts import redirect

# Create your views here.
#returns blog posts with time < (lte) now to allow for unpublished posts with a future date
#-published_date means descending order
def blog_posts(request):
    posts= Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, "blogposts.html", {'posts':posts})
def post_detail(request, id):
    """
    Create a view that returns a single post object based on the post ID and then render it to the 'postdetail.html'
    template. Or return a 404 error if the post is not found

    """
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    return render(request, "postdetail.html", {'post':post})

def new_post(request):
    if request.method =="POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blogpostform.html',{'form': form})

def edit_post(request,id):
    post=get_object_or_404(Post, pk=id)
    if request.method =="POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blogpostform.html',{'form': form})