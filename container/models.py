from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse

from bayplan.models import BayPlanFile

# Create your models here.
class Container(models.Model):
	bayplanfile = models.ForeignKey(BayPlanFile)
	slug = models.SlugField(unique=True,blank=True, null=True)
	item_no = models.IntegerField()
	container = models.CharField(max_length=11)
	iso_code  = models.CharField(max_length=4,blank=True, null=True)
	full	  = models.BooleanField(default=False)
	partner	  = models.CharField(max_length=10,blank=True, null=True)
	weight	  = models.IntegerField()
	load_port = models.CharField(max_length=10,blank=True, null=True)
	dis_port  = models.CharField(max_length=10,blank=True, null=True)
	deliverly_port = models.CharField(max_length=10,blank=True, null=True)
	good_desc = models.CharField(max_length=100,blank=True, null=True)
	stowage =	models.CharField(max_length=10)
	original_stowage = models.CharField(max_length=10,blank=True, null=True)
	bay       =	models.CharField(max_length=10,blank=True, null=True)
	original_bay       =	models.CharField(max_length=10,blank=True, null=True)
	ready_to_load		= models.BooleanField(default=False)# Ready to UpLoad
	uploaded = models.BooleanField(default=False)
	upload_date = models.DateTimeField(blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return ('%s' % (self.container))

	def get_absolute_url(self):
		return reverse('container:stowage', kwargs={'slug': self.slug})


def create_container_slug(instance, new_slug=None):
    slug = slugify("%s-%s" %(instance.container, instance.item_no))
    if new_slug is not None:
        slug = new_slug
    qs = Container.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.count())
        return create_container_slug(instance, new_slug=new_slug)
    return slug


def pre_save_container_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_container_slug(instance)

pre_save.connect(pre_save_container_receiver, sender=Container)