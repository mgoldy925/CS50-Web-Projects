import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


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


# def my_markdown(str):
#     """
#     Reads markdown into HTML text.  Converts headings, boldface, 
#     unordered lists, links, and paragraphs.
#     """
#     VALID_FULL_LINE_CHARS = {
#         '#': '<h1>|<\h1>',
#         '##': '<h2>|<\h2>',
#         '###': '<h3>|<\h3>',
#         '####': '<h4>|<\h4>',
#         '#####': '<h5>|<\h5>',
#         '######': '<h6>|<\h6>',
#         '\n': '<p><\p>',
#         '**|**': '<strong>|<\strong>',

#     }

#     x = "not none"
#     while x is not None:
#         x = re.search("#", str)

# md_str = re.split("\n", str)
# for line in md_str:
    
#     if re.search("^#{1,6}", line):

#         re.search("^#{1,6}", line)