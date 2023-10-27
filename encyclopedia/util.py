import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.urls import reverse
import bleach


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def titles_urls_dict(list_titles):
    """
    Returns a dictionary that contains key and value pairs for title and
    url of each encyclopedia entry, identified by their titles in a list.  
    """
    entries = []
    for title in list_titles:
        entries.append({
            'title': title,
            'entry_url': reverse('get-entry', args=[title])
        })

    return entries


def sanitize_entry(data):
    """
    This function ensures strips disallowed html tags from a text data
    """
    allowed_tags = [
            'a', 'p', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2',
            'h3', 'h4', 'h5', 'h6', 'b'
        ]
    allowed_attributes = {'a': ['href', 'title']}

    sanitized_data = bleach.clean(data, tags=allowed_tags, 
                                  attributes=allowed_attributes)
    return sanitized_data
