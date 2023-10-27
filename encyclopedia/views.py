"""This module contains the view functions of the encyclopedia app."""
from django.shortcuts import render, redirect
from django.urls import reverse
from . import util
import random


def index(request):
    """
        Args:
            request: The request object
        Return:
            Renders list of titles of all entries in the storage, where each title
            is also a link to it's corresponding encyclopedia page. 
    """
    titles = util.list_entries()
    entries = util.titles_urls_dict(titles)

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def display_entry(request, TITLE):
    """
        Args:
            request: request object
            TITLE: The title of the encyclopedia entry.
        Return:
            On success: Renders the contents of an encyclopedia entry.
            On Failure: Renders a "page not found" error page.
    """
    page_content = util.get_entry(TITLE)

    if not page_content:
        return render(request, "encyclopedia/page_not_found.html", status=404)

    return render(request, "encyclopedia/display_entry.html", {
        "page_content": page_content,
        "title": TITLE,
    })


def search(request):
    """
        Args:
            request: The request object
        Return:
            On success: Renders the marching encyclopedia entry.
            On partial success: Renders list of encyclopedia entries that the have
                                query as a substring.
            On failure: Renders a "page not found" error page.
    """
    query = request.GET.get('q')
    page_content = util.get_entry(query)

    if page_content:
        return render(request, "encyclopedia/display_entry.html", {
            "page_content": page_content,
            "title": query
        })

    titles = util.list_entries()
    likely_titles = [title for title in titles if query.lower() in title.lower()]

    if len(likely_titles) > 0:
        entries = util.titles_urls_dict(likely_titles)
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })
    else:
        return render(request, "encyclopedia/page_not_found.html", status=404)


def create_entry(request):
    """
        Args:
            request: The request object
        Return:
            On success: Renders the newly created encyclopedia entry
    """
    if request.method == "GET":
        return render(request, "encyclopedia/create_entry.html")

    if request.method == "POST" :
        title = request.POST.get('title')
        content = request.POST.get('content')

        titles = util.list_entries()

        for entry_title in titles:
            if title.lower() == entry_title.lower():
                return render(request, 'encyclopedia/page_already_exists.html', status=400)

        if '<' in title and '>' in title:
            return render(request, 'encyclopedia/validation_error.html', status=400)

        sanitized_title = util.sanitize_entry(title)
        if '/' in sanitized_title:
            return render(request, 'encyclopedia/validation_error.html', status=400)

        sanitized_content = util.sanitize_entry(content)

        util.save_entry(sanitized_title, sanitized_content)

        return redirect(reverse('get-entry', args=[sanitized_title]), title=sanitized_title)


def edit_entry(request):
    """
        Args:
            request: The request o
    This function renders the encyclopedia entry form."""
    if request.method == 'GET':
        title = request.GET.get('title')
        return render(request, 'encyclopedia/edit_entry.html', {
            "page_content": util.get_entry(title),
            "title": title
        })

    if request.method == "POST" :
        title = request.POST.get('title')
        content = request.POST.get('content')

        sanitized_content = util.sanitize_entry(content)

        util.save_entry(title, sanitized_content)

        return redirect(reverse('get-entry', args=[title]), title=title)


def display_random_entry(request):
    """
        Args:
            request: request object
        Return:
            Renders the content of a randomly selected encyclopedia entry.
    """
    titles = util.list_entries()
    title = random.choice(titles)

    page_content = util.get_entry(title)

    return render(request, "encyclopedia/display_entry.html", {
        "page_content": page_content,
        "title": title,
    })
