// Aela Daily - Theme JavaScript
document.addEventListener('DOMContentLoaded', function() {
  // FAQ toggle
  document.querySelectorAll('.faq-item__question').forEach(function(q) {
    q.addEventListener('click', function() {
      this.parentElement.classList.toggle('faq-item--open');
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function(link) {
    link.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});
