from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)

from rest_framework import serializers

from container.models import Container

container_detail_url=HyperlinkedIdentityField(
		view_name='container-api:detail',
		lookup_field='slug'
		)


class ContainerListSerializer(ModelSerializer):
	# url = serializers.CharField(source='get_absolute_url', read_only=True)
	# url = container_detail_url
	class Meta:
		model = Container
		# fields ='__all__'
		# exclude = ('voy','created_date','modified_date','user',)
		fields =['container','stowage','original_stowage']

class ContainerDetailSerializer(ModelSerializer):
	class Meta:
		model = Container
		fields ='__all__'
