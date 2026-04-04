/* =========================================================
   B&B COFFEE — Главный JavaScript
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

    /* ── Хедер: становится непрозрачным при скролле ── */
    const header = document.querySelector('.site-header');
    if (header && !header.classList.contains('solid')) {
        const onScroll = () => {
            header.classList.toggle('scrolled', window.scrollY > 40);
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    /* ── Мобильное меню ── */
    const burger = document.querySelector('.burger');
    const nav    = document.querySelector('.nav');
    if (burger && nav) {
        burger.addEventListener('click', () => {
            const open = nav.classList.toggle('open');
            burger.setAttribute('aria-expanded', open);
            burger.querySelectorAll('span')[0].style.transform = open ? 'rotate(45deg) translate(4px, 4.5px)' : '';
            burger.querySelectorAll('span')[1].style.opacity  = open ? '0' : '';
            burger.querySelectorAll('span')[2].style.transform = open ? 'rotate(-45deg) translate(4px, -4.5px)' : '';
        });
        // Закрыть при клике вне меню
        document.addEventListener('click', (e) => {
            if (nav.classList.contains('open') && !nav.contains(e.target) && !burger.contains(e.target)) {
                nav.classList.remove('open');
                burger.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
            }
        });
    }

    /* ── Появление элементов при скролле ── */
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    /* ── Навигация по категориям меню (активный пункт) ── */
    const menuLinks = document.querySelectorAll('.menu-nav-link');
    const menuSections = document.querySelectorAll('.menu-section[data-slug]');

    if (menuLinks.length && menuSections.length) {
        const sectionObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const slug = entry.target.dataset.slug;
                    menuLinks.forEach(link => {
                        link.classList.toggle('is-active', link.dataset.slug === slug);
                    });
                }
            });
        }, { rootMargin: '-30% 0px -60% 0px' });

        menuSections.forEach(s => sectionObserver.observe(s));

        // Плавный скролл к секции при клике
        menuLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(`.menu-section[data-slug="${link.dataset.slug}"]`);
                if (target) {
                    const offset = 72 + 56; // хедер + меню-нав
                    window.scrollTo({ top: target.offsetTop - offset, behavior: 'smooth' });
                }
            });
        });
    }

    /* ── Автоскрыть баннер успеха ── */
    const banner = document.querySelector('.success-banner');
    if (banner) {
        setTimeout(() => {
            banner.style.transition = 'opacity 0.8s, transform 0.8s';
            banner.style.opacity = '0';
            banner.style.transform = 'translateY(-8px)';
            setTimeout(() => banner.remove(), 800);
        }, 5000);
    }

    /* ── Анимация кнопки при отправке формы ── */
    const form = document.getElementById('reservationForm');
    if (form) {
        form.addEventListener('submit', () => {
            const btn = form.querySelector('.btn');
            if (btn) { btn.textContent = 'Отправка...'; btn.style.opacity = '0.7'; }
        });
    }

});
