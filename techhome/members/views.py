from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import UserForm, EditUserForm, EditProfileForm
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import ListView, DetailView
from home.models import Profile, Post, Comment, Author
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import CreateView

class CreateAuthorView(CreateView):
    model = Author
    template_name = 'registration/create-author.html'
    fields = ()
    success_url = reverse_lazy('newpost')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = self.request.user.username
        form.instance.picture = self.request.user.profile.picture
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(CreateAuthorView,self).get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user

        return context

class CreateProfileView(CreateView):
    model = Profile
    template_name = 'registration/create-profile.html'
    fields = ('bio','picture')
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateProfileView,self).get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user

        return context
class ProfileView(DetailView):
    model = Profile
    template_name = 'registration/profile.html'
    def get_context_data(self, **kwargs):
        context = super(ProfileView,self).get_context_data(**kwargs)
        profile = get_object_or_404(Profile,id=self.kwargs['pk'])
        posts = Post.objects.all()
        pk = self.kwargs["pk"]
        liked = False
        try:
            if profile.user.author.likes.filter(id=self.request.user.id).exists():
                liked = True
            total_likes = profile.user.author.total_likes()
            context['total_likes'] = total_likes
        except:
            pass
        context['liked'] = liked
        context['profile'] = profile
        context['posts'] = posts
        return context

def PasswordChanged(request):
    return render(request,'registration/success.html',{})

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password-done')
    template_name = 'registration/change-password.html'

class UserEdit(generic.UpdateView):
    form_class = EditUserForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

class EditProfileView(generic.UpdateView):

    form_class = EditProfileForm
    template_name = 'registration/profilepicture.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user.profile

def UserSignUpView(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserForm()

    return render(request, 'registration/signup.html', {'form': form})