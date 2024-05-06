from django.http import JsonResponse
from django.shortcuts import render, redirect
from app.models import Contact

# Create your views here.

# index
def index(request):
    return render(request, 'index.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        contact = Contact(name=name, email=email, message=message)
        contact.save()
       
        return JsonResponse({'message': 'Your message has been sent successfully!'})
    
    return render(request, 'contact.html')
