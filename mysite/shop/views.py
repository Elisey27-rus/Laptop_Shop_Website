from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import redirect, reverse
from .models import Product, User_profile, CartItem
from .forms import ProductForm, CategoryForm, UserProfileForm, UserRegistrationForm
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from random import shuffle


def main_page(request):
    products = list(Product.objects.all())
    shuffle(products)

    items_per_page = 10
    paginator = Paginator(products, items_per_page)

    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    context = {
        'products_page': products_page
    }

    return render(request, 'shop/main_page.html', context=context)


def create(request, value):
    if value == 'product':
        template_dir = 'shop/create_product.html'
        form = ProductForm(request.POST, request.FILES)
    else:
        template_dir = 'shop/create_category.html'
        form = CategoryForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            url = reverse('main_page')
            return redirect(url)
    context = {
        'form': form
    }

    return render(request, template_dir, context=context)


def product_category_page(request, value):
    category_id = None
    if value == 'keybord':
        category_id = 1
        template_dir = 'shop/category_keybord.html'
        form = ProductForm(request.POST, request.FILES)
    elif value == 'mouse':
        category_id = 2
        template_dir = 'shop/category_mouse.html'
        form = ProductForm(request.POST, request.FILES)
    elif value == 'headphones':
        category_id = 3
        template_dir = 'shop/category_headphones.html'
        form = ProductForm(request.POST, request.FILES)
    elif value == 'spekers':
        category_id = 4
        template_dir = 'shop/category_spekers.html'
        form = ProductForm(request.POST, request.FILES)
    elif value == 'micro':
        category_id = 5
        template_dir = 'shop/category_micro.html'
        form = ProductForm(request.POST, request.FILES)
    elif value == 'seats':
        category_id = 6
        template_dir = 'shop/category_seats.html'
        form = ProductForm(request.POST, request.FILES)
    elif value == 'table':
        category_id = 7
        template_dir = 'shop/category_table.html'
        form = ProductForm(request.POST, request.FILES)
    elif value == 'ps':
        category_id = 8
        template_dir = 'shop/category_ps.html'
        form = ProductForm(request.POST, request.FILES)
    elif value == 'xbox':
        category_id = 9
        template_dir = 'shop/category_xbox.html'
        form = ProductForm(request.POST, request.FILES)
    else:
        template_dir = 'errors/error'

    products = Product.objects.filter(product_category_id=category_id)
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    context = {
        'products_page': products_page,
        'form': ProductForm(request.POST, request.FILES),
    }
    return render(request, template_dir, context=context)


class ProductDetailsView(DetailView):
    template_name = 'shop/product_details.html'
    model = Product
    context_object_name = "product"

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        quantity = int(request.POST.get('quantity', 1)) 

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('shop:main_page')


def start_page(request):
    context = {

    }
    return render(request, 'shop/start_page.html', context=context)


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('shop:main_page')

        return render(request, 'shop/login.html')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('shop:main_page')
    else:
        return render(request, 'shop/login.html', {'error': 'Invalid login credentials'})


class LogoutView(LogoutView):
    next_page = reverse_lazy('shop:main_page')


@login_required
def create_profile(request):
    try:
        user_profile = User_profile.objects.get(user=request.user)
    except User_profile.DoesNotExist:
        user_profile = User_profile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('shop:profile')

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'shop/profile-form.html', {'form': form})




@login_required
def profile_view(request):
    user_profile, created = User_profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('shop:profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'shop/profile.html', {'form': form, 'user_profile': user_profile})




class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'shop/registration.html'
    success_url = reverse_lazy(
        'shop:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    context = {
        'cart_items': cart_items
    }

    return render(request, 'shop/cart.html', context)
