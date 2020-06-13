from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post, PostCategory
from .forms import EmailPostForm, CommentPostForm, PostCategoryForm, PostForm


# TODO: Refactor project and place view functions into different files to encourage project scaling 

def index(request):
    template = "index.html"
    categories = PostCategory.approved.all()
    context = {
        'categories': categories
    }
    return render(request, template, context)


def posts_page(request, slug):
    template = "blog/post/list.html"
    object_list = Post.objects.filter(category__slug=slug)
    paginator = Paginator(object_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts,
        "page": page
    }
    return render(request, template, context)


class PostListView(ListView):
    """
    This is a Class Based View, It has the exact same functionality as the
    function based view below post_list(request)
    """
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 6
    template_name = "blog/post/list.html"


def post_list(request):
    """
    This is a function based view, It has the exact same functionality as the
    Class Based View above PostListView.
    :param request:
    :return:
    """
    object_list = Post.published.all()
    paginator = Paginator(object_list, 6)   # 6 post in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    template = "blog/post/list.html"
    # import pdb; pdb.set_trace()
    context = {
        "posts": posts,
        "page": page
    }
    return render(request, template, context)


def post_add(request):
    if request.method == "POST":
        request.POST = request.POST.copy()
        request.POST["author"] = request.user.pk 
        request.POST["status"] = "published"
        form = PostForm(request.POST, request.FILES)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            instance = form.save()
            return redirect(instance.get_absolute_url())
    template = "blog/post/add.html"
    form = PostForm()

    categories = PostCategory.approved.all()
    context = {
        "form": form,
        "categories": categories
        }
    return render(request, template, context)


def post_detail(request, year, month, day, post):
    """
    This function based view gets a particular post with the parameters below
    :param request:
    :param year:
    :param month:
    :param day:
    :param post:
    :return:
    """
    template = "blog/post/detail.html"
    post = get_object_or_404(
        Post, slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None
    if request.method == "POST":
        request.POST = request.POST.copy()
        request.POST["name"] = request.user.username
        request.POST["email"] = request.user.email
        comment_form = CommentPostForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentPostForm(request.GET)
        form = EmailPostForm(request.GET)
        context = {
            "post": post,
            "form": form,
            "comment_form": comment_form,
            "new_comment": new_comment,
            "comments": comments
        }
        return render(request, template, context)


def post_share(request, year, month, day, post):
    """
    A View function that shares posts via email
    :param request:
    :param year:
    :param month:
    :param day:
    :param post:
    :return:
    """
    post = get_object_or_404(Post,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             status='published')
    template = "blog/post/share.html"
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            cd = form.cleaned_data
            # TODO: Send the email
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['first_name']} {cd['last_name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@kaliblog.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
        context = {
            "post": post,
            "form": form,
            "sent": sent
        }
        return render(request, template, context)


###################################################
#           Category View Functions
###################################################
def add_category(request):
    """
    A View Function that adds a category for POST request and returns category add template for get request
    :param request
    """
    if request.method == "POST":
        form = PostCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.approve = True
            instance.save()
            return redirect("home")
    
    template = "blog/post_category/add.html"
    form = PostCategoryForm()
    context = {
        "form": form
    }
    return render(request, template, context)
