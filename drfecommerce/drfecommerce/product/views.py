from django.db import connection
from django.db.models import Prefetch
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers.sql import SqlLexer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from sqlparse import format

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

# Create your views here.


class CategoryViewSet(viewsets.ViewSet):

    """
    A simple Viewset for viewing all categories
    """

    queryset = Category.objects.all()

    @extend_schema(
        responses=CategorySerializer,
        summary="category",
        description="This endpoint returns a list of all categories.",
    )
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)



class ProductViewSet(viewsets.ViewSet):

    """
    A simple Viewset for viewing all products
    """

    queryset = Product.objects.all().is_active()
    lookup_field = "slug"

    @extend_schema(
        responses=ProductSerializer,
        summary="single product",
        description="This endpoint returns a single product.",
    )
    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug)
            .select_related("category")
            .prefetch_related(
                Prefetch("product_line__product_image"),
                Prefetch("product_line__attribute_value__attribute"),
            ),
            many=True,
        )
        data = Response(serializer.data)
        # q = list(connection.queries)
        # print(len(q))
        # for qs in q:
        #     sqlformatted = format(str(qs["sql"]), reindent=True)
        #     print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))

        return data

    @extend_schema(
        responses=ProductSerializer,
        summary="all products",
        description="This endpoint returns a list of all products.",
    )
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(description="This endpoint returns products by a specific category")
    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<slug>[\w-]+)",
    )
    def list_product_by_category_slug(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(category__slug=slug), many=True
        )
        return Response(serializer.data)
