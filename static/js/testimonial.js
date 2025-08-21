
document.addEventListener('DOMContentLoaded', function() {
  var carousel = document.getElementById('testimonialCarousel');
  carousel.addEventListener('slide.bs.carousel', function (e) {
    var indicators = document.querySelectorAll('#testimonialCarousel .carousel-indicators button');
    indicators.forEach(function(indicator, index) {
      var distance = Math.abs(index - e.to);
      if (distance === 0) {
        indicator.style.width = '8px';
        indicator.style.height = '8px';
        indicator.style.backgroundColor = '#28729c';
      } else {
        indicator.style.width = '8px';
        indicator.style.height = '8px';
        indicator.style.backgroundColor = '#4b93bc';
      }
    });
  });
});
