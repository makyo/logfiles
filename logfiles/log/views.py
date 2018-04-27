from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def app(request):
    return render(request, 'app.html')
