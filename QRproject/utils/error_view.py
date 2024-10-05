<<<<<<< HEAD
from django.http import JsonResponse

def handler404(request,exception):
    message = ('Path not found')
    response = JsonResponse(data={'error':message})
    response.status_code = 404
    return response

def handler500(request):
    message = ('Internal server error')
    response = JsonResponse(data={'error':message})
    response.status_code = 500
    return response
=======
from django.http import JsonResponse

def handler404(request,exception):
    message = ('Path not found')
    response = JsonResponse(data={'error':message})
    response.status_code = 404
    return response

def handler500(request):
    message = ('Internal server error')
    response = JsonResponse(data={'error':message})
    response.status_code = 500
    return response
>>>>>>> 49cc1c162d40e4b298df25389748a49b7cebbf23
