from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import *


# Register your models here.

class Item_info_Admin(ImportExportMixin, admin.ModelAdmin):
    pass


class Item_class_Admin(ImportExportMixin, admin.ModelAdmin):
    pass


class Item_condition_Admin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(Item_info, Item_info_Admin)
admin.site.register(Item_Class, Item_class_Admin)
admin.site.register(Item_Condition, Item_condition_Admin)

