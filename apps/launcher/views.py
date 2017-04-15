from django.shortcuts import render


def launcher(request):
    return render(request, 'launcher_index.html', {'user': request.user})
