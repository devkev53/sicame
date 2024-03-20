from django.contrib import admin
from django.utils.html import format_html
from .models import Entry, MaterialEntryDetail
# Register your models here.


class MaterialEntryDetailInline(admin.TabularInline):
  '''Tabular Inline View for MaterialEntryDetail'''

  model = MaterialEntryDetail
  min_num = 0
  # max_num = 20
  extra = 0
  raw_id_fields = ('id_material',)
  autocomplete_fields = ['id_material',]
  readonly_fields = ["total",]
  fieldsets = (
  (None, {
      'fields': (('id_material', 'quantity', 'amount', 'location','total'), (
          ))
  }),)

  def total(self, obj):
      return format_html("<input type='number' class='vTextField' value=0.00 readonly />")

@admin.register(MaterialEntryDetail)
class MaterialEntryDetailAdmin(admin.ModelAdmin):
  '''Admin View for MaterialEntryDetail'''

  list_display = ('id_material',)
#   list_filter = ('',)
#   inlines = [
#     Inline,
#   ]
#   raw_id_fields = ('',)
#   readonly_fields = ('',)
  search_fields = ('id_material',)
#   date_hierarchy = ''
#   ordering = ('',)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
  '''Admin View for Entry'''

  list_display = ('created_by', 'created', 'reference',)
  # list_filter = ('',)
  inlines = [
    MaterialEntryDetailInline,
  ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  # search_fields = ('',)
  # date_hierarchy = ''
  # ordering = ('',)