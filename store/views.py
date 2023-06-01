from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
# from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Product, Collection, OrderItem
from .serializers import ProductSerializer, CollectionSerialer


""" 
Base class for getting product list and creating product list.
Here we inherited APIView class
Then we can define get() and post() methods to 
perform getting and creating products
"""
# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             queryset, many=True, context={'request': request}
#         ) # serialization
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data) # de-serialization
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


""" 
Base class for getting product list and creating product list.
Here we inherited ListCreateAPIView generics class
Here we have to override generic classes methods
get_queryset() -- for getting queryset
get_serializer_class() -- for define the serializer
get_serializer_context() -- for define the serializer context
"""
# class ProductList(ListCreateAPIView):
#     def get_queryset(self):
#         return Product.objects.select_related('collection').all()
    
#     def get_serializer_class(self, *args, **kwargs):
#         return ProductSerializer
    
#     def get_serializer_context(self):
#         return { 'request': self.request }
    

""" 
Base class for getting product list and creating product list.
Here we inherited ListCreateAPIView generics class
Here we defined queryset and serializer_class
withouth overriding the generic class methods
get_queryset() -- for getting queryset
get_serializer_class() -- for define the serializer
get_serializer_context() -- for define the serializer context
"""
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
#     def get_serializer_context(self):
#         return { 'request': self.request }

""" 
Base class for getting, deleting and update one product at one time.
Here we inherited APIView class
Then we can define get(), delete() and put() methods
"""
# class ProductDetails(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product) # serialization
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data) # de-serialization
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

""" 
Base class for getting, deleting and update one product at one time
Here we inherited RetrieveUpdateDestroyAPIView generics class
Here we defined queryset and serializer_class
withouth overriding the generic class methods
get_queryset() -- for getting queryset
get_serializer_class() -- for define the serializer
get_serializer_context() -- for define the serializer context
"""
# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = 'id' we can use this if we use path('products/<int:id>/'
    
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

""" 
Base class for
getting product list and creating product list and
getting, deleting and update one product at one time
Here we inherited ModelViewSet generics class
Here we defined queryset and serializer_class
withouth overriding the generic class methods
get_serializer_context() -- for define the serializer context
delete() -- overide the delete method
"""
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return { 'request': self.request }
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs)


""" 
Base function for getting collection list and creating coleection list.
"""
# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(
#              products_count=Count('products')).all()
#         serializer = CollectionSerialer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerialer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
""" 
Base class for getting collection list and creating colection list.
Here we inherited ListCreateAPIView generics class
Here we defined queryset and serializer_class
withouth overriding the generic class methods
get_queryset() -- for getting queryset
get_serializer_class() -- for define the serializer
get_serializer_context() -- for define the serializer context
"""
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()
#     serializer_class = CollectionSerialer

#     def get_serializer_context(self):
#         return { 'request': self.request }

""" 
Base function for getting collection list and creating coleection list.
"""
# @api_view(['GET', 'PATCH', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(products_count=Count('products')),
#         pk=pk
#     )
    
#     if request.method == 'GET':
#         serializer = CollectionSerialer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PATCH':
#         serializer = CollectionSerialer(collection,  data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error': 'COllection cannot be deleted!'})
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

""" 
Base class for getting, deleting and update one collection at one time
Here we inherited RetrieveUpdateDestroyAPIView generics class
Here we defined queryset and serializer_class
withouth overriding the generic class methods
get_queryset() -- for getting queryset
get_serializer_class() -- for define the serializer
get_serializer_context() -- for define the serializer context
"""
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products'))
#     serializer_class = CollectionSerialer

#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted!'})
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


""" 
Base class for
getting collection list and creating collection list and
getting, deleting and update one collection at one time
Here we inherited ModelViewSet generics class
Here we defined queryset and serializer_class
withouth overriding the generic class methods
get_serializer_context() -- for define the serializer context
delete() -- overide the delete method
"""
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerialer

    def get_serializer_context(self):
        return { 'request': self.request }

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted!'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)