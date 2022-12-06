from django.shortcuts import render


def handle_page_not_found(request, exception):
    return render(request, 'feed/handlers/404.html')


def handle_server_error(request, *args, **kwargs):
    return render(request, 'feed/handlers/500.html')
