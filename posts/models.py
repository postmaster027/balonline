from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=80)
#    image = models.ImageField(blank=True, null=True, upload_to='media/posts')
    pub_date = models.DateTimeField('date published')
    annotation  = models.TextField(max_length=320)
    content  = models.TextField(max_length=4000)

    def __unicode__(self):
        return self.title

# Create your models here.
