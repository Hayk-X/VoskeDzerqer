document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.querySelector('.newsletter-form');
    const newsletterInput = document.querySelector('.newsletter-input');
    const newsletterBtn = document.querySelector('.newsletter-btn');
    
    if (newsletterForm && newsletterInput && newsletterBtn) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = newsletterInput.value.trim();
            
            if (!email) {
                const enterEmail = document.querySelector('[data-translate="enter-email"]')?.textContent || 'Please enter email address';
                alert(enterEmail);
                return;
            }
            
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                const validEmail = document.querySelector('[data-translate="valid-email"]')?.textContent || 'Please enter a valid email address';
                alert(validEmail);
                return;
            }
            
            newsletterBtn.innerHTML = '✓';
            newsletterBtn.style.backgroundColor = '#4caf50';
            newsletterBtn.style.borderColor = '#4caf50';
            newsletterInput.value = '';
            newsletterInput.disabled = true;
            
            setTimeout(function() {
                newsletterBtn.innerHTML = '✉';
                newsletterBtn.style.backgroundColor = '#FF8C00';
                newsletterBtn.style.borderColor = '#FF8C00';
                newsletterInput.disabled = false;
            }, 3000);
            
            if (typeof alert !== 'undefined') {
                setTimeout(function() {
                    const thanksText = document.querySelector('[data-translate="thanks-subscribe"]')?.textContent || 'Thank you for subscribing!';
                    alert(thanksText);
                }, 500);
            }
        });
    }
});

