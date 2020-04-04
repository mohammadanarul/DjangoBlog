from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


# Create your models here.
class author(models.Model):
    name            = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.FileField()
    datails         =  models.TextField()

    # Author Function
    def __str__(self):
        return self.name.username

class category(models.Model):
    name = models.CharField(max_length=100,)


    # Category Function
    def __str__(self):
        return self.name

class article(models.Model):
    article_author = models.ForeignKey(author, on_delete=models.CASCADE)
    title          = models.CharField(max_length=200)
    body           = RichTextUploadingField()
    image          = models.FileField()
    posted_on      = models.DateField(auto_now=False, auto_now_add=True)
    updated_on     = models.DateField(auto_now=True, auto_now_add=False)
    category       = models.ForeignKey(category, on_delete=models.CASCADE)

    
    # Article Function
    def __str__(self):
        return self.title 

class comment(models.Model):
    post         = models.ForeignKey(article, on_delete=models.CASCADE)
    name         = models.CharField(max_length=200)
    email        = models.EmailField(max_length=254)
    post_comment = models.TextField()

    def __str__(self):
        return self.post.title

    def __unicode__(self):
        return 





