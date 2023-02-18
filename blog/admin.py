from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin
from .models import Category, Post, Comment
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.enable_nav_sidebar = False


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'id',
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)

@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    list_display = ["__str__",'views','category','status','posted',"id", ]
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['posted','author','category',]
    search_fields = ["__str__"]
    list_per_page = 10
    pass

admin.site.register(Comment, MPTTModelAdmin)