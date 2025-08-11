  function toggleFaq(button) {
            const faqItem = button.closest('.faq-item');
            const answer = faqItem.querySelector('.faq-answer');
            const toggle = faqItem.querySelector('.faq-toggle');
            
            if (answer.style.display === 'none') {
                answer.style.display = 'block';
                toggle.textContent = '▴';
            } else {
                answer.style.display = 'none';
                toggle.textContent = '▾';
            }
        }