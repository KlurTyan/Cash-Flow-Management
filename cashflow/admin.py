from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Status, Type, Category, SubCategory, CashflowRecord


@admin.register(Status)
class StatusAdmin(ModelAdmin):
    list_display = ('title',)

@admin.register(Type)
class TypeAdmin(ModelAdmin):
    list_display = ('title',)

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('title', 'type')
    list_filter = ('type',)
    search_fields = ('title',)

@admin.register(SubCategory)
class SubCategoryAdmin(ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title',)

@admin.register(CashflowRecord)
class CashflowRecordAdmin(ModelAdmin):
    list_display = ('date', 'amount', 'type', 'category', 'sub_category', 'status')
    fields = ('date', 'amount', 'type', 'category', 'sub_category', 'status', 'comment')
    list_filter = ('status', 'type', 'category', 'sub_category', 'date')
    search_fields = ('comment', 'category__title', 'sub_category__title')
    date_hierarchy = 'date'
    raw_id_fields = ('category', 'sub_category')