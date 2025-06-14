document.addEventListener('DOMContentLoaded', () => {
    const animatedCards = document.querySelectorAll('.animated-card');

    if (!animatedCards.length) {
        return;
    }

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add a delay based on the card's index for a staggered effect
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 150); // 150ms delay between each card
                
                // Stop observing the element once it's visible
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1 // Trigger when 10% of the element is visible
    });

    animatedCards.forEach(card => {
        observer.observe(card);
    });
});

