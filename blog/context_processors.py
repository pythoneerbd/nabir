from .models import Category, Post

def kategorie(request):
    category = Category.objects.all()
    return {"kategorie" : category}


def breaking(request):
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    return {"breaking": breaking}