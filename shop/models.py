from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from cloudinary.models import CloudinaryField

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField('Correo electrónico', unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Emoji o clase de icono (ej: 🖱)", blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Categoría")
    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    brand = models.CharField(max_length=100, verbose_name="Marca", blank=True, help_text="Ej: Logitech, Razer, ATK")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Identificador (SKU)", help_text="Ej: ATK-ZERO-01")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="Descripción Corta (Hero)", help_text="Se muestra al lado de la imagen")
    detailed_description = models.TextField(verbose_name="Descripción Detallada (Markdown)", blank=True, help_text="Usa Markdown para tablas, listas, etc.")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio (S/)")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio Anterior (Opcional)")
    image = CloudinaryField(verbose_name="Imagen del Producto")
    
    is_new = models.BooleanField(default=False, verbose_name="¿Es Nuevo?")
    is_archive = models.BooleanField(default=False, verbose_name="¿Es del Archivo (Second Hand)?")
    is_sale = models.BooleanField(default=False, verbose_name="¿Está en Oferta?")
    is_featured = models.BooleanField(default=False, verbose_name="¿Destacar en el Hero?")
    
    stock = models.PositiveIntegerField(default=10)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.name} ({self.sku})"

class Order(models.Model):
    PAYMENT_METHODS = (
        ('WSP', 'WhatsApp'),
        ('YAPE', 'Yape / Plin'),
        ('TRANS', 'Transferencia Bancaria'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente de Verificación'),
        ('COMPLETED', 'Completado / Entregado'),
        ('REJECTED', 'Rechazado (Requiere nuevo comprobante)'),
        ('CANCELLED', 'Anulado / Sin Stock'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Cliente")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Pedido")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='WSP', verbose_name="Método de Pago")
    payment_proof = CloudinaryField(verbose_name="Comprobante de Pago", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', verbose_name="Estado del Pedido")
    notes = models.TextField(blank=True, verbose_name="Notas del Pedido")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False, verbose_name="¿Está Pagado?")

    class Meta:
        verbose_name = "Pedido / Asignación"
        verbose_name_plural = "Pedidos / Asignaciones"
        ordering = ('-created',)

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio al momento de compra")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = "Lista de Deseos"
        verbose_name_plural = "Listas de Deseos"
