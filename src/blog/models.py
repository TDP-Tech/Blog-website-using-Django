from django.db import models
# Create your models here.
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import pre_save,post_delete
from django.dispatch import receiver


def upload_location(instance, filename, **kwargs): # for uploading images it takes the intance and file name as an input
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id = str(instance.author.id),    # author of the post
        title = str(instance.title),    #title of the blog
        filename = filename
    )
    return file_path


class BlogPost(models.Model):
    title = models.CharField(max_length=70, null=False, blank=False)
    body = models.TextField(max_length=100000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True) #slug is just a URL and it is UNIQUE

    def __str__(self):
        return self.title


@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):   #this is called before the blog post is actually commited to the database
    if not instance.slug: #if no slug created yet
        instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)    #wire up the receiver