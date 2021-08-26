from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def permission_denied_view(request, exception):
    message = "You don't have access to this page. Contact account administrator."
    return render(request, '403.html', {'message': message})
