from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

# Create your views here.


def home_redirect(request):
  return redirect('/admin')
