from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta, date
import bcrypt

from .models import User, Quote

def login_reg_page(request):
    return render(request, 'login.html')


def create_user(request):
    potential_users = User.objects.filter(email = request.POST['email'])

    if len(potential_users) != 0:
        messages.error(request, "User with that email already exists!")
        return redirect('/')

    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')

    hashed_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw,
    )

    request.session['user_id'] = new_user.id

    return redirect('/success')


def login(request):
    potential_users = User.objects.filter(email = request.POST['email'])

    if len(potential_users) == 0:
        messages.error(request, "Please check your email and password.")
        return redirect('/')

    user = potential_users[0]

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Please check your email and password.")
        return redirect('/')

    request.session['user_id'] = user.id

    return redirect('/success')


def success(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'current_user': current_user,
    }
    return render(request, 'success.html', context)


def quotes(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')
     
    current_user = User.objects.get(id=request.session['user_id'])
    liked = Quote.objects.filter(user_who_like=current_user)
    quotes = Quote.objects.exclude(id__in=[l.id for l in liked])
    this_user = Quote.objects.filter(quoter__id=request.session['user_id'])

   

    context = {
        'this_user' : this_user, 
        'quotes' : quotes,
        'current_user': current_user,
        'liked' : liked,
        
    }

    return render(request, 'quotes.html', context)
def create_quote(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')
    if request.method =='POST':
        errors = User.objects.quote_validator(request.POST)

        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect('/quotes')
    

    current_user = User.objects.get(id=request.session['user_id'])

    new_quote = Quote.objects.create(
        author = request.POST["author"],
        message = request.POST['message'],
        quoter = current_user
        
    )



    return redirect('/quotes')
def eliminate_quote(request, quote_id):
    deleted=Quote.objects.get(id=quote_id)
    if deleted.quoter.id == request.session["user_id"]:
        deleted.delete()

    return redirect('/quotes')



def profile(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')

        
    quoter = User.objects.get(id=user_id)
    context = {
        'quotes': Quote.objects.filter(quoter = quoter),
        'quoter': quoter 
    }

    return render(request, 'profile.html', context)


def edit_quote(request, quote_id):
    
    
    quote = Quote.objects.get(id=quote_id)
   
    context = {
        
        'quote' : quote
    }
    return render(request, 'edit.html', context)


def edit(request, quote_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')
    quote = Quote.objects.get(id=quote_id)
    if request.method =='POST':
        errors = User.objects.quote_validator(request.POST)

        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect(f'/edit_quote/{quote.id}')

    
        updates=Quote.objects.get(id=quote_id)
        updates.author=request.POST['author']
        updates.message=request.POST['message']
        updates.save()
        return redirect ('/quotes')

def favorite(request, quote_id):
    
    user_id=request.session['user_id']
    quoteobject=Quote.objects.get(id=quote_id)
    this_user=User.objects.get(id=user_id)
    quoteobject.user_who_like.add(this_user)
    return redirect ('/quotes')


def unfavorite(request, quote_id):
    
    user_id=request.session['user_id']
    quoteobject=Quote.objects.get(id=quote_id)
    this_user=User.objects.get(id=user_id)
    quoteobject.user_who_like.remove(this_user)
    return redirect ('/quotes')

def logout(request):
    if 'user_id' not in request.session:
        messages.error(request, "You are not logged in!")
        return redirect('/')

    request.session.clear()

    return redirect('/')