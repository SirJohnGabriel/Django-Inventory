from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.urls import reverse

from authuserapp.models import InventoryItem
from authuserapp.utils.mq import send_inventory_update_notif
from .forms import LoginUserForm
from .forms import RegisterUserForm
from .forms import InventoryForm

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("authuserapp:dashboard"))
    
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)

                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse("authuserapp:dashboard"))
                else:
                    messages.error(request, "Invalid email or passowrd")
            except User.DoesNotExist:
                messages.error(request, "User with this email does not exist")
    else:
        form = LoginUserForm()

    return render(request, 'authuserapp/index.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('authuserapp:authhome')


# logged in user dashboard
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'authuserapp/dashboard.html')

    else:
        return redirect('authuserapp:authhome')

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful")
            return redirect('authuserapp:authhome')
        else:
            print(form.errors)
    else:
        form = RegisterUserForm()
    
    return render(request, 'authuserapp/register.html', {'form': form})

def inventory(request):
    items = InventoryItem.objects.all()
    return render(request, 'authuserapp/inventory.html', {'items': items})

@login_required
def inventory_list(request):
    items = InventoryItem.objects.all()
    return render(request, 'authuserapp/inventory_list.html', {'items': items})

@login_required
def inventory_create(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authuserapp:inventory_list')
    else:
        form = InventoryForm()
    
    return render(request, 'authuserapp/inventory_form.html', {'form': form})

@login_required
def inventory_update(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    original_item = {
        'sku': item.sku,
        'price': float(item.price),
        'count': item.count,
        'status': item.status,
    }

    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            update_item = form.save()

            changes = {}
            if original_item['sku'] != update_item.sku:
                changes['sku'] = {'from': original_item['sku'], 'to': update_item.sku}
            if original_item['price'] != float(update_item.price):
                changes['price'] = {'from': original_item['price'], 'to': float(update_item.price)}
            if original_item['count'] != update_item.count:
                changes['count'] = {'from': original_item['count'], 'to': update_item.count}
            if original_item['status'] != update_item.status:
                changes['status'] = {'from': original_item['status'], 'to': update_item.status}

            if changes:
                payload = {
                    'items_id': update_item.id,
                    'changes': changes
                }
                send_inventory_update_notif(payload)

            return redirect('authuserapp:inventory_list')
    else:
        form = InventoryForm(instance=item)

    return render(request, 'authuserapp/inventory_form.html', {'form': form})
            

@login_required
def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('authuserapp:inventory_list')
    return render(request, 'authuserapp/inventory_confirm_delete.html', {'item': item})