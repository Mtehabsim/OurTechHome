from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255)
    info = models.TextField(max_length=500)
    picture = models.ImageField(null=True, blank=True, upload_to="images/category")
    def __str__(self): # for admin display
        return self.name

class Author(models.Model):

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    picture = models.ImageField(null= True, blank= True,upload_to="images/")
    verified = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, null=True, blank=True, related_name='author_user_likes')

    def total_likes(self):
        return self.likes.count()
    def __str__(self): # for admin display
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    writer = models.ForeignKey(Author,on_delete=models.CASCADE)
    content = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default='SOME STRING')
    date = models.DateField(default=datetime.date.today())
    picture = models.ImageField(upload_to="images/",default='images/default.jpg')
    likes = models.ManyToManyField(User, null= True, blank= True,related_name='post_user_likes')
    dislikes = models.ManyToManyField(User, null= True, blank= True,related_name='post_user_dislikes')
    Resources = models.TextField(max_length=1000, null=True, blank=True)
    top = models.BooleanField(default= False)
    verified =models.BooleanField(default=False)
    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self): # for admin display
        return self.title + " | " + self.writer.name + " | " + str(self.category)


class Comment(models.Model):
    date = models.DateField(default=datetime.date.today())
    content = models.TextField(max_length=500)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    def __str__(self): # for admin display
        return self.post.title + " | " + str(self.creator)


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True, upload_to="images/",  default='images/default.jpg')
    bio = models.TextField()

    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'pk': self.pk})

    def __str__(self): # for admin display
        return str(self.user)

# Create your models here.
