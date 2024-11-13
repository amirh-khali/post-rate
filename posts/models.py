from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Rating(models.Model):
    user_id = models.CharField(max_length=255)
    post = models.ForeignKey(Post, related_name='ratings', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()  # Rating between 0 and 5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'user_id')

    def __str__(self):
        return f'{self.user_id} rated {self.post.title} with {self.score}'
