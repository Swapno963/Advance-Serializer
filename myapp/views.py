from django.shortcuts import get_object_or_404
from myapp.serializers import * 
from myapp.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def product_list_basic(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_list_detail(request):
    products = Product.objects.all()
    serializer = DetailedUserSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# SHOW COMMENTS
@api_view(['GET'])
def artical_list_basic(request):
    products = Article.objects.all()
    serializer = ArticleSerializer(products, many=True)
    return Response(serializer.data)