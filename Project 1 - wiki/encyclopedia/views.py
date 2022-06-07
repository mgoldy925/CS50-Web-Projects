from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import choice
from markdown2 import markdown
from . import util

class NewSearchForm(forms.Form):
    # Found documentation online for widgets from StackOverflow
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewEditForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.Textarea(attrs={'rows': '1', 'cols': '40'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'rows': '22', 'cols': '120'}))
    original = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'hidden'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def entry(request, title):
    if title in util.list_entries():
        content = markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "form": NewSearchForm(),
            "entry": content
        })
    else:
        return render(request, "encyclopedia/notfound.html", {
            "form": NewSearchForm()
        })

INVALID_WORDS = ["search", "edit", "random"]
def search(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query not in INVALID_WORDS:
                entries = util.list_entries()
                if query in entries:
                    return HttpResponseRedirect(reverse('entry', args=(query,)))
                else:
                    results = []
                    for entry in entries:
                        if query in entry:
                            results.append(entry)
                    return render(request, "encyclopedia/search_results.html", {
                        "form": NewSearchForm(),
                        "results": results
                    })
        # Found this on StackOverflow for redirecting back to original page
        return HttpResponseRedirect(request.POST.get("next", "/"))
    else:
        return HttpResponseRedirect(reverse('index'))

def edit(request, title=''):
    if request.method == "GET":
        if title in util.list_entries():
            content = util.get_entry(title)
            form = NewEditForm(initial={'title': title, 'content': content, 'original': title})
            return render(request, "encyclopedia/edit.html", {
                "form": NewSearchForm(),
                "edit_form": form,
                "error": False,
                "error_message": ""
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": NewSearchForm(),
                "edit_form": NewEditForm(),
                "error": False,
                "error_message": ""
            })
    elif request.method == "POST":
        form = NewEditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entries = util.list_entries()
            if title in entries:
                if form.cleaned_data["original"] != " ":
                    if form.cleaned_data["title"] == form.cleaned_data["original"]:
                        content = form.cleaned_data["content"]
                        util.save_entry(title, content)
                        return HttpResponseRedirect(reverse('entry', args=(title,)))
            else:
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('entry', args=(title,)))
        return render(request, "encyclopedia/edit.html", {
            "form": NewSearchForm(),
            "edit_form": NewEditForm(request.POST),
            "error": True,
            "error_message": f"{request.POST['title']} already has a Wiki page."
        })

    return HttpResponseRedirect(request.POST.get("next", "/"))

def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    return HttpResponseRedirect(reverse('entry', args=(entry,)))
