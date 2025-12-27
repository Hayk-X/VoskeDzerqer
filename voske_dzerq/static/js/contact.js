function handleSubmit(event) {
    event.preventDefault();
    
    const savedCart = localStorage.getItem('shaurma_cart');
    let orderText = '';
    
    if (savedCart) {
        const cart = JSON.parse(savedCart);
        if (cart.length > 0) {
            orderText = cart.map(item => `${item.name} x${item.quantity}`).join(', ');
        }
    }
    
    const orderInput = document.getElementById('inp_message');
    if (!orderInput.value && orderText) {
        orderInput.value = orderText;
    } else if (orderText) {
        orderInput.value = orderText + (orderInput.value ? ', ' + orderInput.value : '');
    }
    
    // Сбор данных формы
    const formData = new FormData(event.target);
    
    const data = {
        access_key: formData.get('access_key'),
        order: formData.get('order') || orderInput.value,
        phone: formData.get('phone'),
        email: formData.get('email'),
        address: formData.get('address') || '',
        comments: formData.get('comments') || '',
    };
    
    // Отправка на Web3Forms API
    const messageDiv = document.getElementById('form-message');
    messageDiv.className = 'form-message';
    const sendingText = typeof contactTranslations !== 'undefined' ? contactTranslations.sending : 'Order is being sent...';
    messageDiv.textContent = sendingText;
    messageDiv.style.display = 'block';
    
    fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            messageDiv.className = 'form-message success';
            const successText = typeof contactTranslations !== 'undefined' ? contactTranslations.success : 'Thank you! Your order has been sent successfully. We will contact you soon.';
            messageDiv.textContent = successText;
            
            // Очистка формы
            event.target.reset();
            
            // Очистка корзины
            localStorage.removeItem('shaurma_cart');
            
            // Обновляем счетчик корзины
            if (typeof updateCartCount === 'function') {
                updateCartCount();
            }
            
            // Отправляем событие для обновления счетчика
            window.dispatchEvent(new Event('cartUpdated'));
        } else {
            messageDiv.className = 'form-message error';
            const errorText = typeof contactTranslations !== 'undefined' ? contactTranslations.error : 'An error occurred while sending the order. Please try again.';
            messageDiv.textContent = errorText;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageDiv.className = 'form-message error';
        const errorText = typeof contactTranslations !== 'undefined' ? contactTranslations.error : 'An error occurred while sending the order. Please try again.';
        messageDiv.textContent = errorText;
    });
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

document.addEventListener('DOMContentLoaded', function() {
    const savedCart = localStorage.getItem('shaurma_cart');
    if (savedCart) {
        const cart = JSON.parse(savedCart);
        if (cart.length > 0) {
            const orderInput = document.getElementById('inp_message');
            if (orderInput) {
                const orderText = cart.map(item => `${item.name} x${item.quantity}`).join(', ');
                orderInput.value = orderText;
            }
        }
    }
});

