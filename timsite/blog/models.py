from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Post model"""
    title = models.CharField(max_length=128)
    body = models.TextField(blank=True)
    slug = models.SlugField(max_length=128, unique=True)
    create_date = models.DateTimeField('Date the post was originally created', auto_now_add=True)
    pub_date = models.DateTimeField('Publish date', blank=True, null=True)
    edit_date = models.DateTimeField('Date post was edited, most recently', auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    snippet = models.TextField('Short section from the body of the text', blank=True)
    published = models.BooleanField('Whether the post is published, or still in edit', default=False)

    def __str__(self):
        return self.title

    def pt_to_html(self):
        # Converts plain-text input in the body to html <p> tags

        self.body = self.body.replace('\r\n\r\n', '</p><p>')
        if self.body[0:3] != '<p>':
            self.body = '<p>' + self.body

        if self.body[-4:] != '</p>':
            self.body += '</p>'

    def save(self, *args, **kwargs):

        # Set the pub date to the current date when published
        if (self.pub_date is None) and self.published:
            self.pub_date = timezone.now()

        self.pt_to_html()

        self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)
