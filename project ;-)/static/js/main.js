// PartLink Main JavaScript
// Handles alerts, form validation, and interactive features

document.addEventListener('DOMContentLoaded', function () {
  // ============ THEME TOGGLE ============
  setupThemeToggle();

  // ============ AUTO-HIDE ALERTS ============
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // ============ DELETE CONFIRMATION ============
  const deleteForms = document.querySelectorAll('.form-delete');
  deleteForms.forEach(form => {
    form.addEventListener('submit', function (e) {
      if (!confirm('Are you sure you want to delete this? This cannot be undone.')) {
        e.preventDefault();
      }
    });
  });

  // ============ HIGHLIGHT ACTIVE NAV LINK ============
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ============ QUANTITY INPUT VALIDATION ============
  const quantityInputs = document.querySelectorAll('[data-min-qty]');
  quantityInputs.forEach(input => {
    input.addEventListener('change', function () {
      const minQty = parseInt(this.getAttribute('data-min-qty'));
      const value = parseInt(this.value) || 0;
      if (value < minQty) {
        this.value = minQty;
        showNotification(`Minimum quantity is ${minQty}`, 'warning');
      }
    });
  });

  // ============ SEARCH SUGGESTIONS ============
  const searchInput = document.querySelector('input[name="q"]');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const query = this.value.trim();
      if (query.length > 2) {
        // Can implement live search here in future
        console.log('Searching for:', query);
      }
    });
  }

  // ============ FORM VALIDATION ============
  const forms = document.querySelectorAll('form:not(.form-delete)');
  forms.forEach(form => {
    form.addEventListener('submit', function (e) {
      if (!validateForm(this)) {
        e.preventDefault();
      }
    });
  });

  // ============ PRICE CALCULATOR ============
  setupPriceCalculator();
});

// Custom notification system
function showNotification(message, type = 'info') {
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type}`;
  alertDiv.innerHTML = `
    ${type === 'success' ? '✅' : type === 'error' ? '❌' : type === 'warning' ? '⚠️' : 'ℹ️'}
    ${message}
  `;
  
  const container = document.querySelector('[style*="padding"]') || document.body;
  container.insertBefore(alertDiv, container.firstChild);

  setTimeout(() => {
    alertDiv.style.transition = 'opacity 0.5s';
    alertDiv.style.opacity = '0';
    setTimeout(() => alertDiv.remove(), 500);
  }, 5000);
}

// Form validation helper
function validateForm(form) {
  let isValid = true;
  
  const requiredFields = form.querySelectorAll('[required]');
  requiredFields.forEach(field => {
    if (!field.value.trim()) {
      field.classList.add('error');
      isValid = false;
    } else {
      field.classList.remove('error');
    }
  });

  // Email validation
  const emailFields = form.querySelectorAll('[type="email"]');
  emailFields.forEach(field => {
    if (field.value && !isValidEmail(field.value)) {
      field.classList.add('error');
      isValid = false;
    } else {
      field.classList.remove('error');
    }
  });

  return isValid;
}

// Email validation helper
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Price calculator for orders
function setupPriceCalculator() {
  const qtyInput = document.querySelector('input[name="quantity"]');
  const pricePerUnit = document.querySelector('[data-price-per-unit]');
  const totalDisplay = document.getElementById('total-price');

  if (qtyInput && pricePerUnit && totalDisplay) {
    const price = parseFloat(pricePerUnit.getAttribute('data-price-per-unit'));
    qtyInput.addEventListener('input', function () {
      const qty = parseInt(this.value) || 0;
      const total = qty * price;
      totalDisplay.innerHTML = '₹' + total.toFixed(2);
    });
  }
}

// Utility: Format currency
function formatCurrency(amount) {
  return '₹' + parseFloat(amount).toFixed(2);
}

// Utility: Format date
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('en-IN', options);
}

// Theme Toggle logic
function setupThemeToggle() {
  const toggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeIcon');
  if (!toggleBtn || !themeIcon) return;

  // Initialize icon based on current theme defined in head script
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
  themeIcon.textContent = currentTheme === 'light' ? '🌙' : '☀️';

  toggleBtn.addEventListener('click', () => {
    let currentTheme = document.documentElement.getAttribute('data-theme');
    let newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    // Animate rotation during theme change
    themeIcon.style.transition = 'transform 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
    themeIcon.style.transform = 'rotate(-180deg) scale(0.5)';
    
    setTimeout(() => {
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      themeIcon.textContent = newTheme === 'light' ? '🌙' : '☀️';
      themeIcon.style.transform = 'rotate(0deg) scale(1)';
    }, 150); // change icon smoothly mid-rotation
  });
}
