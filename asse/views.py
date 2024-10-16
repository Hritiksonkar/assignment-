from django.views.generic import ListView, DetailView
from .models import Blog, Comment
from django.contrib.postgres.search import TrigramSimilarity, SearchVector
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.db.models import Q

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('blog-list')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})


class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Blog.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return Blog.objects.all()
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = self.object
            comment.author = request.user
            comment.save()
            return redirect('blog-detail', slug=self.object.slug)
        return self.get(request, *args, **kwargs)

def share_blog_email(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        recipient_email = request.POST.get('email')
        send_mail(
            f"Check out this blog: {blog.title}",
            blog.content,
            'from@example.com',
            [recipient_email]
        )
        messages.success(request, 'Email sent successfully!')
        return redirect('blog-detail', slug=blog.slug)
    return render(request, 'share_email.html', {'blog': blog})

def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.like_count += 1
    comment.save()
    return JsonResponse({'success': True, 'like_count': comment.like_count})
