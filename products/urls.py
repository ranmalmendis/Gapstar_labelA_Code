"""autocompany URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products import views as product_views


# Products router
router = DefaultRouter()
router.register(r'products', product_views.ProductViewSet)


urlpatterns = [

    path('', include(router.urls)),
 
   
]
