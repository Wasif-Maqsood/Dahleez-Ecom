from django.shortcuts import render
from .models import Product

def productlist(request):
    products = Product.objects.all()
    template = 'product/product_list.html'
    context = {'product_list': products}  # Fix the context variable name
    return render(request, template, context)

def productdetail(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    template = 'product/product_detail.html'
    context = {'product_detail': product}  # Fix the context variable name
    return render(request, template, context)
