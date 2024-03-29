from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.category_name


# Posts Model
class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="assets/blog_images/")
    datecreated = models.DateTimeField(auto_now_add=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-datecreated"]

    def __str__(self):  # This string is defined to change the name as title
        return self.title


# voter model
class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.voter


# image uploads
