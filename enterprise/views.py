from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin 
from django.utils.timezone import datetime
from customer.models import OrderModel

# Create your views here.

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        # Get the Current Date
        today = datetime.today()
        # orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)
        orders = OrderModel.objects.filter(is_shipped=False)
        
        # Loop throrough the Orders and add the price
        unshipped_orders = []
        total_revenue = 0
        for order in orders:
            total_revenue += order.price
            if not order.is_shipped:
                unshipped_orders.append(order)

        # Pass Total number of orders and total revenue
        context = {
            'orders': unshipped_orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders),
        } 
        return render(request, 'enterprise/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }

        return render (request, 'enterprise/order-details.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {
            'order': order,
        }

        return render (request, 'enterprise/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()