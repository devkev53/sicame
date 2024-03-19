from django.contrib import admin
from .models import Material, Equipment, Brand, Category

# Register your models here.
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
  '''Admin View for Material'''

  # list_display = ('',)
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  # search_fields = ('',)
  # date_hierarchy = ''
  # ordering = ('',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
  '''Admin View for Equipment'''

  # list_display = ('',)
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  # search_fields = ('',)
  # date_hierarchy = ''
  # ordering = ('',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
  '''Admin View for Brand'''

  list_display = ('name', 'showImg')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  '''Admin View for Category'''