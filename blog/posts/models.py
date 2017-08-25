from django.db import models
import random
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from datetime import date
# Create your models here.

def upload_location(instance, filename):
    return "%s/%s" %(instance, filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug":self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]


# def create_slug(instance, new_slug=None):
#     slug = slugify(instance.title)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Post.objects.filter(slug=slug).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" %(slug, qs.first.id)
#         return create_slug(instance, new_slug=new_slug)
#
#
# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#    if not instance.slug:
#        instance.slug = create_slug(instance)
#
# pre_save.connect(pre_save_post_receiver, sender=Post)


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    # today = date.today()
    # print(today)
    instance.slug = '%s-%s' % (slug, random.randint(1, 200))
    return instance.slug


pre_save.connect(pre_save_post_receiver, sender=Post)