from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Category, Author, Comment, Profile
from django.urls import reverse_lazy, reverse
from .forms import CommentForm
from django.http import HttpResponseRedirect

class ReviewCatPostView(DetailView):
    model = Category
    template_name = 'post-review.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        check = False
        context['check'] = check

        return context

class ReviewPostView(ListView):
    model = Category
    template_name = 'review.html'

class AddPostView(CreateView):
    model = Post
    template_name = 'new-post.html'
    fields = ('title', 'content', 'category', 'picture','Resources')
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.writer = self.request.user.author
        form.instance.top = False

        if form.instance.writer.verified:
            form.instance.verified = True

        return super().form_valid(form)


def ApproveView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    user = get_object_or_404(Author, pk = post.writer.pk)
    if not post.verified:
        user.verified = True
        post.verified = True
        user.save()
        post.save()

    return HttpResponseRedirect(reverse('article', args=[str(pk)]))

def DisLikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
    return HttpResponseRedirect(reverse('article', args=[str(pk)]))

def LikeAuthorView(request,pk):
    profile = get_object_or_404(Profile, id=request.POST.get('profile_id'))
    author = profile.user.author
    if author.likes.filter(id=request.user.id).exists():
        author.likes.remove(request.user)
    else:
        author.likes.add(request.user)

    return HttpResponseRedirect(reverse('profile', args=[str(pk)]))

def LikeView(request,pk):

    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('article', args=[str(pk)]))

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-date']
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(verified=True)
        return queryset

class ArticleView(DetailView):
    model = Post
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]

        form = CommentForm()
        post = get_object_or_404(Post, pk=pk)
        comments = post.comment_set.all()
        liked = False
        disliked = False
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
            disliked = False
        if stuff.dislikes.filter(id=self.request.user.id).exists():
            disliked = True
            liked = False

        total_likes = stuff.total_likes()
        total_dislikes = stuff.total_dislikes()
        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        context['total_likes'] = total_likes
        context['total_dislikes'] = total_dislikes
        context['liked'] = liked
        context['disliked'] = disliked
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                creator=request.user, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)

class CategoryView(ListView):
    model = Category
    template_name = 'category.html'

class catPage(DetailView):
    model = Category
    template_name = 'ca-page.html'


class docsView(ListView):
    model = Author
    template_name = 'docs.html'

#def about(request):
#    return render(request, 'about.html',{})

def search_posts(request):
    searched = request.POST['searched']
    posts = Post.objects.filter(title__contains = searched, verified=True)

    if request.method == 'POST':
        return render(request,
                  'search.html',
                  {'searched':searched,
                   'posts':posts})

