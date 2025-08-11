
document.addEventListener('DOMContentLoaded', function() {
    const filterToggle = document.querySelector('.filter-toggle');
    const filterColumn = document.querySelector('.filter-column');
    const filterOverlay = document.querySelector('.filter-overlay');
    
    if (filterToggle) {
        filterToggle.addEventListener('click', function() {
            filterColumn.classList.toggle('show');
            filterOverlay.style.display = filterOverlay.style.display === 'block' ? 'none' : 'block';
        });
        
        filterOverlay.addEventListener('click', function() {
            filterColumn.classList.remove('show');
            filterOverlay.style.display = 'none';
        });
    }
    
    const priceRange = document.getElementById('priceRange');
    if (priceRange) {
        priceRange.addEventListener('input', function() {
            document.getElementById('priceValue').textContent = '$' + this.value;
        });
    }
});
