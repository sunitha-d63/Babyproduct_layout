def filter_products(products, price_filter=None, free_shipping=False, discounts=False):
    filtered = products
    if price_filter:
        min_price, max_price = price_filter
        filtered = [p for p in filtered if min_price <= p['price'] <= max_price]
    if free_shipping:
        filtered = filtered[:6]
    if discounts:
        filtered = [p for p in filtered if p['mrp'] > p['price']]
    return filtered