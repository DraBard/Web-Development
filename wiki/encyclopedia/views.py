from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import markdown
from django.urls import reverse

from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entries.html", {
            "entry": markdown(util.get_entry(title)), "title": title
            })
    else:
        return render(request, "encyclopedia/error.html")

def search(request):
    user_input = request.GET.get("q")
    # If the user request matches exactly the entry
    if util.get_entry(user_input):
        return render(request, "encyclopedia/entries.html", {
            "entry": markdown(util.get_entry(user_input)), "title": user_input
            })

    # If user entry includes substring of the entry
    substring = []
    for e in util.list_entries():
        if user_input.lower() in e.lower():
            substring.append(e)
    if substring:
        return render(request, "encyclopedia/search.html", {
            "user_input": user_input, 
            "entries": substring
        })
    # No matches
    else:
        return render(request, "encyclopedia/error.html")

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    if request.method == "POST":
        title = request.POST.get("title")
        if title in util.list_entries():
            return HttpResponseRedirect(reverse("encyclopedia:error_create"))
        definition = markdown(request.POST.get("definition"))
        util.save_entry(title, definition, True)
        return render(request, "encyclopedia/entries.html", {
                "entry": markdown(util.get_entry(title)), "title": title
                })

def error_create(request):
    return render(request, "encyclopedia/error_create.html")

def edit(request, title):
    description = util.get_entry(title)
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry": description
        })
    if request.method == "POST":
        definition = request.POST.get("definition")
        util.save_entry(title, definition)
        return render(request, "encyclopedia/entries.html", {
                "entry": markdown(util.get_entry(title)), "title": title
                })     

def random_page(request):
    title = random.choice(util.list_entries())
    return render(request, "encyclopedia/entries.html", {
        "entry": markdown(util.get_entry(title)),
        "title": title
        })  





