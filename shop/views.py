from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, Product, Order, OrderItem, User, Wishlist
from .forms import RegisterForm, LoginForm, ProductForm, OrderAssignmentForm
from .cart import Cart
import urllib.parse

# --- FUNCIONES DE APOYO ---

def is_admin(user):
    return user.is_authenticated and user.is_staff

# --- VISTAS PÚBLICAS ---

def index(request):
    categories = Category.objects.all()[:4]
    products = Product.objects.all()[:6]
    featured_products = Product.objects.filter(is_featured=True).order_by('-created')[:3]
    context = {'categories': categories, 'products': products, 'featured_products': featured_products}
    return render(request, 'shop/index.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]
    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    context = {'product': product, 'related_products': related_products, 'is_in_wishlist': is_in_wishlist}
    return render(request, 'shop/product_detail.html', context)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(brand__icontains=query) | Q(sku__icontains=query) | Q(description__icontains=query))
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    brands = Product.objects.values_list('brand', flat=True).distinct()
    context = {'category': category, 'categories': categories, 'products': products, 'brands': [b for b in brands if b], 'query': query}
    return render(request, 'shop/product_list.html', context)

# --- CARRITO DE COMPRAS ---

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    current_qty = cart.cart.get(str(product.id), {}).get('quantity', 0)
    if current_qty + 1 > product.stock:
        return JsonResponse({'status': 'error', 'message': f'Solo quedan {product.stock} unidades.'}, status=400)
    cart.add(product=product)
    return JsonResponse({'status': 'ok', 'cart_count': len(cart)})

def cart_update_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    import json
    data = json.loads(request.body)
    quantity = int(data.get('quantity'))
    if 0 < quantity <= product.stock:
        cart.add(product=product, quantity=quantity, override_quantity=True)
        return JsonResponse({'status': 'ok', 'item_total': f"S/{(product.price * quantity):.2f}", 'cart_total': f"S/{cart.get_total_price():.2f}", 'cart_count': len(cart)})
    return JsonResponse({'status': 'error'}, status=400)

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

# --- CHECKOUT Y PAGOS ---

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0: return redirect('shop:product_list')
    if request.method == 'POST':
        method = request.POST.get('method')
        proof = request.FILES.get('proof')
        order = Order.objects.create(user=request.user, payment_method=method, payment_proof=proof, total_amount=cart.get_total_price(), status='PENDING')
        order_items_text = []
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            order_items_text.append(f"- {item['quantity']}x {item['product'].name}")
            item['product'].stock -= item['quantity']; item['product'].save()
        cart.clear()
        if method == 'WSP':
            msg = (f"Hola AdanStore! He realizado un pedido.\n\nProductos:\n" + "\n".join(order_items_text) + f"\n\nTotal: S/{order.total_amount}\nCliente: {request.user.email}\nID Cliente: #{request.user.id}\n\nMi comprobante de pago es:")
            msg_encoded = urllib.parse.quote(msg)
            return redirect(f"https://wa.me/51951141939?text={msg_encoded}")
        return render(request, 'shop/thanks.html', {'order': order})
    return render(request, 'shop/checkout.html', {'cart': cart})

@login_required
def order_reupload_proof(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user, status='REJECTED')
    if request.method == 'POST':
        proof = request.FILES.get('proof')
        if proof: order.payment_proof = proof; order.status = 'PENDING'; order.save(); return redirect('shop:profile')
    return render(request, 'shop/reupload_proof.html', {'order': order})

# --- VISTAS DE USUARIO ---

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).exclude(status='CANCELLED').prefetch_related('items__product').order_by('-created')
    return render(request, 'shop/profile.html', {'orders': orders})

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'shop/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created: wishlist_item.delete(); action = "removed"
    else: action = "added"
    return JsonResponse({'status': 'ok', 'action': action, 'count': request.user.wishlist_items.count()})

# Autenticación...
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST); 
        if form.is_valid(): user = form.save(); login(request, user); return redirect('shop:index')
    else: form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user: login(request, user); return redirect('shop:index')
    else: form = LoginForm()
    return render(request, 'shop/login.html', {'form': form})

def logout_view(request): logout(request); return redirect('shop:index')

# --- PANEL DE CONTROL (ADMIN) ---

