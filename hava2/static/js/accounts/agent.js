document.addEventListener('DOMContentLoaded', function() {
    // Animation pour les cartes
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        }, index * 150);
    });

    // Animation pour les statistiques
    const statBoxes = document.querySelectorAll('.stat-box');
    statBoxes.forEach((box, index) => {
        const statNumber = box.querySelector('.stat-number');
        const finalValue = parseInt(statNumber.textContent);
        let currentValue = 0;
        
        setTimeout(() => {
            const interval = setInterval(() => {
                currentValue += Math.ceil(finalValue / 20);
                if (currentValue >= finalValue) {
                    currentValue = finalValue;
                    clearInterval(interval);
                }
                statNumber.textContent = currentValue;
            }, 30);
        }, 500 + (index * 200));
    });

    // Effet de survol amélioré pour les cartes
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
            this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = 'var(--shadow)';
        });
    });

    // Navigation active
    const navLinks = document.querySelectorAll('nav ul li a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
});

