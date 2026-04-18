// Theme Toggle
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

if (themeToggle) {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') body.classList.add('light-mode');

    themeToggle.addEventListener('click', () => {
        body.classList.toggle('light-mode');
        localStorage.setItem('theme', body.classList.contains('light-mode') ? 'light' : 'dark');
    });
}

// Add to Cart AJAX
document.querySelectorAll('.add-cart').forEach(btn => {
    btn.addEventListener('click', function() {
        const productId = this.getAttribute('data-id');
        const cartBadge = document.getElementById('cart-count');
        const stickyBadge = document.getElementById('sticky-cart-count');
        const originalText = this.innerText;

        if (!productId || this.disabled) return;

        // Desactivar temporalmente para evitar spam
        this.disabled = true;

        fetch(`/carrito/add/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                // Feedback visual exitoso
                this.innerText = '✓ Añadido';
                this.style.background = '#4ade80';
                this.style.color = '#000';

                // Actualizar badges
                if (cartBadge) {
                    cartBadge.style.display = 'block';
                    cartBadge.classList.add('update');
                    setTimeout(() => cartBadge.classList.remove('update'), 300);
                }
                if (stickyBadge) {
                    stickyBadge.style.display = 'flex';
                    stickyBadge.innerText = data.cart_count;
                    stickyBadge.classList.add('update');
                    setTimeout(() => stickyBadge.classList.remove('update'), 300);
                }

                // Restaurar botón después de 2 segundos
                setTimeout(() => {
                    this.innerText = originalText;
                    this.style.background = ''; // Vuelve al CSS original
                    this.style.color = '';
                    this.disabled = false;
                }, 2000);

            } else {
                // Manejar error de stock
                alert(data.message || "No se pudo añadir al carrito.");
                this.disabled = false;
            }
        })
        .catch(err => {
            console.error("Error:", err);
            this.disabled = false;
        });
    });
});

// Wishlist Toggle AJAX (Para todos los botones .wish-btn)
document.querySelectorAll('.wish-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault(); // Evitar que el clic haga scroll o navegue
        const productId = this.getAttribute('data-id');
        const icon = this.querySelector('svg');
        const countBadge = document.getElementById('wishlist-count');

        if (!productId) return;

        fetch(`/wishlist/toggle/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.status === 403) {
                window.location.href = '/login/';
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.status === 'ok') {
                if (data.action === 'added') {
                    this.classList.add('active');
                    icon.style.fill = 'currentColor';
                } else {
                    this.classList.remove('active');
                    icon.style.fill = 'none';
                }
                if (countBadge) countBadge.style.display = data.count > 0 ? 'block' : 'none';
            }
        })
        .catch(err => console.error("Error en wishlist:", err));
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Cursor and animations
const c1=document.getElementById('cur'), c2=document.getElementById('cur2');
let mx=0,my=0,rx=0,ry=0;
document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;});
(function loop(){
  if(c1 && c2){
    c1.style.left=mx+'px';c1.style.top=my+'px';
    rx+=(mx-rx)*.12;ry+=(my-ry)*.12;
    c2.style.left=rx+'px';c2.style.top=ry+'px';
  }
  requestAnimationFrame(loop);
})();

document.querySelectorAll('a,button').forEach(el=>{
  el.addEventListener('mouseenter',()=>document.body.classList.add('ha'));
  el.addEventListener('mouseleave',()=>document.body.classList.remove('ha'));
});

const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in');});},{threshold:.1});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

function faq(btn){
  const ans=btn.nextElementSibling,open=btn.classList.contains('open');
  document.querySelectorAll('.faq-q').forEach(b=>{b.classList.remove('open');b.nextElementSibling.classList.remove('open');});
  if(!open){btn.classList.add('open');ans.classList.add('open');}
}
window.faq = faq;
