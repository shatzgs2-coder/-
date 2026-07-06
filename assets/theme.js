/* Aela Daily - Theme JavaScript */

document.addEventListener('DOMContentLoaded', function() {

  /* === Mobile Menu Toggle === */
  var hamburger = document.querySelector('.header__hamburger');
  var nav = document.querySelector('.header__nav');

  if (hamburger && nav) {
    hamburger.addEventListener('click', function() {
      var expanded = hamburger.getAttribute('aria-expanded') === 'true';
      hamburger.setAttribute('aria-expanded', !expanded);
      nav.classList.toggle('header__nav--open');
      document.body.classList.toggle('no-scroll');
    });
  }

  /* === FAQ Accordion === */
  var faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(function(item) {
    item.addEventListener('click', function() {
      this.classList.toggle('open');
    });
  });

  /* === FAQ Category Filter === */
  var faqBtns = document.querySelectorAll('.faq-category-btn');
  faqBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      faqBtns.forEach(function(b) { b.classList.remove('active'); });
      this.classList.add('active');
      var category = this.getAttribute('data-category');
      faqItems.forEach(function(item) {
        if (category === 'all' || item.getAttribute('data-category') === category) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });

  /* === Quantity Buttons === */
  var qtyBtns = document.querySelectorAll('.cart-item__quantity-btn');
  qtyBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var input = this.parentElement.querySelector('.cart-item__quantity-value');
      if (!input) return;
      var val = parseInt(input.textContent) || 1;
      if (this.classList.contains('plus')) {
        input.textContent = val + 1;
      } else if (this.classList.contains('minus') && val > 1) {
        input.textContent = val - 1;
      }
    });
  });

  /* === Smooth Scroll === */
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

});
