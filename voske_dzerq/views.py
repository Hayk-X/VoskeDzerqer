from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MenuItem, Order
from .forms import OrderForm

def main_page(request):
    return render(request, "main.html")

def menu_page(request):
    category = request.GET.get('category', '')
    menu_items = MenuItem.objects.filter(is_available=True)
    
    if category:
        menu_items = menu_items.filter(category=category)
    
    categories = [
        (code, str(label)) for code, label in MenuItem.CATEGORY_CHOICES
    ]
    
    context = {
        'menu_items': menu_items,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, "menu.html", context)

def contact_page(request):
    return render(request, "contact.html")

def privacy_policy_page(request):
    return render(request, "privacy_policy.html")

def support_page(request):
    return render(request, "support.html")

def about_page(request):
    return render(request, "about.html")


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            from django.utils.translation import gettext as _
            messages.success(request, _('Order successfully created! Thank you, %(name)s!') % {'name': order.customer_name})
            return redirect('order_create')
    else:
        form = OrderForm()
    
    recent_orders = Order.objects.all()[:5]
    
    context = {
        'form': form,
        'recent_orders': recent_orders,
    }
    return render(request, 'order_form.html', context)

