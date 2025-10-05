from rest_framework import status
from django.shortcuts import render , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category,Product,File
from .serializers import CategorySerializer,ProductSerializer,FileSerializer

class CategoryListView(APIView):
    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

class CategoryDetailView(APIView):
    def get(self,request,pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
           return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)

class ProductListView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class ProductDetailView(APIView):

    def get(self,request,pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
           return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

class FileListView(APIView):
    def get(self,request,product_id):
        files = File.objects.filter(product_id=product_id)
        serializer = FileSerializer(files, many=True, context={'request': request})
        return Response(serializer.data)
class FileDetailView(APIView):
    def get(self,request,product_id,pk):
        try:
            file = File.objects.get(product_id=product_id,pk=pk)
        except File.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FileSerializer(file, context={'request': request})
        return Response(serializer.data)

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.prefetch_related('categories','files').filter(title__icontains=query)
    else:
        products = Product.objects.prefetch_related('categories', 'files').all()
    return render(request, 'product/product_list.html',{'products':products,'query':query})

def product_detail(request,pk):
    product = get_object_or_404(Product, pk=pk)
    files = product.files.filter(is_enabled = True)
    return render(request, 'product/product_detail.html', {'product': product, 'files':files})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'product/category_list.html',{'categories':categories})

def product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'product/product_list.html', {
        'category': category,
        'products': products
    })

def contact_us(request):
    phone_number = "98902366773765"
    return render(request,'product/contact_us.html',{'phone_number':phone_number})

def about_us(request):
    return render(request,'product/about_us.html')

def profile_view(request):
    return render(request,'product/profile_view.html',
                  {
                      'user': request.user })

    User = get_user_model()

    def phone_auth_view(request):
        context = {}
        if request.method == 'POST':
            phone_number = request.POST.get('phone_number')
            if not phone_number:
                context['error'] = 'لطفا شماره تلفن را وارد کنید.'
            else:
                try:
                    user = User.objects.get(phone_number=phone_number)
                    login(request, user)
                    context['user'] = user
                    context['message'] = 'ورود با موفقیت انجام شد.'
                except User.DoesNotExist:
                    context['error'] = 'کاربری با این شماره تلفن یافت نشد.'
        return render(request, 'product/phone_auth_view.html', context)
