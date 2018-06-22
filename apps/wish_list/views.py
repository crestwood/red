from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Item, UserManager, ItemManager

def index(request):
    return render(request, 'wish_list/index.html')

def register(request):
    errors = User.objects.validReg(request.POST)
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/')
    tempPass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    User.objects.create(name=request.POST['name'],username=request.POST['username'], hired_at=request.POST['hired_at'],password=tempPass)
    request.session['username'] = request.POST['username']
    print(User.objects.all())
    return redirect('/home')

def login(request):
    if User.objects.filter(username=request.POST['username']):
        user = User.objects.get(username=request.POST['username'])
        request.session['username']=request.POST['username']
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['username']=request.POST['username']
            return redirect ('/home')
    messages.error(request, 'Username and Password do not match')
    return redirect('/')

def home(request):
    if 'username' not in request.session:
        return redirect('/')
    user = User.objects.get(username = request.session['username'])
    otheritems = Item.objects.exclude(liked_by=user)
    context = {
        'users': User.objects.all(),
        'items': Item.objects.all(),
        'me': User.objects.get(username=request.session['username']),
        'otheritems':otheritems,
    }
    print(user.liked_item.all())
    return render(request, 'wish_list/main.html',context)

def addItem(request):
    if 'username' not in request.session:
        return redirect('/')
    return render(request, 'wish_list/create.html')

def create(request):
    errors = Item.objects.validItem(request.POST)
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/addItem')
    user = User.objects.get(username = request.session['username'])
    Item.objects.create(name=request.POST['item'], added_by =user)
    return redirect ('/home')

def viewItem(request, id):
    if 'username' not in request.session:
        return redirect('/')
    context = {
        'item': Item.objects.get(id=id),
        'users': User.objects.all()
    }
    return render(request, 'wish_list/Item.html', context)

def like(request):
    user=User.objects.get(username=request.session['username'])
    item=Item.objects.get(id=request.POST['item_id'])
    item.liked_by.add(user)
    item.save()
    return redirect('/home')

def remove(request):
    item = Item.objects.get(id=request.POST['item_id'])
    user = User.objects.get(username=request.session['username'])
    item.liked_by.remove(user)
    item.save()
    return redirect('/home')

def delete(request):
    Item.objects.get(id=request.POST['item_id']).delete()
    return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect('/')