// Обработка формы связи с техподдержкой
function handleSupportSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    
    const data = {
        access_key: formData.get('access_key'),
        name: formData.get('name'),
        phone: formData.get('phone'),
        email: formData.get('email'),
        subject: formData.get('subject'),
        message: formData.get('message'),
    };
    
    const messageDiv = document.getElementById('support-form-message');
    messageDiv.className = 'form-message';
    const sendingText = typeof supportTranslations !== 'undefined' ? supportTranslations.sending : 'Message is being sent...';
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
            const successText = typeof supportTranslations !== 'undefined' ? supportTranslations.success : 'Thank you! Your message has been sent successfully. We will contact you soon.';
            messageDiv.textContent = successText;
            
            event.target.reset();
        } else {
            messageDiv.className = 'form-message error';
            const errorText = typeof supportTranslations !== 'undefined' ? supportTranslations.error : 'An error occurred while sending the message. Please try again.';
            messageDiv.textContent = errorText;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageDiv.className = 'form-message error';
        const errorText = typeof supportTranslations !== 'undefined' ? supportTranslations.error : 'An error occurred while sending the message. Please try again.';
        messageDiv.textContent = errorText;
    });
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

