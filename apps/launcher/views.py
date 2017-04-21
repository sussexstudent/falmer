from django.shortcuts import render


def launcher(request):
    if request.user.is_authenticated and request.user.authority == 'IS':
        return render(request, 'launcher_index.html', {'user': request.user})
    else:
        return render(request, 'launcher_index_anon.html', {'user': request.user})
