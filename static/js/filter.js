
  function applyFilter(options) {
    const url = new URL(window.location);
    const params = url.searchParams;

    if ('min_price' in options) {
      params.set('min_price', options.min_price);
      params.set('max_price', options.max_price);
    }
    if ('free_shipping' in options) {
      options.free_shipping ? params.set('free_shipping', 'true') : params.delete('free_shipping');
    }
    if ('discounts' in options) {
      options.discounts ? params.set('discounts', 'true') : params.delete('discounts');
    }

    window.location = url.pathname + '?' + params.toString();
  }


document.querySelectorAll('.buy-btn').forEach(button => {
    button.addEventListener('click', async function() {
        const productId = this.dataset.productId;
        
        try {
            const response = await fetch('/verify_product', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product_id: productId
                })
            });

            if (!response.ok) {
                throw new Error('Product unavailable');
            }

           
            window.location.href = `/checkout/${productId}`;
            
        } catch (error) {
            console.error('Error:', error);
        }
    });
});
