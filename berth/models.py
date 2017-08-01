from django.db import models
from colorfield.fields import ColorField
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.
ACTIVE='A'
DEACTIVE='D'
STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (DEACTIVE, 'Deactive'),
    )


class Terminal(models.Model):
	name = models.CharField(max_length=50,primary_key=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	start_range = models.CharField(verbose_name ='Excel start range',max_length=2,blank=True, null=True)
	stop_range = models.CharField(verbose_name ='Excel stop range',max_length=2,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name


class Service(models.Model):
	name = models.CharField(max_length=50,primary_key=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

class Vessel(models.Model):
	V = 'VESSEL'
	B ='BARTH'
	VESSEL_TYPE_CHOICES = (
        (V, 'Vessel'),
        (B, 'Barth'),
    )
	name = models.CharField(max_length=50,primary_key=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	lov = models.IntegerField(verbose_name ='Lenght of Vessel',default=100)
	imo = models.CharField(verbose_name ='IMO number',max_length=20,blank=True, null=True)
	color = ColorField(default='#CCFFFF')
	v_type = models.CharField(verbose_name ='Vessel Type',max_length=10,choices=VESSEL_TYPE_CHOICES,default=V)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	
	def __str__(self):
		return self.name

class Voy(models.Model):
	voy = models.CharField(max_length=50,primary_key=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	code = models.CharField(max_length=20,blank=True, null=True)
	vessel = models.ForeignKey('Vessel', related_name='plans')
	service = models.ForeignKey('Service', related_name='plans')
	terminal = models.ForeignKey('Terminal', related_name='plans')
	start_pos = models.IntegerField(verbose_name ='Start Position',default=50)
	performa_in =  models.DateTimeField(blank=True, null=True)
	performa_out =  models.DateTimeField(blank=True, null=True)
	eta =  models.DateTimeField(verbose_name ='Arrival Time',blank=True, null=True)
	etb =  models.DateTimeField(verbose_name ='Berth Time',blank=True, null=True)
	etd =  models.DateTimeField(verbose_name ='Departure Time',blank=True, null=True)
	dis_no =  models.IntegerField(verbose_name ='Number of Discharge',default=0)
	load_no =  models.IntegerField(verbose_name ='Number of Loading',default=0)
	est_teu = models.IntegerField(verbose_name ='Estimate TEU',default=0)
	vsl_oper = models.CharField(verbose_name ='Vsl Operator',max_length=20,blank=True, null=True)
	arrival_draft = models.CharField(verbose_name ='Arrival draft',max_length=50,blank=True, null=True,default=0)
	departure_draft = models.CharField(verbose_name ='Departure draft',max_length=50,blank=True, null=True,default=0)
	remark = models.TextField(max_length=255,blank=True, null=True)
	draft = models.BooleanField(verbose_name ='Saved as Draft',default=False)


# Handle Slug of Vessel

def create_vessel_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Vessel.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().imo)
        return create_vessel_slug(instance, new_slug=new_slug)
    return slug


def pre_save_vessel_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_vessel_slug(instance)

pre_save.connect(pre_save_vessel_receiver, sender=Vessel)


# Handle Slug of Terminal

def create_terminal_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Terminal.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_terminal_slug(instance, new_slug=new_slug)
    return slug


def pre_save_terminal_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_terminal_slug(instance)

pre_save.connect(pre_save_terminal_receiver, sender=Terminal)


# Handle Slug of Service

def create_service_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Terminal.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_service_slug(instance, new_slug=new_slug)
    return slug


def pre_save_service_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_service_slug(instance)

pre_save.connect(pre_save_service_receiver, sender=Service)



# Handle Slug of Voy

def create_voy_slug(instance, new_slug=None):
    slug = slugify(instance.voy)
    if new_slug is not None:
        slug = new_slug
    qs = Terminal.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_service_slug(instance, new_slug=new_slug)
    return slug


def pre_save_voy_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_voy_slug(instance)

pre_save.connect(pre_save_voy_receiver, sender=Voy)