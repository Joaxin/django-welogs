from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import MiniBlog,Topic
from .models import UploadForm, UploadModel


@admin.register(MiniBlog)
class MiniBlogAdmin(MarkdownxModelAdmin):
    list_display = ['user', 'status','content','tag_list','num_click', 'num_likes', 'num_comment', 't_publish']
    search_fields = ['user', 'content',  'num_comment']
    list_filter = ['user','status', 'content', 'num_click', 'num_likes', 'num_comment', 't_publish']
    ordering = ('status', 't_publish',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['topic_name','t_publish','t_publish']
    search_fields = ['topic_name']
    list_filter = ['topic_name','t_publish']

@admin.register(UploadModel)
class UploadModelAdmin(admin.ModelAdmin):
    list_display = ["images_list"]
    form = UploadForm

# @admin.register(Quote)
# class QuoteAdmin(MarkdownxModelAdmin):
#     list_display = ['author','title', 'slug','category','person', 't_create','t_publish','status']
#     list_filter = ('status', 't_create', 't_publish', 'author',)
#     search_fields = ('title', 'content','content_trans')
#     prepopulated_fields = {'slug': ('title',)}
#     raw_id_fields = ('author',)
#     date_hierarchy = 't_publish'
#     ordering = ('status', 't_publish',)

# @admin.register(Person)
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ['full_name','picture']

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['title']


# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['name', 'quote', 'email','body', 'created','updated','active']
#     list_filter = ('active', 'created', 'updated')
#     search_fields = ('name', 'email', 'body')