from sitetree.models import Tree, TreeItem

def header(title, parent):
    return dict(title=title,
                parent=parent,
                hint="header",
                url="placeholder")

def divider(parent):
    return dict(title="Divider",
                parent=parent,
                hint="divider",
                url="placeholder")


tree, created = Tree.objects.get_or_create(alias='radio_tree')

tree_items = [
    dict(title="News", hint="icon-globe", url="radio-news"),
    dict(title="Playlist", hint="icon-list", url="radio-playlist"),
    dict(title="Submit Track", hint="icon-arrow-up", url="radio-submit"),
    dict(title="Request", hint="icon-bullhorn", url="radio-search"),
    dict(title="More", url="/more/", urlaspattern=False),
    dict(title="IRC", hint="icon-comment", url="radio-irc", parent="More"),
    dict(title="Favourites", hint="icon-heart", url="radio-faves", parent="More"),
    divider(parent="More"),
    header("About", parent="More"),
    dict(title="Staff", hint="icon-user", url="radio-staff", parent="More"),
    dict(title="Stats", hint="icon-info-sign", url="radio-stats", parent="More"),
]

if created:
    default = dict(
            tree=tree,
            urlaspattern=True,
            )

    for item in tree_items:
        # Make sure we resolve parent strings
        if item.get('parent', None):
            item['parent'] = TreeItem.objects.get(title=item['parent'], tree=tree)

        info = dict(
                tree=tree,
                urlaspattern=True,
                )
        info.update(item)

        TreeItem.objects.create(**info)
