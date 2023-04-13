from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def chat_page(request, *args, **kwargs):
    return render(request, "demo/chat_page.html")
