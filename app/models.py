from django.db import models
from django.urls import reverse
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
""" markdownx追記 """
from markdownx.models import MarkdownxField
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

#実行順１
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.name

    # urls.pyの記述からの逆引きでURLを表示する関数
    # (カテゴリーでの記事一覧を作成するためのURL生成する)
    def get_absolute_url(self):
        if self.slug:
            return reverse('post_list_by_category', args=[self.slug])
        else:
            return reverse('post_list_by_category', args=['undefined'])

#実行順2
#マイグレーション時にだけ起動する関数を定義
@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    #djangoblogアプリマイグレーション時にだけ起動する
    # if sender.name == apps.get_app_config('djangoblog').name:
    if sender.name == apps.get_app_config('app').name:
        #未分類カテゴリーがなければ作成、あれば取得する
        category, created = Category.objects.get_or_create(
            name='未分類',
            slug='undefined',
            defaults={
                'description': 'Default category created by migration',
            }
        )
        # キャッシュをクリア
        ContentType.objects.clear_cache()
        
class Post(models.Model):
    title = models.CharField(max_length=255)
    # content = models.TextField()
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='images/', null=True, blank=True) #追加
    categories = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, related_name='posts', default=1)
    
    # """ カスタムメソッド """
    def get_text_markdownx(self):
        # print ("this is debug print")
        return mark_safe(markdownify(self.content))
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50, blank=True, default='匿名')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)
 
    def __str__(self):
        return self.text