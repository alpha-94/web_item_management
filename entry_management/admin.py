from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Entry_Info


# Register your models here.

class Entry_info_Admin(ImportExportMixin, admin.ModelAdmin):
    pass


class Item_class_Admin(ImportExportMixin, admin.ModelAdmin):
    pass


class Item_condition_Admin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(Entry_Info, Entry_info_Admin)

