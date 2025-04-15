from django.contrib import admin
from django.shortcuts import render
from .models import Category, Hub, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    
@admin.register(Hub)
class HubAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    
@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created', 'updated')
    prepopulated_fields = {"slug": ("name",)}