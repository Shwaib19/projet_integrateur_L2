export function init() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const sidebarMenu = document.getElementById('sidebarMenu');
    const body = document.body;
    const navLinks = sidebarMenu.querySelectorAll('nav ul li a');

    if (mobileMenuToggle && sidebarMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            body.classList.toggle('menu-open');
            const isExpanded = body.classList.contains('menu-open');
            mobileMenuToggle.setAttribute('aria-expanded', isExpanded);
            if (isExpanded) {
                mobileMenuToggle.setAttribute('aria-label', 'Fermer le menu');
            } else {
                mobileMenuToggle.setAttribute('aria-label', 'Ouvrir le menu');
            }
        });
    }

    // Close menu when a nav link is clicked (useful for single-page navigation)
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (body.classList.contains('menu-open')) {
                body.classList.remove('menu-open');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
                mobileMenuToggle.setAttribute('aria-label', 'Ouvrir le menu');
            }
            // Active link styling
            navLinks.forEach(nav => nav.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // Set active link based on scroll
    
}