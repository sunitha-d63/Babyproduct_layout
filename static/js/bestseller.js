document.addEventListener('DOMContentLoaded', () => {
  const carousel = document.getElementById('bestsellerCarousel');
  carousel.addEventListener('slide.bs.carousel', (e) => {
    const indicators = document.querySelectorAll('#bestsellerCarousel .carousel-indicators button');
    indicators.forEach((btn, idx) => {
      if (idx === e.to) {
        btn.style.width = '16px';
        btn.style.height = '16px';
        btn.style.backgroundColor = '#28729c';
      } else {
        btn.style.width = '10px';
        btn.style.height = '10px';
        btn.style.backgroundColor = '#4b93bc';
      }
    });
  });
});
