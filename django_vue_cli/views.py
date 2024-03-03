from django.shortcuts import render


def index(request):
    """
    Renders the index page.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered index page.
    """
    return render(request, "index.prod.html")
