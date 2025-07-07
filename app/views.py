from .models import Post, Category
from .forms import CommentForm
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic import View
""" markdownx追記 """
from .forms import BlogForm

class PostListView(ListView):
    model = Post
    # defaultでよいので削除 template_name = 'app/post_list.html'
    ordering = '-id'
    context_object_name = 'posts'   # HTMLに渡す
    paginate_by = 5   #追加

    #コンテキストを追加
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_data())
        return context
 
# 名前変更 PostDetailView --> PostDetail
class PostDetail(DetailView):
    model = Post
    # defaultでよいので削除 template_name = 'post_detail.html'  # 名前変更したが、デフォルトは「app/post_detail.html」になる

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #投稿されたコメントの全権を取得
        comments = self.object.comments.all()
        #コメントフォームを設置
        form = CommentForm()
        context.update({
            'comments': comments, 
            'form': form,
        })
        #コンテキストを追加
        context.update(get_common_data())
        return context
    # POSTで呼び出された場合はコメントを登録
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(data=self.request.POST or None)
        #フォームの入力値に問題がなければ、投稿に紐づけてから登録する
        if form.is_valid():
            # context_object_name = 'comments'   # 「no such table: app_comment」エラーが出る（未解決）
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
 
        return redirect('post_detail', pk=self.object.pk)

#PostListViewを継承してカテゴリー一覧を作成
class PostListByCategoryView(PostListView):
    # defaultでよいので削除 template_name = 'post_by_category.html'
 
    #カテゴリーで絞り込み
    def get_queryset(self):
        queryset = super().get_queryset()
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return queryset.filter(categories=category)
 
    #コンテキストにカテゴリー名を追加
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'categories': self.get_queryset().first().categories})
        return context

#PostListViewを継承して作成
class PostListByMonthView(PostListView):
    # defaultでよいので削除 template_name = 'post_by_month.html'
 
    def get_queryset(self):
        queryset = super().get_queryset()
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        #取得した年月で投稿を絞り込み
        if year and month:
            queryset = queryset.filter(created_at__year=year, created_at__month=month)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #取得した年月をそのままコンテキストに登録
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        context.update({
            'year': year,
            'month': month,
        })
        return context

def get_common_data():
    #サイドバーのカテゴリー一覧
    category_list = Category.objects.all()
    #サイドバーの月別投稿ー一覧
    post_month_list = Post.objects.dates('created_at', 'month', order='DESC')
    return {'category_list': category_list, 'post_month_list': post_month_list}

""" 自作フォーム """
# 次にdef定義したのを、class定義に変える。urls.pyも変更する
# def PostNew(request):

#     if request.method == "POST":
#         form = BlogForm(request.POST)

#         if form.is_valid():
#             form.save()
#             # return redirect('blog:index')
#             return redirect('post_list')

#     else:
#         form = BlogForm
#     context = {
#         'form': form
#     }
#     return render(request, 'app/form.html', context)

class CreatePostView(View):
    def get(self, request, *args, **kwargs):
        form = BlogForm(request.POST or None)

        return render(request, 'app/form.html', {
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = BlogForm(request.POST or None)

        if form.is_valid():
            form.save()
            return redirect('post_list')

        return render(request, 'app/form.html', {
            'form': form
        })

# class EditPostView(LoginRequiredMixin, View):
class EditPostView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = BlogForm(
            request.POST or None,
            initial={
                'title': post_data.title,
                'content': post_data.content,
            }
        )

        return render(request, 'app/form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = BlogForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])

        return render(request, 'app/form.html', {
            'form': form
        })

# class PostDeleteView(LoginRequiredMixin, View):
class PostDeleteView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html', {
            'post_data': post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('post_list')