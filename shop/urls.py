from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('tienda/', views.product_list, name='product_list'),
    path('tienda/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Carrito y Pago
    path('carrito/', views.cart_detail, name='cart_detail'),
    path('carrito/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('carrito/update/<int:product_id>/', views.cart_update_quantity, name='cart_update'),
    path('carrito/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('finalizar-compra/', views.checkout, name='checkout'),

    # Wishlist
    path('favoritos/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    path('perfil/', views.profile_view, name='profile'),
    path('registro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Rutas del Panel de Control (Admin)
    path('control/', views.admin_dashboard, name='admin_dashboard'),
    path('control/productos/', views.admin_products_list, name='admin_products_list'),
    path('control/productos/nuevo/', views.admin_add_product, name='admin_add_product'),
    path('control/productos/editar/<int:pk>/', views.admin_edit_product, name='admin_edit_product'),
    path('control/productos/eliminar/<int:pk>/', views.admin_delete_product, name='admin_delete_product'),
    path('control/usuarios/', views.admin_users_list, name='admin_users_list'),
    path('control/usuarios/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('control/usuarios/asignar/<int:user_id>/', views.admin_assign_product, name='admin_assign_product'),
    path('control/historial/', views.admin_orders_list, name='admin_orders_list'),
    path('pedido/re-comprobante/<int:pk>/', views.order_reupload_proof, name='reupload_proof'),
    path('control/pedido/completar/<int:pk>/', views.admin_order_complete, name='admin_order_complete'),
    path('control/pedido/rechazar/<int:pk>/', views.admin_order_reject, name='admin_order_reject'),
    path('control/pedido/cancelar/<int:pk>/', views.admin_order_cancel, name='admin_order_cancel'),
    path('control/pedido/eliminar/<int:pk>/', views.admin_order_delete, name='admin_order_delete'),
]
