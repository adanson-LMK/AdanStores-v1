from django import forms
from .models import User, Product, Category, Order

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Contraseña',
        'class': 'nl-input'
    }))
    
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'tu @correo.com',
                'class': 'nl-input'
            })
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'tu @correo.com',
        'class': 'nl-input'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Contraseña',
        'class': 'nl-input'
    }))

# --- FORMULARIOS DE ADMINISTRACIÓN ---

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'brand', 'sku', 'slug', 'description', 'detailed_description', 'price', 'old_price', 'image', 'is_new', 'is_archive', 'is_sale', 'is_featured', 'stock']
        widgets = {
            field: forms.TextInput(attrs={'class': 'nl-input'}) for field in ['name', 'sku', 'slug']
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'nl-input', 'rows': 3})
        self.fields['detailed_description'].widget = forms.Textarea(attrs={'class': 'nl-input', 'rows': 10, 'placeholder': 'Usa Markdown para especificaciones detalladas...'})
        self.fields['category'].widget.attrs.update({'class': 'nl-input'})

class OrderAssignmentForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'nl-input'}),
        label="Seleccionar Producto"
    )
    quantity = forms.IntegerField(
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'nl-input'}),
        label="Cantidad"
    )

    class Meta:
        model = Order
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'nl-input', 'rows': 3, 'placeholder': 'Ej: Nro de serie, estado de garantía...'}),
        }
