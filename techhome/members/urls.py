from django.contrib import admin
from django.urls import path
from .views import CreateAuthorView,UserSignUpView, UserEdit, PasswordsChangeView, PasswordChanged, ProfileView,EditProfileView,CreateProfileView
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('signup', UserSignUpView, name="signup"),
    path('edit', UserEdit.as_view(), name="edit"),
    path('password', PasswordsChangeView.as_view(), name="password"),
    path('password-success', PasswordChanged, name="password-done"),
    path('<int:pk>/profile', ProfileView.as_view(), name="profile"),
    path('<int:pk>/edit/profile', EditProfileView.as_view(), name="edit-profile"),
    path('create/profile', CreateProfileView.as_view(), name="create-profile"),
    path('become/author', CreateAuthorView.as_view(), name="author"),

    path('reset_password/', auth_view.PasswordResetView.as_view(template_name="registration/password_reset.html"), name="reset_password"),
    path('reset_password/done', auth_view.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), name="password_reset_done"),
    path('reset_password/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password/completed', auth_view.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_complete"),



]