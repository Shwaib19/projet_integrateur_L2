document.addEventListener('DOMContentLoaded', () => {
    // Thumbnail gallery functionality
    const mainImage = document.getElementById('main-property-image');
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            // Update main image source
            mainImage.src = this.src;
            
            // Update active class
            thumbnails.forEach(thumb => thumb.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Add hover effect for feature items
    const featureItems = document.querySelectorAll('.feature-item');
    
    featureItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Basic action button listeners (can be expanded)
    const likeButton = document.querySelector('.like-button');
    const editButton = document.querySelector('.edit-button');

    likeButton.addEventListener('click', () => {
        alert('Propriété aimée ! (Action fictive)');
        // Add actual like logic here (e.g., send to server)
    });

    editButton.addEventListener('click', () => {
        alert('Modifier la propriété (Action fictive)');
        // Add actual edit logic here (e.g., redirect to edit page)
    });
    
    // Add animation when page loads
    const propertyDetails = document.querySelector('.property-details');
    const propertyActions = document.querySelector('.property-actions');
    
    setTimeout(() => {
        propertyDetails.style.opacity = '1';
        propertyDetails.style.transform = 'translateY(0)';
        propertyActions.style.opacity = '1';
        propertyActions.style.transform = 'translateY(0)';
    }, 300);
});