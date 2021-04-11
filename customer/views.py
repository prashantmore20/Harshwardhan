import json
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        # Get Every Items from Each Category
        # HouseholdItems = MenuItem.objects.filter(category__name__contains='HouseholdItems')
        # Sanitizers = MenuItem.objects.filter(category__name__contains='Sanitizer')
        menu_items = MenuItem.objects.all()

        # Pass in to Context
        context = {
            # 'HouseholdItems': HouseholdItems,
            # 'Sanitizers': Sanitizers
            'menu_items': menu_items
        }

        # Render in to html
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        order_items = {
            'items' : []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'cgst': menu_item.cgst,
                'sgst': menu_item.sgst,
                'price': menu_item.price,
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
            
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip,
        )
        order.items.add(*item_ids)

        # after everythong is done, send an email confirmation
        body = ('Thank You for Your Order, Your Order is under shipment.. We will confirm you upon the order has been shipped..\n'
                f'Order Items: {order_items}\n'
                f'Your Total : {price}\n'

        )
        send_mail(
            'Thank You for your Order!!',
            body,
            'example@example.com',
            ['email'],
            fail_silently=False
        )
        context = {
            'items': order_items['items'],
            'price': price,
        }

        return redirect('order-confirmation', pk=order.pk)

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }
            
        return render(request, 'customer/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        data = jason.loads(request.body)
        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')

class BillingPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/billing_pay_confirmation.html')

class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render (request, 'customer/menu.html', context)

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query)|
            Q(price__icontains=query)|
            Q(discription__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)