from django.shortcuts import redirect, render
from django import forms
import markdown2
from . import util
from random import choice

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    markdown = util.get_entry(entry)
    if not markdown:
        return render(request, "encyclopedia/not_found.html", {
            "entry": entry
        })
    html = markdown2.markdown(markdown)
    return render(request, "encyclopedia/wiki.html", {
        "entry": entry,
        "markdown": html
    })

def search(request):
    entry = request.GET.get("q")
    if not entry:
        return render(request, "encyclopedia/search.html", {"error": "Please enter a search term",})
    entries = util.list_entries()
    results = []
    for e in entries:
        if entry.lower() == e.lower():
            return redirect("encyclopedia:wiki", entry)
        elif entry.lower() in e.lower():
            results.append(e)
    if len(results) == 0:
        return render(request, "encyclopedia/search.html", {
            "error": "No results found",
            "entry": entry})
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "entry": entry
    })

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title", "class": "mb-4 mt-3 form-control w-25"}), label="")
    markdown = forms.CharField(widget=forms.Textarea(attrs={"class": "d-block form-control w-75 mb-4"}), label="")

def add(request):
    if request.method == "GET":
        return render(request, "encyclopedia/add.html", {
            "form": NewEntryForm()
        })
    elif request.method == "POST":
        form = NewEntryForm(request.POST)
        if not form.is_valid():
            return render(request, "encyclopedia/add.html", {
                "form": form,
                "error": "Invalid form"
            })
        title = form.cleaned_data["title"]
        markdown = form.cleaned_data["markdown"]
        already_exists = title.lower() in (string.lower() for string in util.list_entries())
        if already_exists:
            return render(request, "encyclopedia/add.html", {
                "form": NewEntryForm(request.POST),
                "error": "Entry already exists"
            })
        util.save_entry(title, markdown)
        return redirect("encyclopedia:wiki", title)

def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    return redirect("encyclopedia:wiki", entry)

class NewEditForm(forms.Form):
    markdown = forms.CharField(widget=forms.Textarea(attrs={"class": "d-block form-control w-75 mb-4"}), label="")
    title = forms.CharField(widget=forms.HiddenInput())

def edit(request, entry):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "title": entry,
            "form": NewEditForm(initial={"title": entry, "markdown": util.get_entry(entry)})
        })
    elif request.method == "POST":
        form = NewEditForm(request.POST)
        if not form.is_valid():
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "error": "Invalid form"
            })
        title = form.cleaned_data["title"]
        markdown = form.cleaned_data["markdown"]
        util.save_entry(title, markdown)
        return redirect("encyclopedia:wiki", title)
