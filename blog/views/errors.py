from django.shortcuts import render


def handler404(request, exception):
    template = "errors/404.html"
    # context = {}
    return render(request, template, status=404)