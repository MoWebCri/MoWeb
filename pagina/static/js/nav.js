document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.header');
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.header .nav');

    // Manejo del scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Manejo del menú móvil
    menuToggle.addEventListener('click', function() {
        nav.classList.toggle('active');
        document.body.classList.toggle('menu-open');
    });

    // Cerrar menú al hacer clic en un enlace
    const navLinks = document.querySelectorAll('.header .nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            nav.classList.remove('active');
            document.body.classList.remove('menu-open');
        });
    });

    // Cerrar menú al hacer clic fuera
    document.addEventListener('click', function(event) {
        if (nav.classList.contains('active') && 
            !event.target.closest('.header')) {
            nav.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    });
}); 