// ─── PartLink Main JS ─────────────────────────────
// Dynamic canvas background + UI interactions

/* ═══════════════════════════════════════════════════
   1. DYNAMIC PARTICLE CANVAS BACKGROUND
═══════════════════════════════════════════════════ */
(function () {
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let W, H, particles, mouseX = -999, mouseY = -999;
  const PARTICLE_COUNT = 80;
  const MAX_DIST = 130;

  function isLight() {
    return document.documentElement.getAttribute('data-theme') === 'light';
  }

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function mkParticle() {
    return {
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.8 + 0.4,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      // alternate cyan / violet / white-ish
      hue: Math.random() < 0.45 ? 192 : Math.random() < 0.7 ? 252 : 220,
    };
  }

  function init() {
    resize();
    particles = Array.from({ length: PARTICLE_COUNT }, mkParticle);
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);

    const light = isLight();
    const alpha = light ? 0.55 : 1;

    // ── draw lines between nearby particles ──
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < MAX_DIST) {
          const lineAlpha = (1 - dist / MAX_DIST) * (light ? 0.12 : 0.22) * alpha;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `hsla(${particles[i].hue},80%,70%,${lineAlpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }

    // ── draw particles ──
    particles.forEach(p => {
      const mouseDist = Math.hypot(p.x - mouseX, p.y - mouseY);
      const glowRadius = mouseDist < 120 ? p.r * 3 : p.r;

      ctx.beginPath();
      ctx.arc(p.x, p.y, glowRadius, 0, Math.PI * 2);
      const baseAlpha = light ? 0.45 : 0.7;
      ctx.fillStyle = `hsla(${p.hue},90%,75%,${baseAlpha})`;
      ctx.shadowBlur = mouseDist < 120 ? 14 : 6;
      ctx.shadowColor = `hsl(${p.hue},90%,70%)`;
      ctx.fill();
      ctx.shadowBlur = 0;

      // move
      p.x += p.vx;
      p.y += p.vy;

      // slight mouse repulsion
      if (mouseDist < 100) {
        const force = (100 - mouseDist) / 100;
        p.x += (p.x - mouseX) * force * 0.02;
        p.y += (p.y - mouseY) * force * 0.02;
      }

      // wrap edges
      if (p.x < -10) p.x = W + 10;
      if (p.x > W + 10) p.x = -10;
      if (p.y < -10) p.y = H + 10;
      if (p.y > H + 10) p.y = -10;
    });

    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  window.addEventListener('mousemove', e => { mouseX = e.clientX; mouseY = e.clientY; });
  window.addEventListener('mouseleave', () => { mouseX = -999; mouseY = -999; });

  init();
  draw();
})();


/* ═══════════════════════════════════════════════════
   2. THEME TOGGLE
═══════════════════════════════════════════════════ */
function setupThemeToggle() {
  const btn  = document.getElementById('themeToggleBtn');
  const icon = document.getElementById('themeIcon');
  if (!btn || !icon) return;

  const cur = document.documentElement.getAttribute('data-theme') || 'dark';
  icon.textContent = cur === 'light' ? '🌙' : '☀️';

  btn.addEventListener('click', () => {
    icon.style.transition = 'transform 0.45s cubic-bezier(.68,-.55,.265,1.55)';
    icon.style.transform  = 'rotate(-180deg) scale(0.4)';

    setTimeout(() => {
      const current = document.documentElement.getAttribute('data-theme');
      const next    = current === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      icon.textContent = next === 'light' ? '🌙' : '☀️';
      icon.style.transform = 'rotate(0deg) scale(1)';
    }, 160);
  });
}


/* ═══════════════════════════════════════════════════
   3. COUNTER ANIMATION (for hero stats)
═══════════════════════════════════════════════════ */
function animateCounters() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const target  = parseInt(el.getAttribute('data-count'), 10);
    const suffix  = el.getAttribute('data-suffix') || '';
    let current   = 0;
    const step    = Math.ceil(target / 60);
    const timer   = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current.toLocaleString() + suffix;
      if (current >= target) clearInterval(timer);
    }, 20);
  });
}


/* ═══════════════════════════════════════════════════
   4. DOMContentLoaded — wire everything up
═══════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', function () {
  setupThemeToggle();
  animateCounters();

  // ── Auto-hide alerts after 5 s ──
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      alert.style.opacity    = '0';
      alert.style.transform  = 'translateX(20px)';
      setTimeout(() => alert.remove(), 600);
    }, 5000);
  });

  // ── Active nav link highlight ──
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === path) link.classList.add('active');
  });

  // ── Delete confirmation ──
  document.querySelectorAll('.form-delete').forEach(form => {
    form.addEventListener('submit', e => {
      if (!confirm('Are you sure you want to delete this? This action cannot be undone.'))
        e.preventDefault();
    });
  });

  // ── Min-qty validation ──
  document.querySelectorAll('[data-min-qty]').forEach(input => {
    input.addEventListener('change', function () {
      const min = parseInt(this.getAttribute('data-min-qty'));
      if (parseInt(this.value) < min) { this.value = min; showNotification(`Minimum quantity is ${min}`, 'warning'); }
    });
  });

  // ── Form validation ──
  document.querySelectorAll('form:not(.form-delete)').forEach(form => {
    form.addEventListener('submit', e => { if (!validateForm(form)) e.preventDefault(); });
  });

  // ── Price calculator ──
  setupPriceCalculator();

  // scroll-reveal is handled purely by CSS animations
});


/* ═══════════════════════════════════════════════════
   6. NOTIFICATION TOAST
═══════════════════════════════════════════════════ */
function showNotification(message, type = 'info') {
  const div = document.createElement('div');
  div.className = `alert alert-${type}`;
  div.style.cssText = 'position:fixed;top:80px;right:1.5rem;z-index:9999;max-width:360px;animation:slideInAlert .4s ease;';
  div.innerHTML = `${type==='success'?'✅':type==='error'?'❌':type==='warning'?'⚠️':'ℹ️'} ${message}`;
  document.body.appendChild(div);
  setTimeout(() => {
    div.style.transition = 'opacity .5s, transform .5s';
    div.style.opacity = '0'; div.style.transform = 'translateX(20px)';
    setTimeout(() => div.remove(), 500);
  }, 4500);
}


/* ═══════════════════════════════════════════════════
   7. PRICE CALCULATOR
═══════════════════════════════════════════════════ */
function setupPriceCalculator() {
  const qty   = document.querySelector('input[name="quantity"]');
  const ppu   = document.querySelector('[data-price-per-unit]');
  const total = document.getElementById('total-price');
  if (!qty || !ppu || !total) return;
  const price = parseFloat(ppu.getAttribute('data-price-per-unit'));
  qty.addEventListener('input', function () {
    const q = parseInt(this.value) || 0;
    total.innerHTML = '₹' + (q * price).toFixed(2);
  });
}


/* ═══════════════════════════════════════════════════
   8. FORM VALIDATION
═══════════════════════════════════════════════════ */
function validateForm(form) {
  let ok = true;
  form.querySelectorAll('[required]').forEach(f => {
    if (!f.value.trim()) { f.classList.add('error'); ok = false; }
    else f.classList.remove('error');
  });
  form.querySelectorAll('[type="email"]').forEach(f => {
    if (f.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value)) {
      f.classList.add('error'); ok = false;
    } else f.classList.remove('error');
  });
  return ok;
}
