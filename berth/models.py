from django.db import models
from colorfield.fields import ColorField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError

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
	color = ColorField(default='#CCFFFF')
	move_performa =  models.IntegerField(verbose_name ='Move Performa',default=0)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

class Vessel(models.Model):
	V = 'VESSEL'
	B ='BARGE'
	N = 'NOTICE'
	VESSEL_TYPE_CHOICES = (
        (V, 'Vessel'),
        (B, 'Barge'),
        (N, 'Notice'),
    )
	name = models.CharField(max_length=50,primary_key=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	lov = models.IntegerField(verbose_name ='Lenght of Vessel',default=100)
	imo = models.CharField(verbose_name ='IMO number',max_length=20,blank=True, null=True)
	v_type = models.CharField(verbose_name ='Vessel Type',max_length=10,choices=VESSEL_TYPE_CHOICES,default=V)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	
	def __str__(self):
		return self.name

class Voy(models.Model):
	R = 'R'
	L ='L'
	T = 'T'
	B = 'B'
	TEXT_POS_CHOICES = (
        (R, 'Right'),
        (L, 'Left'),
        (T, 'Top'),
        (B, 'Buttom'),
    )
	voy = models.CharField(max_length=50 )#,primary_key=True
	slug = models.SlugField(unique=True,blank=True, null=True)
	code = models.CharField(max_length=20,blank=True, null=True)
	vessel = models.ForeignKey('Vessel', related_name='plans')
	service = models.ForeignKey('Service', related_name='plans')
	terminal = models.ForeignKey('Terminal', related_name='plans')
	start_pos = models.IntegerField(verbose_name ='Start Position',default=50)
	performa_in =  models.DateTimeField(blank=True, null=True)
	performa_out =  models.DateTimeField(blank=True, null=True)
	move_performa =  models.IntegerField(verbose_name ='Move Performa',default=0)
	move_confirm = models.BooleanField(verbose_name ='Move Confirm',default=False)
	eta =  models.DateTimeField(verbose_name ='ETA',blank=True, null=True)
	etb =  models.DateTimeField(verbose_name ='ETB',blank=True, null=True)
	etd =  models.DateTimeField(verbose_name ='ETD',blank=True, null=True)
	qc = models.CharField(verbose_name ='Q',max_length=20,blank=True, null=True)
	dis_no =  models.IntegerField(verbose_name ='Discharge',default=0)
	load_no =  models.IntegerField(verbose_name ='Loading',default=0)
	est_teu = models.IntegerField(verbose_name ='Est TEU',default=0)
	vsl_oper = models.CharField(verbose_name ='Vsl Operator',max_length=20,blank=True, null=True)
	arrival_draft = models.CharField(verbose_name ='Arrival draft',max_length=50,blank=True, null=True,default=0)
	departure_draft = models.CharField(verbose_name ='Departure draft',max_length=50,blank=True, null=True,default=0)
	remark = models.TextField(max_length=255,blank=True, null=True)
	draft = models.BooleanField(verbose_name ='Saved as Draft',default=False)
	text_pos = models.CharField(verbose_name ="Text position for Barge",max_length=1,choices=TEXT_POS_CHOICES,default=R)
	next_date = models.IntegerField(verbose_name ='Next arrive date',default=14)

	def clean(self):
		if self.etd <= self.etb :
			raise ValidationError('ETD must bigger than ETB')

	def save(self, *args, **kwargs):
		teu_factor = 1.43
		if self.dis_no != 0 :
			teu_dis = self.dis_no * teu_factor
		else:
			teu_dis = 0

		if self.load_no != 0 :
			teu_load = self.load_no * teu_factor
		else :
			teu_load = 0

		self.est_teu = teu_dis + teu_load
		super(Voy, self).save(*args, **kwargs) # Call the "real" save() method.
	# class Meta:
	# 	unique_together = ('voy', 'vessel',)




# Handle Slug of Vessel

def create_vessel_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Vessel.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().lov)
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
    qs = Service.objects.filter(slug=slug).order_by("-id")
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
    slug = slugify(instance.voy + '-v')
    print ('New slug %s' % slug)
    if new_slug is not None:
        slug = new_slug
    qs = Voy.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_voy_slug(instance, new_slug=new_slug)
    return slug


def pre_save_voy_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_voy_slug(instance)

pre_save.connect(pre_save_voy_receiver, sender=Voy)