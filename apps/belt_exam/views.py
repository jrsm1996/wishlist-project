from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Item

def flashErrors(request, errors):
    for error in errors:
        messages.error(request, error)

def index(request):
    if 'user_id' in request.session:
        return redirect('/dashboard')
    return render(request, 'belt_exam/index.html')

def login(request):
    if request.method == 'POST':
        errors = User.objects.validateLogin(request.POST)
        if errors:
            flashErrors(request, errors)
        else:
            user = User.objects.get(username = request.POST['username'])
            request.session['user_id'] = user.id
            return redirect('/dashboard')
    return redirect('/')

def register(request):
    if request.method == 'POST':
        errors = User.objects.validateRegistration(request.POST)
        if errors:
            flashErrors(request, errors)
        else:
            user = User.objects.createUser(request.POST)
            request.session['user_id'] = user.id
            return redirect('/dashboard')
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.currentUser(request)
    wishlist = user.items.all()
    other_items = Item.objects.exclude(id__in = wishlist)
    context = {
        'current_user': user,
        'wishlist': wishlist,
        'other_items': other_items

    }
    return render(request, 'belt_exam/dashboard.html', context)

def logout(request):
    request.session.pop('user_id')
    return redirect('/')

def createPage(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'belt_exam/create.html')

def create(request):
    if request.method == "POST":
        errors = []
        if len(request.POST['item_name']) < 3:
            errors.append('Please enter an item name that is 3 or more characters.')
            flashErrors(request, errors)
        else:
            user = User.objects.currentUser(request)
            item = Item.objects.create(
                name = request.POST['item_name'],
                creator = user
            )
            item.users.add(user)
            return redirect('/dashboard')
    return redirect('/wish_items/create')

def deleteItem(request, id):
    user = User.objects.currentUser(request)
    item = Item.objects.get(id = id)
    item.delete()
    return redirect('/dashboard')

def addItem(request, id):
    user = User.objects.currentUser(request)
    item = Item.objects.get(id = id)
    item.users.add(user)
    return redirect('/dashboard')

def removeItem(request, id):
    user = User.objects.currentUser(request)
    item = Item.objects.get(id = id)
    item.users.remove(user)
    return redirect('/dashboard')

def itemPage(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    item = Item.objects.get(id = id)
    users = item.users.all()
    context = {
        'item': item,
        'users': users
    }
    return render(request, 'belt_exam/itempage.html', context)
