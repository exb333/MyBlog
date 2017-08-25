from urllib.parse import quote_plus
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import Post
from .forms import PostForm

# Create your views here.


def home(request):
    return render(request, "base.html", {})

def post_detail(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.content)
    context = {
        "instance" : instance,
        "share_string": share_string,
    }
    return render(request, 'post_detail.html', context)


def post_create(request):
    if not request.user.is_staff or not request.user.is_authenticated:
        raise Http404

    heading = "Create New Posts"
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())


    elif form.errors:
        messages.error(request, "NOT Successfully Created")
    context = {
        'form':form,
        'heading':heading,
    }
    return render(request, 'post_form.html', context)


def post_list(request):
    queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
        )

    paginator = Paginator(queryset_list, 3)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    if not queryset_list:
        no_results = "No Results Found"
        context = {"no_results": no_results, }
    else:
        context = {
            "object_list": queryset,
        }
    return render(request, 'index.html', context)


def post_update(request, slug):
    if not request.user.is_staff or not request.user.is_authenticated:
        raise Http404
    heading = "Update Post"
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())


    elif form.errors:
        messages.error(request, "NOT Successfully Updated")

    context = {
        "instance": instance,
        "form": form,
        "heading": heading,
    }
    return render(request, 'post_form.html', context)


def post_delete(request, slug):
    if not request.user.is_staff or not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Deleted Successfully")
    return redirect("posts:list")
