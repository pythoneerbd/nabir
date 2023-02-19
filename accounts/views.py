from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from accounts.forms import RegistrationForm, AccountAuthenticateForm, AccountUpdateForm, CreateForm
from blog.models import Category
from .models import Accounts
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#For password change import
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.conf import settings

# Create your views here.
def registration_view(request):
    category = Category.objects.all()
    context = {'category': category, }
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save User data
            # login user with newly register data
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('accounts:profile')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)


def login_view(request):
    category = Category.objects.all()
    context = {'category': category,}
    if request.user.is_authenticated:
        return redirect('blog:index')
    if request.method == 'POST':
        form = AccountAuthenticateForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get("next"))
                else:
                    return redirect('blog:index')
        else:
            context['login_form'] = form
    else:
        form = AccountAuthenticateForm()
        context['login_form'] = form
    return render(request, "accounts/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('blog:index')


@login_required()
def account_view(request):
    category = Category.objects.all()
    context = {'category': category, }
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            context['success_message'] = 'Data Updated'
    else:
        form = AccountUpdateForm(initial={
            'email': request.user.email,
            'username': request.user.username,
            'image': request.user.image.url,
            'name': request.user.name,
            'dob': request.user.dob,
            'address': request.user.address,
            'bio': request.user.bio,
            'phone_number': request.user.phone_number,
        }
        )
    context['account_form'] = form
    return render(request, 'accounts/profile.html', context)

@login_required
def post_create(request):
    category = Category.objects.all()
    if request.user.is_authenticated:
        u = get_object_or_404(Accounts, email=request.user.email)
        form = CreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = u
            instance.save()
            return redirect('blog:index')
        return render(request, 'accounts/post_create.html', {"form": form,'category': category})
    else:
        return redirect('blog:index')

@login_required
def PostUpdate(request, id):
    category = Category.objects.all()
    if request.user.is_authenticated:
        u = get_object_or_404(Accounts, email=request.user.email)
        post = get_object_or_404(Post, id=id)
        form = CreateForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = u
            instance.save()
            messages.success(request, "Post updated successfully")
            return redirect('accounts:author', username=u.username)
        return render(request, 'accounts/post_create.html', {"form": form, 'category': category})
    else:
        return redirect('accounts:login')

@login_required()
def getAuthor(request, username):
    user = get_object_or_404(Accounts, username=username)
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 4 if index >= 4 else 0
    end_index = index + 4 if index <= max_index else max_index
    page_range = paginator.page_range[start_index:end_index]
    category = Category.objects.all()
    context = {
        'posts':posts,
        'author': user,
        'items': items,
        'page_range': page_range,
        'category': category,
    }
    return render(request,'accounts/author_profile.html', context)

def change_password(request):
    category = Category.objects.all()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('blog:index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form,
        'category': category,
    })
