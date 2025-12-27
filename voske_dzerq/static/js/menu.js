// Корзина
let cart = [];

document.addEventListener('DOMContentLoaded', function() {
    const savedCart = localStorage.getItem('shaurma_cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
    }
    
    if (typeof updateCartCount === 'function') {
        updateCartCount();
    }

    const addToCartButtons = document.querySelectorAll('.btn-add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.getAttribute('data-item-id');
            const itemName = this.getAttribute('data-item-name');
            const itemPrice = parseFloat(this.getAttribute('data-item-price'));
            
            addToCart(itemId, itemName, itemPrice);
        });
    });
    
    const cartIcon = document.getElementById('cart-icon');
    if (cartIcon) {
        cartIcon.addEventListener('click', showCart);
    }

    const modal = document.getElementById('cart-modal');
    const closeBtn = document.querySelector('.close');
    const goToOrderBtn = document.getElementById('go-to-order');

    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }

    if (goToOrderBtn) {
        goToOrderBtn.addEventListener('click', function() {
            window.location.href = '/contact/';
        });
    }

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});

function addToCart(itemId, itemName, itemPrice) {
    const existingItem = cart.find(item => item.id === itemId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: itemId,
            name: itemName,
            price: itemPrice,
            quantity: 1
        });
    }

    localStorage.setItem('shaurma_cart', JSON.stringify(cart));
    
    if (typeof updateCartCount === 'function') {
        updateCartCount();
    }
    
    window.dispatchEvent(new Event('cartUpdated'));
    
}

function showCart() {
    const modal = document.getElementById('cart-modal');
    const cartItems = document.getElementById('cart-items');
    const cartTotalPrice = document.getElementById('cart-total-price');
    
    if (!modal || !cartItems) return;

    cartItems.innerHTML = '';
    
    if (cart.length === 0) {
        const emptyText = typeof translations !== 'undefined' ? translations.emptyCart : 'Cart is empty';
        cartItems.innerHTML = `<p>${emptyText}</p>`;
        cartTotalPrice.textContent = '0';
        modal.style.display = 'block';
        return;
    }

    let total = 0;
    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        const amdSymbol = typeof translations !== 'undefined' ? translations.amd : 'AMD';
        const removeText = typeof translations !== 'undefined' ? translations.remove : 'Remove';
        cartItem.innerHTML = `
            <div>
                <strong>${item.name}</strong><br>
                <small>${item.price} ${amdSymbol} × ${item.quantity}</small>
            </div>
            <div>
                <strong>${itemTotal.toFixed(2)} ${amdSymbol}</strong>
                <button onclick="removeFromCart('${item.id}')" style="margin-left: 10px; background: #FF6B35; color: #ffffff; border: 2px solid #FF6B35; padding: 5px 10px; border-radius: 3px; cursor: pointer; font-weight: bold;">×</button>
            </div>
        `;
        cartItems.appendChild(cartItem);
    });
    
    cartTotalPrice.textContent = total.toFixed(2);
    modal.style.display = 'block';
}

function removeFromCart(itemId) {
    cart = cart.filter(item => item.id !== itemId);
    localStorage.setItem('shaurma_cart', JSON.stringify(cart));
    
    if (typeof updateCartCount === 'function') {
        updateCartCount();
    }
    
    window.dispatchEvent(new Event('cartUpdated'));
    
    showCart();
}

function getOrderText() {
    if (cart.length === 0) return '';
    
    return cart.map(item => `${item.name} x${item.quantity}`).join(', ');
}

