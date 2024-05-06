from django.http import JsonResponse
from django.shortcuts import render, redirect
from app.models import Register

# index
def index(request):
    # get session and sent it wot index
    username = request.session.get('username')
    profile_picture = f'/static/profile_pictures/{username}.png'
    user_username_and_profile = {
        'username': username,
        'profile_picture': profile_picture
    }
    return render(request, 'index.html', {'username': user_username_and_profile})

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['confirm_password']

        
        # if email is valid and password is valid
        if Register.objects.filter(email=email).exists():
           return JsonResponse({'error': 'Email is already taken!'})
        elif Register.objects.filter(username=username).exists():
             return JsonResponse({'error': 'Username is already taken!'})
        elif password != password2:
            return JsonResponse({'error': 'Password does not match!'})
        
        register = Register(email=email, username=username, password=password, password2=password2)
        register.save()
        return JsonResponse({'message': 'You have successfully registered!'})
    
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        if Register.objects.filter(email=email).exists():
            if Register.objects.filter(password=password).exists():
                username = Register.objects.get(email=email).username
                request.session['username'] = username
                
                return redirect('home')
                
            else:
                return JsonResponse({'error': 'Password is incorrect!'})
        else:
            return JsonResponse({'error': 'Email is incorrect!'})
        
    return render(request, 'login.html')

def logout(request):
    request.session.clear()
    return redirect('home')

def update_profile(request):
    username = request.session.get('username')
    
    if not username:
        return redirect('login')
    
    if request.method == 'POST':
        profile_picture = request.FILES['profile_picture']
        
        if not profile_picture.name.endswith(('.jpg', '.jpeg', '.png')):
            return JsonResponse({'error': 'File format is not supported!'})
        elif profile_picture.size > 2*1024*1024:
            return JsonResponse({'error': 'File size is too large!'})
        
        with open(f'app/static/profile_pictures/{username}.png', 'wb+') as destination:
            for chunk in profile_picture.chunks():
                destination.write(chunk)
                
        return JsonResponse({'message': 'Profile picture has been updated!'})
    
    return render(request, 'update_profile.html', {'username': username})
        

