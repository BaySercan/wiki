from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from . import util
from django.http import HttpResponse
import markdown2
import random

class NewEntry(forms.Form):
    title = forms.CharField(label="Entry Title", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'style':'margin-bottom:15px;'}))
    entry = forms.CharField(label="Entry Body", max_length=300, widget=forms.Textarea(attrs={'class': 'form-control'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "h1": "All Pages",
    })

def wiki(request, title=None):
    if title == None or title == " ":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "error": "Choose an entry to check it out",
            "h1": "All Pages",
        })

    titleContent = util.get_entry(title)

    if titleContent is not None:
        return render(request, "encyclopedia/content.html", {
            "title": title,
            "content": markdown2.markdown(titleContent),
        })
    else:
        return HttpResponse(f"No entries for '{title}'")

def searchEntry(request):
    q = request.POST.get("q")

    if not q:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "h1": "All Pages",
        })

    query = util.get_entry(q)

    if query is not None:
        return render(request, "encyclopedia/content.html", {
            "title": q,
            "content": markdown2.markdown(query),
        })

    else:
        allEntries = util.list_entries()

        possibleEntries = [entry for entry in allEntries if str(q).lower() in str(entry).lower()]

        if len(possibleEntries) > 0:
            return render(request, "encyclopedia/index.html", {
                "entries": possibleEntries,
                "error": "Did you mean one of the below entries?",
                "h1": "Possible entries for your search " + "'" + str(q) + "'",
            })

        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "error": "No entries found for your query, you may choose one from below list",
                "h1": "All Pages",
            })

def create(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]

            allEntries = util.list_entries()

            for e in allEntries:
                if str(title).lower() == e.lower():
                    return render(request, "encyclopedia/create.html", {
                        "form": form,
                        "error": "This entry title already exist",
                    })

            util.save_entry(title, entry)

            return HttpResponseRedirect(reverse('encyclopedia:wiki', kwargs={'title': title}))

        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })

    return render(request, "encyclopedia/create.html", {
        "form": NewEntry()
    })

def update(request, title=None):

    if title == None or title == " ":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "error": "Choose an entry to check it out",
            "h1": "All Pages",
        })

    if request.method == "POST":
        form = NewEntry(request.POST)

        if form.is_valid:
            title = form.data["title"]
            entry = form.data["entry"]

            util.save_entry(title, entry)

            return HttpResponseRedirect(reverse('encyclopedia:wiki', kwargs={'title': title}))
        else:
            return render(request, "encyclopedia/update.html", {
                "form": form
            })

    else:
       
        entry = util.get_entry(title)
        # form = NewEntry(request.GET)

        data = {'title': title,
                'entry': entry}

        form = NewEntry(data, initial=data)

        # form.fields["title"] = title
        # form.fields["entry"] = entry

        return render(request, "encyclopedia/update.html" ,{
                    "form": form,
                    "title": title,
                }) 

def randomEntry(request):
    allEntries = util.list_entries()

    rE = random.choice(allEntries)

    rEcontent = util.get_entry(rE)

    return render(request, "encyclopedia/content.html", {
            "title": rE,
            "content": markdown2.markdown(rEcontent),
        })