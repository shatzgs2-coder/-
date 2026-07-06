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

  /* === Product Page - Variant Selection === */
  var variantDataEl = document.getElementById('product-variants-data');
  if (variantDataEl) {
    try { window.productVariants = JSON.parse(variantDataEl.textContent); } catch(e) {}
  }

  var optionBtns = document.querySelectorAll('.product-form__option-btn:not(:disabled)');
  optionBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      // Update sibling buttons in same group
      var parent = this.parentElement;
      parent.querySelectorAll('.product-form__option-btn').forEach(function(b) {
        b.classList.remove('is-active');
      });
      this.classList.add('is-active');

      // Update label
      var labelSpan = parent.previousElementSibling.querySelector('.product-form__selected-value');
      if (labelSpan) labelSpan.textContent = this.getAttribute('data-value');

      // Find matching variant
      updateSelectedVariant();
    });
  });

  function updateSelectedVariant() {
    if (!window.productVariants || !window.productVariants.variants) return;

    // Gather currently selected values from each option group
    var selectedOptions = [];
    document.querySelectorAll('.product-form__option').forEach(function(group) {
      var activeBtn = group.querySelector('.product-form__option-btn.is-active');
      selectedOptions.push(activeBtn ? activeBtn.getAttribute('data-value') : '');
    });

    // Find variant that matches all selections
    var matchedVariant = null;
    window.productVariants.variants.forEach(function(v) {
      var match = true;
      v.options.forEach(function(opt, i) {
        if (opt !== selectedOptions[i]) match = false;
      });
      if (match && !matchedVariant) matchedVariant = v;
    });

    if (matchedVariant) {
      // Update hidden input
      var hiddenInput = document.getElementById('variant-id');
      if (hiddenInput) hiddenInput.value = matchedVariant.id;

      // Update price display
      var priceEl = document.getElementById('variant-price');
      if (priceEl) {
        var moneyFormat = window.Shopify?.money_format || '${{amount}}';
        var formattedPrice = formatMoney(matchedVariant.price, moneyFormat);
        priceEl.textContent = formattedPrice;

        // Compare at price
        var priceContainer = document.getElementById('product-price');
        var compareEl = priceContainer.querySelector('.product-card__compare-price');
        if (compareEl) {
          if (matchedVariant.compare_at_price > matchedVariant.price) {
            compareEl.textContent = formatMoney(matchedVariant.compare_at_price, moneyFormat);
            compareEl.style.display = '';
          } else {
            compareEl.style.display = 'none';
          }
        }
      }

      // Enable/disable ATC
      var atcBtn = document.querySelector('.product-form__add-to-cart[name="add"]');
      if (atcBtn) {
        if (matchedVariant.available) {
          atcBtn.disabled = false;
          atcBtn.textContent = document.querySelector('[data-add-text]')?.textContent || 'Add to Cart';
        } else {
          atcBtn.disabled = true;
          atcBtn.textContent = document.querySelector('[data-soldout-text]')?.textContent || 'Sold Out';
        }
      }
    }
  }

  function formatMoney(cents, format) {
    // Simple EUR formatting fallback
    if (typeof cents === 'string') cents = parseInt(cents, 10);
    return '€' + (cents / 100).toFixed(2).replace('.', ',');
  }

  /* === Product Page - Quantity Controls (+/-) === */
  document.querySelectorAll('.qty-control__btn--minus').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var input = this.parentElement.querySelector('.qty-control__input');
      if (!input) return;
      var val = parseInt(input.value, 10) || 1;
      if (val > 1) input.value = val - 1;
    });
  });

  document.querySelectorAll('.qty-control__btn--plus').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var input = this.parentElement.querySelector('.qty-control__input');
      if (!input) return;
      var val = parseInt(input.value, 10) || 1;
      input.value = val + 1;
    });
  });

  /* === Cart Page - Quantity Buttons === */
  var cartQtyBtns = document.querySelectorAll('.cart-item__quantity-btn');
  cartQtyBtns.forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      var input = this.parentElement.querySelector('.cart-item__quantity-value');
      if (!input) return;
      var val = parseInt(input.textContent, 10) || 1;
      if (this.classList.contains('plus')) {
        input.textContent = val + 1;
      } else if (this.classList.contains('minus') && val > 1) {
        input.textContent = val - 1;
      }
      var form = this.closest('form');
      if (form) {
        var nameInput = input.parentElement.querySelector('input[type="hidden"]');
        if (nameInput) nameInput.value = input.textContent;
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
