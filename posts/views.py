import datetime
import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from posts.forms import PostForm
from posts.models import Author, Category, Post
from main.functions import generate_form_errors, paginate_instances
from main.decorators import allow_self


@login_required(login_url="users/login/")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            tags = form.cleaned_data['tags']

            if not Author.objects.filter(user=request.user).exists():
                author = Author.objects.create(
                    user=request.user, name=request.user.username)
            else:
                author = request.user.author

            instance = form.save(commit=False)
            instance.published_date = datetime.date.today()
            instance.author = author
            instance.save()

            tags_list = tags.split(",")
            for tag in tags_list:
                category, created = Category.objects.get_or_create(
                    title=tag.strip())
                instance.categories.add(category)

            response_data = {
                "title": "Successfully submitted",
                "message": "Successfully submitted",
                "status": "success",
                "redirect": "yes",
                "redirect_url": "/",
            }

        else:
            error_message = generate_form_errors(form)
            response_data = {
                "title": "form validation error",
                "message": str(error_message),
                "status": "error",
                "stable": "yes"
            }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        data = {
            "title": "Hello",
            "description": "Hello",
            "short_description": "Hello",
            "time_to_read": "8 min",
            "tags": "technology,programming,coding",
        }
        form = PostForm(initial=data)
        context = {
            "title": "Create new post",
            "form": form,
        }
        return render(request, "posts/create.html", context=context)


@login_required(login_url="users/login/")
def my_posts(request):
    posts = Post.objects.filter(author__user=request.user, is_deleted=False)
    instances = paginate_instances(request, posts, per_page=1)
    context = {
        "title": "My Posts",
        "instances": instances,
    }
    return render(request, "posts/my-posts.html", context=context)


@login_required(login_url="users/login/")
@allow_self
def delete_post(request, id):
    instance = get_object_or_404(Post, id=id)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "title": "Successfully deleted",
        "message": "Post deleted successfully",
        "status": "success",
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="users/login/")
@allow_self
def draft_post(request, id):
    instance = get_object_or_404(Post, id=id)
    instance.is_draft = not instance.is_draft
    instance.save()

    response_data = {
        "title": "Successfully changed",
        "message": "Post updated successfully",
        "status": "success",
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="users/login/")
@allow_self
def edit_post(request, id):
    # Post.objects.filter(id=id,author__user=request.user)
    instance = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():

            tags = form.cleaned_data['tags']

            # if not Author.objects.filter(user=request.user).exists():
            #     author = Author.objects.create(
            #         user=request.user, name=request.user.username)
            # else:
            #     author = request.user.author

            instance = form.save(commit=False)
            # instance.published_date = datetime.date.today()
            # instance.author = author
            instance.save()

            instance.categories.clear()

            tags_list = tags.split(",")
            for tag in tags_list:
                category, created = Category.objects.get_or_create(
                    title=tag.strip())
                instance.categories.add(category)

            response_data = {
                "title": "Successfully submitted",
                "message": "Successfully submitted",
                "status": "success",
                "redirect": "yes",
                "redirect_url": "/",
            }

        else:
            error_message = generate_form_errors(form)
            response_data = {
                "title": "form validation error",
                "message": str(error_message),
                "status": "error",
                "stable": "yes"
            }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        category_string = ""
        for category in instance.categories.all():
            category_string += f"{category.title},"
        form = PostForm(instance=instance, initial={"tags": category_string[:-1]})
        context = {
            "title": "Create new post",
            "form": form,
        }
        return render(request, "posts/create.html", context=context)
