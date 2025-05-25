from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class News(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    image = models.ImageField(upload_to="news_images/")
    content = models.TextField()
    published_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft",
    )
    vertical = models.ForeignKey(
        "accounts.Vertical", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_pro = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.status == "published" and self.published_date is None:
            self.published_date = timezone.now()
        elif self.status == "draft":
            self.published_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
