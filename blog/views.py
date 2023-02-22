from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404, HttpResponseRedirect
from .models import Category, Post, VideoPost
from .forms import NewCommentForm
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Max


# Create your views here.
def index(request):
    # post = get_object_or_404(Post)
    category = Category.objects.all()
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    try:
        featured_big = Post.published_objects.filter().order_by('-posted')[0]       # query for latest post
    except IndexError:
        featured_big = None
    try:
        featured_medium = Post.published_objects.filter().order_by('-posted')[1:3]  # query for latest 2nd and 3rd post
    except IndexError:
        featured_medium = None
    try:
        featured_small = Post.published_objects.filter().order_by('-posted')[3:8]  # query for latest third to 12th post
    except Indexerror:
        featured_small = None
    most_popular = Post.published_objects.all().order_by('-views')[:4]          # query for 4 most viewed post
    latest_post = Post.published_objects.filter().order_by('-posted')[0:6]  # SHOW latest posts
    bangladesh_category = get_object_or_404(Category, name='Bangladesh')  # query for bangladesh category
    bangladesh_post = Post.published_objects.all().filter(category=bangladesh_category).order_by('-posted')[:6]  # query for bangladesh categorys post
    world_category = get_object_or_404(Category, name='Worlds')  # query for world category
    world_post = Post.published_objects.all().filter(category=world_category).order_by('-posted')[:4]  # query for world category posts
    technology_category = get_object_or_404(Category, name='Technology')  # query for tech category
    technology_post = Post.published_objects.all().filter(category=technology_category).order_by('-posted')[:3]  # query for tech category posts
    sports_category = get_object_or_404(Category, name='Sports')  # query for sports category
    sports_post = Post.published_objects.all().filter(category=sports_category).order_by('-posted')[:3]  # query for sports category posts
    editor_category = get_object_or_404(Category, name='Editors Pick')  # query for editors category
    editor_post = Post.published_objects.all().filter(category=editor_category).order_by('-posted')[:6]  # query for editors category posts
    entertain_category = get_object_or_404(Category, name='Entertainment')  # query for entertainment category
    entertain_post = Post.published_objects.all().filter(category=entertain_category).order_by('-posted')[:3]
    videos = VideoPost.objects.filter().order_by('-posted')[:3]
    context = {
        'category': category,
        # 'post': post,
        'breaking': breaking,
        'featured_big': featured_big,
        'featured_medium': featured_medium,
        'featured_small': featured_small,
        'most_popular': most_popular,
        'videos': videos,
        'latest_post': latest_post,
        'bangladesh_post': bangladesh_post,
        'world_post': world_post,
        'technology_post': technology_post,
        'sports_post': sports_post,
        'editor_post': editor_post,
        'entertain_post': entertain_post,

    }
    return render(request,'blog/index.html', context)

def single_article(request, id, tag_slug=None):
    post = get_object_or_404(Post, pk=id)
    category = Category.objects.all()
    first = Post.published_objects.first()
    last = Post.published_objects.last()
    related = Post.published_objects.filter(category=post.category).exclude(id=id)[:6]
    latest_post = Post.published_objects.filter().order_by('-posted')[0:6]  # SHOW latest posts
    most_popular = Post.published_objects.all().order_by('-views')[:4]  # query for 4 most viewed post
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post = post.filter(tags__in=[tag])
    if post.status == 'published':
        post.views += 1  # clock up the number of post views
        post.save()

    allcomments = post.comments.filter(status=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 3)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return redirect('blog:single_article', id=id)
    else:
        comment_form = NewCommentForm()

    context = {
        'post' : post,
        'tag': tag,
        'first': first,
        'last': last,
        'related': related,
        'category': category,
        'comments': user_comment,
        'comments': comments,
        'comment_form': comment_form,
        'allcomments': allcomments,
        'latest_post': latest_post,
        'most_popular': most_popular,
    }
    return render(request,'blog/single-post.html', context)

def article_category(request, id, slug):
    post_cat = Post.objects.filter(category_id = id)
    category = Category.objects.all()
    topic = get_object_or_404(Category, slug=slug)
    post = Post.published_objects.filter(category=topic.id)
    small_featured_category = Post.published_objects.filter(category=topic.id)[2:12]
    try:
        featured_big = Post.published_objects.filter(category=topic.id)[0]
    except IndexError:
        featured_big = None
    featured_medium = Post.published_objects.filter(category=topic.id)[1:4]
    featured_small = Post.published_objects.filter(category=topic.id)[4:12]
    most_popular = Post.published_objects.filter(category=topic.id).order_by('-views')[:5]  # query for 4 most viewed post
    latest_post = Post.published_objects.filter(category=topic.id).order_by('-posted')[0:5]  # SHOW latest posts
    paginator = Paginator(post, 9)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 2 if index <= max_index else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        'post_cat': post_cat,
        'page_range': page_range,
        'items': items,
        'post': post,
        'category': category,
        'small_featured_category': small_featured_category,
        'featured_big': featured_big,
        'featured_medium': featured_medium,
        'featured_small': featured_small,
        'most_popular': most_popular,
        'latest_post': latest_post,
    }
    return render(request,'blog/catagories-post.html', context)

def search_posts(request):
    all_post = Post.published_objects.all().order_by('-posted')
    category = Category.objects.all()
    query = request.GET.get("q")
    if query:
        all_post = all_post.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(slug__icontains=query)
        ).distinct()
    context = {
        'all_post' : all_post,
        'category': category,
    }
    return render(request, 'blog/search_posts.html', context)


def show_video(request):
    category = Category.objects.all()
    videos = VideoPost.objects.all()
    paginator = Paginator(videos, 6)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 2 if index <= max_index else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        'videos': videos,
        'category': category,
        'page_range': page_range,
        'items': items,
    }
    return render(request, 'blog/video_posts.html', context)

def about_us(request):
    post = "Hello world"
    context = {
        'post' : post,
    }
    return render(request,'blog/about.html', context)


def contact_us(request):
    post = "Hello world"
    context = {
        'post' : post,
    }
    return render(request,'blog/contact.html', context)


