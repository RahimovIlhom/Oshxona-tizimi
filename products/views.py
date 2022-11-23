from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from products.models import Category, Product, OrderProduct, Order
import datetime

def create_ref_code():
    order_last = Order.objects.all().last()
    if order_last == None:
        return 1
    else:
        order_last_number = order_last.ref_code
        if order_last_number >= 99:
            return 1
        else:
            number = order_last_number + 1
            return number


def professions_page(request):
    if request.user.is_authenticated:
        return render(request, 'profession.html', {
        })
    else:
        response = redirect('/accounts/login/')
        return response


def cashier_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.profession == 'cashier':
            all_category = Category.objects.all()
            objects = []
            for category in all_category:
                category_products = Product.objects.filter(category=category)
                objects.append({'category': category, 'products': category_products})
            try:
                order = Order.objects.filter(ordered=False).last()
                context = {
                    'objects': objects,
                    'order_one': order,
                }
            except ObjectDoesNotExist:
                context = {
                    'objects': objects,
                }
            return render(request, 'profession-cashier.html', context)
        else:
            return redirect('/page/not_found/')
    else:
        response = redirect('/accounts/login/')
        return response

@login_required
def add_to_card(request, id):
    product = get_object_or_404(Product, id=id)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        ordered=False,
    )
    order_qs = Order.objects.filter(ordered=False)
    if order_qs.exists():
        order = order_qs.last()
        if order.products.filter(product__id=product.id).exists():
            order_product.quantity += 1
            order_product.save()
            order.cash = order.get_total()
            order.save()
            # messages.info(request, "Bu mahsulot miqdori yangilandi!")
            return redirect("/profession/cashier")
        else:
            order.products.add(order_product)
            order.cash = order.get_total()
            order.save()
            # messages.info(request, "Mahsulot qo'shildi!")
            return redirect('/profession/cashier')
    else:
        ordered_date = timezone.now()
        new_ref_code = create_ref_code()
        cash = order_product.get_final_price()
        order = Order.objects.create(
            ordered_date=ordered_date,
            ref_code=new_ref_code,
            cash=cash,
        )
        order.products.add(order_product)
        # messages.info(request, "Mahsulot qo'shildi!")
        return redirect('/profession/cashier')

@login_required
def remove_from_card(request, id):
    product = get_object_or_404(Product, id=id)
    order_qs = Order.objects.filter(
        ordered=False,
    )
    if order_qs.exists():
        order = order_qs.last()
        if order.products.filter(product__id=product.id).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                ordered=False,
            )[0]
            order.products.remove(order_product)
            order_product.delete()
            # messages.info(request, "Bu mahsulot olib tashlandi!")
            return redirect('/profession/cashier')
        else:
            # messages.info(request, "This item was not in your cart")
            return redirect('/profession/cashier')
    else:
        # messages.info(request, "You do not have an active order")
        return redirect('/profession/cashier')

@login_required
def products_ordered(request, ref_code):
    try:
        order_qs = Order.objects.filter(ordered=False, ref_code=ref_code)
    except ObjectDoesNotExist:
        return redirect("/profession/cashier")
    else:
        try:
            order_products = OrderProduct.objects.filter(ordered=False)
        except ObjectDoesNotExist:
            return redirect("/profession/cashier")
        else:
            if order_products:
                ordered_date = timezone.now()
                for order_product in order_products:
                    order_product.ordered = True
                    order_product.save()
                order = order_qs.last()
                order.ordered = True
                order.ordered_date = ordered_date
                order.save()
                # messages.info(request, "Buyurtma berildi!")
                return redirect("/profession/cashier")
            else:
                return redirect("/profession/cashier")

class UpdatePartialPaymentView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'partial-payment.html'
    fields = ['cash', 'plastic']

@login_required
def order_completed(request, ref_code):
    try:
        order_qs = Order.objects.filter(order_completed=False, ref_code=ref_code)
    except ObjectDoesNotExist:
        return redirect("/profession/chef")
    else:
        order_complete_date = timezone.now()
        order_last = order_qs.last()
        order_last.order_completed = True
        order_last.order_completed_date = order_complete_date
        order_last.save()
        return redirect("/profession/chef")


def chef_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.profession == 'chef':
            today = datetime.date.today()
            today_orders = reversed(Order.objects.filter(ordered_date__gte=today, ordered=True))
            return render(request, 'profession-chef.html', {
                'today': today,
                'today_orders': today_orders,
            })
        else:
            return redirect('/page/not_found/')
    else:
        return redirect('/accounts/login/')


def accountant_view(request):
    if request.user.is_superuser or request.user.profession == 'accountant':
        today = datetime.date.today()
        today_orders = Order.objects.filter(ordered_date__gte=today)
        orders_price = list(map(lambda order: order.get_order_price(), today_orders))
        summa = sum(orders_price)
        return render(request, 'admin_page/home.html', {
            'today': today,
            'today_orders': reversed(today_orders),
            'summa': summa,
        })
    else:
        return redirect('/page/not_found/')

def accountant_view1(request):
    if request.user.is_superuser or request.user.profession == 'accountant':
        today = datetime.date.today()
        week = datetime.date.today() - datetime.timedelta(days=7)
        week_orders = Order.objects.filter(ordered_date__gte=week)
        orders_price = list(map(lambda order: order.get_order_price(), week_orders))
        summa = sum(orders_price)
        return render(request, 'admin_page/home1.html', {
            'today': today.strftime('%d.%m.%Y'),
            'week': week.strftime('%d.%m'),
            'week_orders': reversed(week_orders),
            'summa': summa,
        })
    else:
        return redirect('/page/not_found/')


def accountant_view2(request):
    if request.user.is_superuser or request.user.profession == 'accountant':
        today = datetime.date.today()
        month = datetime.date.today() - datetime.timedelta(days=30)
        month_orders = Order.objects.filter(ordered_date__gte=month)
        orders_price = list(map(lambda order: order.get_order_price(), month_orders))
        summa = sum(orders_price)
        return render(request, 'admin_page/home2.html', {
            'today': today.strftime('%d.%m.%Y'),
            'month': month.strftime('%d.%m'),
            'month_orders': reversed(month_orders),
            'summa': summa,
        })
    else:
        return redirect('/page/not_found/')


def categories_view(request):
    if request.user.is_superuser or request.user.profession == 'accountant':
        all_categoies = Category.objects.all()

        return render(request, 'admin_page/categories.html', {
            'categories': all_categoies,
        })
    else:
        return redirect('/page/not_found/')

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    template_name = 'admin_page/create_category.html'
    fields = ['name', ]

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser

class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    template_name = 'admin_page/update_category.html'
    fields = ['name']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'admin_page/delete_category.html'
    success_url = reverse_lazy('categories')

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser

@login_required
def products_view(request):
    if request.user.is_superuser or request.user.profession == 'accountant':
        products = Product.objects.all()

        return render(request, 'admin_page/products.html', {
            'products': products,
        })
    else:
        return redirect('/page/not_found/')

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    template_name = 'admin_page/create_product.html'
    fields = ['name', 'price', 'discount_price', 'category',]

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'admin_page/update_product.html'
    fields = ['name', 'price', 'discount_price', 'category',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'admin_page/delete_product.html'
    success_url = reverse_lazy('products')

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser