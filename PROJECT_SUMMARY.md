# AdanStore v1 — Resumen de Estado del Proyecto

Este documento sirve como memoria técnica del progreso realizado hasta el 17 de abril de 2026.

## 🚀 Funcionalidades Implementadas

### 1. Arquitectura Base
- **Django 6.0.4**: Localización en Soles (S/) y zona horaria de Lima.
- **Usuarios Personalizados**: Autenticación mediante Email. Los usuarios tienen un `CLIENTE_ID` visible en su perfil.
- **Cloudinary**: Integración para almacenamiento de imágenes en la nube.
- **Seguridad**: Uso de variables de entorno mediante `.env`.

### 2. Tienda y Experiencia de Usuario
- **Catálogo Dinámico**: Filtrado por categorías, marcas, precios y estado (Nuevo/Segunda Mano).
- **Ficha de Producto**: Soporte para descripciones técnicas en **Markdown**.
- **Carrito de Compras AJAX**: Gestión de cantidades y eliminación sin recargar la página.
- **Wishlist**: Sistema de favoritos con contador dinámico en el Navbar.
- **Modo Oscuro/Claro**: Selector persistente (guarda preferencia en localStorage).

### 3. Flujo de Pago (Localización Perú)
- **WhatsApp**: Redirección automática con mensaje detallado (incluye ID de cliente).
- **Pago Manual**: Datos de Yape/Plin, BCP y BBVA visibles en el checkout.
- **Comprobantes**: Opción para subir captura de pantalla directamente.
- **Reintento de Pago**: Si el admin rechaza un comprobante, el usuario puede volver a subirlo desde su perfil.

### 4. Panel de Control (Custom Admin)
- **Gestión de Catálogo**: CRUD completo agrupado por categorías.
- **Gestión de Clientes**: Buscador por ID/Email y expedientes individuales.
- **Control de Pedidos**: Sistema de estados (Pendiente, Verificado, Rechazado, Cancelado).
- **Gestión de Stock**: Descuento automático al comprar y devolución al cancelar.

## 🛠️ Comandos Útiles
- Iniciar Servidor: `python manage.py runserver`
- Crear Superusuario: `python manage.py createsuperuser`
- Actualizar DB: `python manage.py makemigrations` -> `python manage.py migrate`

---
*Documento generado automáticamente por Gemini CLI.*
