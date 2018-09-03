from django.shortcuts import render

def home(request):
    """
    Página inicial

    :type request: request
    :param request: requisição recebida
    """

    return render(request, 'index.html')