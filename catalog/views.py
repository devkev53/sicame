from django.shortcuts import render
from .models import Brand

# Create your views here.


def render_brand(request):
  brands = Brand.objects.all()
  return render(request, "index.html", {'brands':brands})