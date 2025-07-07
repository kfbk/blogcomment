from django.contrib import admin
from .models import Post, Comment,Category
from django.urls import reverse
from django.utils.html import format_html
from markdownx.admin import MarkdownxModelAdmin

#投稿詳細管理画面にコメントも追加
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('author', 'text', 'approved_comment')
 
class PostAdmin(admin.ModelAdmin):
     list_display = ('title', 'created_at', 'updated_at','thumbnail', 'get_comment_count')
     inlines = (CommentInline,)
    
     #コメント数を測定して、記事一覧画面に反映
     def get_comment_count(self, obj):
          return obj.comments.count()
 
     get_comment_count.short_description = 'Comment Count'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'get_post_link', 'author', 'created_at', 'approved_comment')
    list_filter = ('approved_comment', 'created_at',)
    search_fields = ('text', 'post__title', 'author')
    readonly_fields = ('created_at',)

    def get_post_link(self, obj):
        url = reverse('admin:djangoblog_post_change', args=[obj.post.id])
        return format_html("<a href='{}'>{}</a>", url, obj.post.title)

    get_post_link.short_description = 'Post'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')

#Postモデルに対応する管理機能を定義
# admin.site.register(Post, PostAdmin)
admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)