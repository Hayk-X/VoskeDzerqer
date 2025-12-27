function updateCartCount() {
    const savedCart = localStorage.getItem('shaurma_cart');
    const cartCount = document.getElementById('cart-count');
    
    if (!cartCount) return;
    
    if (savedCart) {
        const cart = JSON.parse(savedCart);
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        
        if (totalItems > 0) {
            cartCount.textContent = totalItems;
            cartCount.classList.remove('empty');
        } else {
            cartCount.textContent = '0';
            cartCount.classList.add('empty');
        }
    } else {
        cartCount.textContent = '0';
        cartCount.classList.add('empty');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    
    const cartIcon = document.getElementById('cart-icon');
    if (cartIcon) {
        cartIcon.addEventListener('click', function() {
            if (typeof showCart === 'function') {
                showCart();
            } else {
                window.location.href = '/menu/';
            }
        });
    }
    
    window.addEventListener('storage', function(e) {
        if (e.key === 'shaurma_cart') {
            updateCartCount();
        }
    });
    
    window.addEventListener('cartUpdated', function() {
        updateCartCount();
    });
});

window.updateCartCount = updateCartCount;

