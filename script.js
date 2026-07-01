const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
const progressBar = document.querySelector('.scroll-progress');
const year = document.getElementById('year');

if (year) year.textContent = new Date().getFullYear();

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
  });

  navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });
}

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

window.addEventListener('scroll', () => {
  const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
  const progress = maxScroll > 0 ? window.scrollY / maxScroll : 0;
  progressBar.style.transform = `scaleX(${progress})`;
});
