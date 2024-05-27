from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .forms import ProductForm


def home(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products':products})

def save_product(request):
    form = ProductForm()
        
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.main_image = Product.compress_image(form.cleaned_data.get('main_image'))
            
            obj.save()
            return HttpResponse('save successfully')
        else:
            print(form.errors)
            return HttpResponse('failed')
    
    return render(request,'save_product.html',{'form':form})

def delete_product(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        product = Product.objects.get(id=id)
        product.delete(delete_files=True)
        return HttpResponse('obj delete with file.')
    
    return render(request,'delete.html')


class ApiHome(APIView):
    def get(self,request):
        return Response("Hello DRF")
