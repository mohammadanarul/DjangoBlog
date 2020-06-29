from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


# Create your models here.
class author(models.Model):
    name            = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_picture', default='profile_picture/pic.png')
    profile_background_picture = models.ImageField(upload_to='profile_background_picture', default='profile_background_picture/banner.jpg')
    datails         =  models.TextField()

    # Author Function
    def __str__(self):
        return self.name.username

class category(models.Model):
    name = models.CharField(max_length=100,)

    # Category Function
    def __str__(self):
        return self.name

class Tag(models.Model):
    tagslug = models.SlugField()

class article(models.Model):
    article_author   = models.ForeignKey(author, on_delete=models.CASCADE)
    title            = models.CharField(max_length=200)
    body             = RichTextUploadingField()
    likes            = models.ManyToManyField(User, related_name='likes', blank=True)
    # comment          = models.ForeignKey(Comment, on_delete=models.CASCADE)
    image            = models.ImageField(upload_to='blog_picture')
    posted_on        = models.DateField(auto_now=False, auto_now_add=True)
    updated_on       = models.DateField(auto_now=True, auto_now_add=False)
    blog_post_views  = models.IntegerField(default=0)
    category         = models.ForeignKey(category, on_delete=models.CASCADE)
    published        = models.BooleanField(default=True)

    
    # Article Function
    def __str__(self):
        return self.title 

class Comment(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    post         = models.ForeignKey(article, on_delete=models.CASCADE)
    email        = models.EmailField(max_length=254)
    reply        = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies')
    post_comment = models.TextField()
    timestamp    = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{} - {}'.format(self.post.title, str(self.user.username))




