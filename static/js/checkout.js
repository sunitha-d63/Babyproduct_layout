 function changeMainImage(src, thumbElem) {
    document.getElementById("mainProductImage").src = src;
    document
      .querySelectorAll(".thumbnail")
      .forEach((t) => t.classList.remove("active"));
    thumbElem.classList.add("active");
  }
  function updateQuantity(delta) {
    const q = document.getElementById("quantity");
    let v = parseInt(q.textContent) + delta;
    q.textContent = Math.min(Math.max(v, 1), 10);
  }

  document.getElementById('mainProductImage').addEventListener('click', function() {
  this.classList.toggle('zoomed');
});



function updateQuantity(change) {
    const quantityElement = document.getElementById('quantity');
    const formQuantity = document.getElementById('form-quantity');
    let quantity = parseInt(quantityElement.textContent);
    quantity += change;
    if (quantity < 1) quantity = 1;
    quantityElement.textContent = quantity;
    formQuantity.value = quantity;
}