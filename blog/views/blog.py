from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from taggit.models import Tag

from blog.models import Post, PostCategory, Comment
from blog.forms import EmailPostForm, CommentPostForm, PostCategoryForm, PostForm


# TODO: Refactor project and place view functions into different files to encourage project scaling 

def index(request):
    """
    Returns the homepage html
    :param request: -   Request object
    """
    template = "index.html"
    # categories = PostCategory.approved.all()
    posts = Post.objects.all().order_by('-views')
    tags = Tag.objects.all()[:9]
    if len(posts) >= 2:
        featured_posts = posts[:2]
    else:
        featured_posts = None
    context = {
        # 'categories': categories,
        'home_active': 'active',
        "posts": featured_posts,
        "tags": tags
    }
    return render(request, template, context)


@login_required
def my_stories(request):
    """
    Returns stories (post) written by the author(request.user)
    :params request:
    """
    template = "blog/posts/my_stories.html"
    _my_stories = Post.objects.filter(active=True, author__id=request.user.pk).order_by('-published_date')
    paginator = Paginator(_my_stories, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        "posts": posts,
        "page": page,
    }
    return render(request, template, context)


def posts_page(request, slug):
    template = "blog/posts/explore.html"
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
        "page": page,
        "explore_active": "active"
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
    paginator = Paginator(object_list, 4)   # 6 post in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    template = "blog/posts/explore.html"
    # import pdb; pdb.set_trace()
    context = {
        "posts": posts,
        "explore_active": "active"
    }
    return render(request, template, context)


def post_by_tag(request, slug):
    template = "blog/posts/explore.html"
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'posts': posts
    }
    return render(request, template, context)


@login_required
def post_add(request):
    if request.method == "POST":
        request.POST = request.POST.copy()
        request.POST["author"] = request.user.pk 
        # request.POST["status"] = "published"
        form = PostForm(request.POST, request.FILES)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            instance = form.save()
            # import pdb; pdb.set_trace()
            if request.POST["action"] == "published":
                return redirect(instance.get_absolute_url())
            elif request.POST["action"] == "draft":
                return redirect(reverse("blog:my_stories"))
    template = "blog/posts/new_post.html"
    
    form = PostForm()
    tags = Tag.objects.all()
    # import pdb; pdb.set_trace()

    categories = PostCategory.approved.all()
    context = {
        "form": form,
        "categories": categories,
        "tags": tags
        }
    return render(request, template, context)


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(Post, instance=post)

    if request.user == post.author:

        if request.method == "POST":
            request.POST = request.POST.copy()
            request.POST['author'] = request.user.pk
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
            else:
                import pdb; pdb.set_trace()

        template = "blog/posts/edit_post.html"
        context = {
            "form": form,
            "post": post
        }
        return render(request, template, context)
    else:
        import pdb; pdb.set_trace()


def post_detail(request, year, month, day, slug):
    """
    This function based view gets a particular post with the parameters below
    :param request:
    :param year:
    :param month:
    :param day:
    :param post:
    :return:
    """
    template = "blog/posts/post.html"
    form = CommentPostForm(request.GET)
    post = get_object_or_404(
        Post, slug=slug,
        status='published',
        published_date__year=year,
        published_date__month=month,
        published_date__day=day
    )
    session_key = "viewed story {slug}"
    if not request.session.get(session_key, False):
        post.views += 1
        post.save()
        request.session[session_key] = True
        
    related_posts = post.tags.similar_objects()

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None
    # if request.method == "POST":
    #     request.POST = request.POST.copy()
    #     request.POST["name"] = request.user.username
    #     request.POST["email"] = request.user.email
    #     comment_form = CommentPostForm(request.POST)
    #     if comment_form.is_valid():
    #         new_comment = comment_form.save(commit=False)
    #         new_comment.post = post
    #         new_comment.save()
    #         return redirect(post.get_absolute_url())
    # else:
    comment_form = CommentPostForm(request.GET)
    # form = EmailPostForm(request.GET)
    context = {
        "post": post,
        "related_posts": related_posts,
        "form": form,
        "comment_form": comment_form,
        "new_comment": new_comment,
        "comments": comments
    }
    return render(request, template, context)


@login_required
def delete_post(request, year, month, day, slug):
    """
    A view function that deletes a story.
    It sets story to be inactive rather that deleting
    :params year:
    :params month:
    :params day:
    :params slug:
    :return:
    """
    post = get_object_or_404(
        Post,
        slug=slug,
        published_date__year=year,
        published_date__month=month,
        published_date__day=day
    )
    if request.user == post.author:
        post.active = False
        post.save()
        previous_url = request.META.get('HTTP_REFERER')
        return redirect(previous_url)
    else:
        import pdb; pdb.set_trace()


@login_required
@csrf_exempt
def add_post_comment(request, slug):
    """
    A view function that adds a comment to a post
    :params year:
    :params month:
    :params day:
    :params slug:
    :return:
    """
    if request.method == "POST":
        post = get_object_or_404(
            Post,
            slug=slug
        )
        form = CommentPostForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            # import pdb; pdb.set_trace()
            comment.save()
            data = dict(form.cleaned_data)
            return JsonResponse(data,  content_type="application/json")
        else:
            import pdb; pdb.set_trace()
            

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


def subscribe(request):
    """
    Add email to the list of subscribers
    """
    if request.method == "POST":
        email = request.POST.get("email")
        # TODO: Send email here
        template = "blog/subscribed.html"
        context = {
            "email": email
        }
        return render(request, context, template)