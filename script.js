// Initialize Web3Forms
const ACCESS_KEY = "bde969e2-32aa-46f8-a5b7-8f1eb2f8a5c1"; // Public key for Web3Forms

const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
const progressBar = document.querySelector('.scroll-progress');
const year = document.getElementById('year');
const profileCard = document.querySelector('.profile-card');
const contactForm = document.getElementById('contactForm');
const submitBtn = document.getElementById('submitBtn');

if (year) year.textContent = new Date().getFullYear();

// Mobile menu toggle
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
  });

  navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });
}

// Typed effect
const typed = document.querySelector('.typed');
if (typed) {
  const phrases = typed.dataset.phrases.split('.');
  let index = 0;
  let charIndex = 0;
  let deleting = false;
  const type = () => {
    const current = phrases[index % phrases.length];
    typed.textContent = current.slice(0, charIndex);
    if (!deleting && charIndex < current.length) {
      charIndex += 1;
    } else if (deleting && charIndex > 0) {
      charIndex -= 1;
    } else {
      deleting = !deleting;
      if (!deleting) index += 1;
    }
    setTimeout(type, deleting ? 40 : 90);
  };
  type();
}

// Active nav highlighting
const sections = document.querySelectorAll('main section[id]');
const navItems = document.querySelectorAll('.nav-links a');
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        navItems.forEach((item) => item.classList.toggle('active', item.getAttribute('href') === `#${entry.target.id}`));
      }
    });
  },
  { threshold: 0.45 }
);
sections.forEach((section) => observer.observe(section));

// Scroll reveal animations
const revealElements = document.querySelectorAll('.card, .project-card, .skill-card, .service-card, .stat-card, .testimonial-card, .timeline-step');
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('scroll-reveal');
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1, rootMargin: '0px 0px -100px 0px' }
);
revealElements.forEach((el) => {
  el.classList.add('scroll-reveal');
  revealObserver.observe(el);
});

// Counter animations
const counters = document.querySelectorAll('[data-counter]');
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = Number(el.dataset.counter || 0);
    const duration = 1200;
    const start = performance.now();
    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const value = Math.floor(progress * target);
      el.textContent = value.toLocaleString();
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
    counterObserver.unobserve(el);
  });
}, { threshold: 0.7 });
counters.forEach((counter) => counterObserver.observe(counter));

// Scroll progress bar
window.addEventListener('scroll', () => {
  const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
  const progress = maxScroll > 0 ? window.scrollY / maxScroll : 0;
  progressBar.style.transform = `scaleX(${progress})`;
});

// Profile card mouse tracking
if (profileCard) {
  window.addEventListener('pointermove', (event) => {
    const x = (event.clientX / window.innerWidth - 0.5) * 10;
    const y = (event.clientY / window.innerHeight - 0.5) * 10;
    profileCard.style.transform = `translate3d(${x}px, ${y}px, 0)`;
  });
  window.addEventListener('pointerleave', () => {
    profileCard.style.transform = '';
  });
}

// Form validation
function validateForm() {
  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  const message = document.getElementById('message').value.trim();
  let isValid = true;

  // Clear errors
  document.getElementById('nameError').textContent = '';
  document.getElementById('emailError').textContent = '';
  document.getElementById('messageError').textContent = '';

  if (!name) {
    document.getElementById('nameError').textContent = 'Name is required';
    isValid = false;
  }
  if (!email) {
    document.getElementById('emailError').textContent = 'Email is required';
    isValid = false;
  } else if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
    document.getElementById('emailError').textContent = 'Please enter a valid email';
    isValid = false;
  }
  if (!message) {
    document.getElementById('messageError').textContent = 'Message is required';
    isValid = false;
  } else if (message.length < 10) {
    document.getElementById('messageError').textContent = 'Message must be at least 10 characters';
    isValid = false;
  }

  return isValid;
}

// Contact form submission with Web3Forms
if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();

    // Show loading state
    submitBtn.disabled = true;
    document.querySelector('.btn-text').classList.add('hidden');
    document.querySelector('.btn-spinner').classList.remove('hidden');

    try {
      const response = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          access_key: ACCESS_KEY,
          name: name,
          email: email,
          message: message,
          subject: `New portfolio inquiry from ${name}`,
          from_name: 'Portfolio Contact Form',
          redirect: 'https://' + window.location.host + window.location.pathname + '#contact'
        })
      });

      const result = await response.json();

      if (result.success) {
        // Success
        document.getElementById('successMessage').classList.remove('hidden');
        document.getElementById('errorMessage').classList.add('hidden');
        contactForm.reset();

        // Hide success message after 5 seconds
        setTimeout(() => {
          document.getElementById('successMessage').classList.add('hidden');
        }, 5000);
      } else {
        throw new Error('Form submission failed');
      }
    } catch (error) {
      console.error('Form submission error:', error);
      document.getElementById('errorMessage').classList.remove('hidden');
      document.getElementById('successMessage').classList.add('hidden');
    } finally {
      submitBtn.disabled = false;
      document.querySelector('.btn-text').classList.remove('hidden');
      document.querySelector('.btn-spinner').classList.add('hidden');
    }
  });
}

// Verify all links and buttons
function verifyLinks() {
  const links = document.querySelectorAll('a[href]');
  const issues = [];

  links.forEach((link) => {
    const href = link.getAttribute('href');
    // Check for dead hash links
    if (href.startsWith('#') && href !== '#') {
      const target = document.querySelector(href);
      if (!target) {
        issues.push(`Dead link: ${href} in element: ${link.textContent}`);
      }
    }
  });

  if (issues.length > 0) {
    console.warn('Link issues found:', issues);
  } else {
    console.log('✓ All links verified');
  }
}

// Verify links on load
document.addEventListener('DOMContentLoaded', verifyLinks);

// Smooth scroll behavior for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href === '#') {
      e.preventDefault();
      return;
    }
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// Log page performance info
window.addEventListener('load', () => {
  if (window.performance && window.performance.timing) {
    const perf = window.performance.timing;
    const pageLoadTime = perf.loadEventEnd - perf.navigationStart;
    console.log(`Page load time: ${pageLoadTime}ms`);
  }
});
