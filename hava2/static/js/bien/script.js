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