@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.filter(status='COMPLETED').count(),
        'pending_orders': Order.objects.filter(status='PENDING').count(),
        'recent_orders': Order.objects.all().select_related('user')[:5],
        'recent_users': User.objects.all().order_by('-date_joined')[:5],
    }
    return render(request, 'shop/admin/dashboard.html', context)

@user_passes_test(is_admin)
def admin_products_list(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    selected_category = get_object_or_404(Category, slug=category_slug) if category_slug else None
    products = Product.objects.filter(category=selected_category) if selected_category else Product.objects.all()
    context = {'categories': categories, 'selected_category': selected_category, 'products': products.select_related('category')}
    return render(request, 'shop/admin/products_list.html', context)

@user_passes_test(is_admin)
def admin_add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES); 
        if form.is_valid(): form.save(); return redirect('shop:admin_products_list')
    else: form = ProductForm()
    return render(request, 'shop/admin/product_form.html', {'form': form, 'title': 'Nuevo Producto'})

@user_passes_test(is_admin)
def admin_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product); 
        if form.is_valid(): form.save(); return redirect('shop:admin_products_list')
    else: form = ProductForm(instance=product)
    return render(request, 'shop/admin/product_form.html', {'form': form, 'title': 'Editar Producto'})

@user_passes_test(is_admin)
def admin_delete_product(request, pk):
    get_object_or_404(Product, pk=pk).delete(); return redirect('shop:admin_products_list')

@user_passes_test(is_admin)
def admin_users_list(request):
    query = request.GET.get('q')
    users = User.objects.all().order_by('-date_joined')
    if query:
        if query.isdigit(): users = users.filter(Q(id=query) | Q(email__icontains=query))
        else: users = users.filter(email__icontains=query)
    return render(request, 'shop/admin/users_list.html', {'users': users, 'query': query})

@user_passes_test(is_admin)
def admin_user_detail(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    status_filter = request.GET.get('status')
    
    # Traemos TODOS los pedidos sin exclusiones iniciales
    orders = Order.objects.filter(user=target_user).prefetch_related('items__product')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'target_user': target_user,
        'orders': orders.order_by('-created'),
        'total_spent': sum(o.total_amount for o in Order.objects.filter(user=target_user, status='COMPLETED')),
        'current_status': status_filter
    }
    return render(request, 'shop/admin/user_detail.html', context)

@user_passes_test(is_admin)
def admin_assign_product(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = OrderAssignmentForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']; quantity = form.cleaned_data['quantity']; total = product.price * quantity
            order = Order.objects.create(user=target_user, notes=form.cleaned_data['notes'], total_amount=total, status='COMPLETED', is_completed=True)
            OrderItem.objects.create(order=order, product=product, price=product.price, quantity=quantity)
            return redirect('shop:admin_user_detail', user_id=user_id)
    else: form = OrderAssignmentForm()
    return render(request, 'shop/admin/assign_product.html', {'form': form, 'target_user': target_user})

@user_passes_test(is_admin)
def admin_orders_list(request):
    status_filter = request.GET.get('status')
    orders = Order.objects.all().select_related('user').prefetch_related('items__product')
    if status_filter: orders = orders.filter(status=status_filter)
    context = {'orders': orders.order_by('-created'), 'current_status': status_filter}
    return render(request, 'shop/admin/orders_list.html', context)

@user_passes_test(is_admin)
def admin_order_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = 'COMPLETED'; order.is_completed = True; order.save()
    return redirect(request.META.get('HTTP_REFERER', 'shop:admin_orders_list'))

@user_passes_test(is_admin)
def admin_order_reject(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = 'REJECTED'; order.save()
    return redirect(request.META.get('HTTP_REFERER', 'shop:admin_orders_list'))

@user_passes_test(is_admin)
def admin_order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk)
    for item in order.items.all(): item.product.stock += item.quantity; item.product.save()
    order.status = 'CANCELLED'; order.save()
    return redirect(request.META.get('HTTP_REFERER', 'shop:admin_orders_list'))

@user_passes_test(is_admin)
def admin_order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status != 'CANCELLED':
        for item in order.items.all(): item.product.stock += item.quantity; item.product.save()
    order.delete()
    return redirect(request.META.get('HTTP_REFERER', 'shop:admin_orders_list'))
