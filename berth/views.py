from django.shortcuts import render

# Create your views here.
from pdfdocument.utils import pdf_response #Pip reportlab
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse
import os.path
from django.conf import settings
# def xls_to_response(xls, fname):
#     response = HttpResponse(mimetype="application/ms-excel")
#     response['Content-Disposition'] = 'attachment; filename=%s' % fname
#     xls.save(response)
#     return response


# def index(request):
#     response = HttpResponse(mimetype="application/ms-excel")
#     response['Content-Disposition'] = 'attachment; filename=test.xlsm'
#     xls.save(response)
#     return response



def pdf_view(request):
	vFileName ='test.pdf'
	full_path = os.path.join(settings.STATIC_ROOT, vFileName) #static(vFileName)
	with open(full_path, 'rb') as pdf:
		response = HttpResponse(pdf.read(),content_type='application/pdf')
		response['Content-Disposition'] = 'filename=some_file.pdf'
	return response
	# pdf, response = pdf_response('filename_without_extension')
	# # ... more code
	# pdf.generate()
	# return HttpResponse(full_path)