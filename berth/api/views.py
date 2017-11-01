from django.db.models import Q

from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	UpdateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView
	)

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

from .serialize import VoySerializer,VoyDetailSerializer
from berth.models import Voy



class VoyListAPIView(ListAPIView):
	queryset=Voy.objects.all()
	serializer_class=VoySerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields =['voy']
	def get_queryset(self,*args,**kwargs):
		# queryset_list=Comment.objects.filter(user=self.request.user)
		queryset_list = Voy.objects.all()
		from_date = self.request.GET.get("f")
		to_date = self.request.GET.get("t")
		print ('From : %s  -- To : %s ' % (from_date,to_date))
		queryset_list = Voy.objects.filter(
				Q(etb__range=[from_date,to_date])|
				Q(etd__range=[from_date,to_date])).order_by('etb')
		return queryset_list
	# filter_backends=[SearchFilter,OrderingFilter],
	# search_fields =['content','user__first_name']
	# pagination_class = PostPageNumberPagination

class VoyDetailAPIView(RetrieveAPIView):
	queryset=Voy.objects.all()
	serializer_class=VoyDetailSerializer
	lookup_field='slug'
	# print ("vessel details")