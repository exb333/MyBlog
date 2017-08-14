from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import Post
from .forms import PostForm

# Create your views here.


def home(request):
    return render(request, "base.html", {})

def post_detail(request, id):
    instance = get_object_or_404(Post, id=id)
    context = {
        "instance" : instance,
    }
    return render(request, 'post_detail.html', context)


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())


    elif form.errors:
        messages.error(request, "NOT Successfully Created")
    context = {
        'form':form,
    }
    return render(request, 'post_form.html', context)


def post_list(request):
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
    }
    return render(request, 'index.html', context)


def post_update(request, id):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
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
    }
    return render(request, 'post_form.html', context)


def post_delete(request, id):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Deleted Successfully")
    return redirect("posts:list")
