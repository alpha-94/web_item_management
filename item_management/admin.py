from django.contrib import admin
from import_export.admin import ExportActionMixin, ImportExportMixin, ImportMixin
from .models import Item_info


# Register your models here.

class Item_info_Admin(ImportExportMixin, admin.ModelAdmin):
    pass


class Item_class_Admin(ImportExportMixin, admin.ModelAdmin):
    pass


class Item_condition_Admin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(Item_info, Item_info_Admin)

