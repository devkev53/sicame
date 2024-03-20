from django.contrib import admin
from .models import Brand, Category, Material, Equipment

# Register your models here.

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
  '''Admin View for Brand'''

  list_display = ('name', 'preview_img',)
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  # search_fields = ('',)
  # date_hierarchy = ''
  # ordering = ('',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  '''Admin View for Category'''

  list_display = ('name',)
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  # search_fields = ('',)
  # date_hierarchy = ''
  # ordering = ('',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
  '''Admin View for Material'''

  list_display = (
    'name', 'preview_image', 'id_brand', 'stock',
    # 'state', 'assigned', 'turned', 'consumed',
    # 'in_warehouse'
  )
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  search_fields = ('name', 'id_brand')
  # date_hierarchy = ''
  # ordering = ('',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
  '''Admin View for Equipment'''

  list_display = (
    'name', 'preview_image', 'id_brand', 'stock',
    # 'state', 'assigned', 'turned', 'consumed',
    # 'in_warehouse'
  )
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  # search_fields = ('',)
  # date_hierarchy = ''
  # ordering = ('',)