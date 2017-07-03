from django.shortcuts import render

from falmer.frontend.views import application_serve


def launcher(request):
    if request.user.is_authenticated and request.user.authority == 'IS':
        return application_serve(request)
    else:
        return render(request, 'launcher/launcher_index_anon.html', {'user': request.user})
