from string import capwords

from django.conf import settings
from django.db import models
from django.db.models import Q, F
from django.core.validators import MinLengthValidator
from django.urls import reverse
from django.template.defaultfilters import slugify

from django_editorjs_fields import EditorJsJSONField


class Author(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Follow',
        related_name='followers',
        symmetrical=False,
        blank=True
    )
    bookmarks = models.ManyToManyField(
        'Article',
        related_name='bookmarks',
        symmetrical=False,
        blank=True
    )
    
    def __str__(self):
        return self.user.get_full_name()
    
    def get_absolute_url(self):
        return reverse('articles:author_detail', kwargs={'username': self.user})


class Follow(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'author'],
                name='unique_followers'
            ),
            models.CheckConstraint(
                check=~Q(follower=F('author')),
                name='prevent_self_follow',
                violation_error_message='The author cannot follow himself.'
            )
        ]
        ordering = ['-created_at']


class Category(models.Model):
    name = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = capwords(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name', 'pk']


class Article(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(
        Category,
        help_text='Select up to 3 categories to help Masonex readers explore articles that interest them.',
    )
    title = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(3)],
        db_index=True
    )
    slug = models.SlugField(max_length=128, null=True, db_index=True)
    thumbnail = models.ImageField(
        upload_to=settings.PHOTOS_PATH,
        verbose_name='Article listing cover image',
        help_text='''
            This image will be displayed on article listing.
            The recommended size 1920x1440 and recommended ratio is 4:3.
        ''',
    )
    body = EditorJsJSONField(**settings.EDITORJS_CONFIG_OVERRIDE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    class Meta:
        ordering = ['-created_at', 'title', 'pk']
