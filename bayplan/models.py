from django.db import models
from berth.models import Voy
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse

from django.db.models import Count,Sum,Min,Max

# Create your models here.
class BayPlanFile(models.Model):
	voy = models.OneToOneField(
				Voy,
				on_delete=models.CASCADE,
				primary_key=True,
				)
	# filename = models.FileField(upload_to='bayplan/%Y/%m/%d/',blank=True, null=True)
	filename = models.FileField(upload_to='bayplan/%Y/%m/%d/')
	slug = models.SlugField(unique=True,blank=True, null=True)
	remark = models.TextField(blank=True, null=True)
	ready_to_load = models.BooleanField(default=False)
	uploaded = models.BooleanField(default=False)
	upload_date = models.DateTimeField(blank=True, null=True)
	updated_filename = models.FileField(upload_to='bayplan/%Y/%m/%d/',blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return ('%s' % (self.voy))

	def get_absolute_url(self):
		return reverse('bayplan:voy-detail', kwargs={'slug': self.voy.slug})

	def get_not_ready_bay(self):
		summary = self.container_set.filter(ready_to_load=False).values('bay').annotate(
			total=Count('container')
			)
		return summary


def create_bayplan_slug(instance, new_slug=None):
    slug = slugify(instance.filename)
    if new_slug is not None:
        slug = new_slug
    qs = BayPlanFile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.count())
        return create_bayplan_slug(instance, new_slug=new_slug)
    return slug


def pre_save_bayplan_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_bayplan_slug(instance)

pre_save.connect(pre_save_bayplan_receiver, sender=BayPlanFile)




