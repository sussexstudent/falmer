from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import MagicLinkToken


def magic_link_login(request, token):
    try:
        magic = MagicLinkToken.objects.get(token=token, used=False)
    except MagicLinkToken.DoesNotExist:
        return JsonResponse({'error': 'Token not found'})

    magic.used = True
    magic.save()

    login(request, magic.user)

    return redirect('/cms')
