from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    featured_image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title

class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10)  # image / video
    file = models.FileField(upload_to='media/')

    def __str__(self):
        return f"{self.media_type} for {self.post.title}"

class SEOMeta(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    keywords = models.TextField()

    def __str__(self):
        return f"SEO for {self.post.title}"
