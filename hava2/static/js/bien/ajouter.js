document.addEventListener('DOMContentLoaded', function() {
    const propertyForm = document.getElementById('propertyForm');
    const resetBtn = document.getElementById('resetBtn');
    const confirmationModal = document.getElementById('confirmationModal');
    const closeModal = document.querySelector('.close-modal');
    const addAnotherBtn = document.getElementById('addAnotherBtn');
    const viewListBtn = document.getElementById('viewListBtn');
    
    // Store uploaded images data
    window.uploadedImages = [];
    
    // Handle form submission

    
    // Reset form
    resetBtn.addEventListener('click', function() {
        propertyForm.reset();
        clearImagePreviews();
        window.uploadedImages = [];
    });
    
    // Modal controls
    closeModal.addEventListener('click', closeConfirmationModal);
    addAnotherBtn.addEventListener('click', function() {
        closeConfirmationModal();
        propertyForm.reset();
        clearImagePreviews();
        window.uploadedImages = [];
    });
    
    viewListBtn.addEventListener('click', function() {
        // This would navigate to the property listing page in a real application
        alert('Cette fonctionnalité vous redirigerait vers la liste des propriétés dans une application réelle.');
        closeConfirmationModal();
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === confirmationModal) {
            closeConfirmationModal();
        }
    });
    
    // Form validation
    function validateForm() {
        let isValid = true;
        const requiredFields = propertyForm.querySelectorAll('[required]');
        
        // Remove any existing error messages
        const errorMessages = propertyForm.querySelectorAll('.error-message');
        errorMessages.forEach(message => message.remove());
        
        // Check required fields
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                showError(field, 'Ce champ est obligatoire');
            }
        });
        
        // Validate images
        if (window.uploadedImages.length === 0) {
            const imageField = document.getElementById('images');
            isValid = false;
            showError(imageField, 'Veuillez télécharger au moins une image');
        }
        
        return isValid;
    }
    
    // Show error message for a field
    function showError(field, message) {
        const parentElement = field.closest('.form-group'); 
        if (!parentElement) return; 

        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.style.color = 'var(--error-color)';
        errorElement.style.fontSize = '0.85rem';
        errorElement.style.marginTop = '0.25rem';
        errorElement.textContent = message;

        const insertAfterElement = field.closest('.file-upload') || field;
        if (insertAfterElement.nextElementSibling && insertAfterElement.nextElementSibling.classList.contains('error-message')) {
            return;
        }
        insertAfterElement.parentElement.insertBefore(errorElement, insertAfterElement.nextElementSibling);


        if (field.closest('.file-upload')) {
             field.closest('.file-upload').style.borderColor = 'var(--error-color)'; 
        } else {
             field.style.borderColor = 'var(--error-color)';
        }
       
        const fieldsToClearError = field.closest('.file-upload') ? [field.closest('.file-upload')] : [field];
        
        fieldsToClearError.forEach(element => {
             element.addEventListener('focus', function() {
                element.style.borderColor = '';
                const error = parentElement.querySelector('.error-message');
                if (error) {
                    error.remove();
                }
            }, { once: true }); 
        });

        if (field.type === 'file') {
             field.addEventListener('change', function() {
                const error = parentElement.querySelector('.error-message');
                if (error) {
                    error.remove();
                }
                 if (field.closest('.file-upload')) {
                     field.closest('.file-upload').style.borderColor = '';
                 }
             }, { once: true });
         }
    }
    
    // Save property data (in a real app, this would send to a server)
    function saveProperty(propertyData) {
        console.log('Property data saved:', propertyData);
        
        let properties = JSON.parse(localStorage.getItem('properties') || '[]');
        properties.push(propertyData);
        localStorage.setItem('properties', JSON.stringify(properties));
    }
    
    // Show confirmation modal with property summary
    function showConfirmationModal(propertyData) {
        document.getElementById('summaryTitle').textContent = propertyData.title;
        document.getElementById('summaryPrice').textContent = `${propertyData.price} € - ${propertyData.status === 'sale' ? 'À vendre' : 'À louer'}`;
        document.getElementById('summaryLocation').textContent = `${propertyData.address}, ${propertyData.zipcode} ${propertyData.city}, ${propertyData.country}`;
        document.getElementById('summaryUsage').textContent = `Usage: ${propertyData.usage}`;

        const summaryImage = document.getElementById('summaryImage');
        if (propertyData.images && propertyData.images.length > 0) {
            summaryImage.src = propertyData.images[0].dataUrl;
            summaryImage.style.display = 'block'; 
        } else {
             summaryImage.src = ''; 
             summaryImage.style.display = 'none'; 
        }
        
        confirmationModal.style.display = 'block';
    }
    
    // Close confirmation modal
    function closeConfirmationModal() {
        confirmationModal.style.display = 'none';
    }
});

// Handle image preview functionality
function previewImages(event) {
    const files = event.target.files;
    const previewContainer = document.getElementById('imagePreviewContainer');
    const maxImages = 5;
    const maxFileSize = 5 * 1024 * 1024; 
    
    // Don't clear existing previews if appending new images
    // clearImagePreviews();
    
    const validFiles = Array.from(files).filter(file => {
        if (!file.type.match('image.*')) {
            alert(`${file.name} n'est pas une image valide.`);
            return false;
        }
        if (file.size > maxFileSize) {
            alert(`${file.name} est trop volumineux. La taille maximale est de 5 Mo.`);
            return false;
        }
        return true;
    });

    if (validFiles.length > maxImages - window.uploadedImages.length) {
        alert(`Vous ne pouvez télécharger que ${maxImages} images maximum. Seules les ${maxImages - window.uploadedImages.length} premières seront conservées.`);
        validFiles.splice(maxImages - window.uploadedImages.length);
    }
    
    validFiles.forEach(file => {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const previewDiv = document.createElement('div');
            previewDiv.className = 'image-preview';
            
            const img = document.createElement('img');
            img.src = e.target.result;
            img.alt = 'Preview';
            
            const removeBtn = document.createElement('span');
            removeBtn.className = 'remove-image';
            removeBtn.innerHTML = '&times;';
            removeBtn.addEventListener('click', function() {
                previewDiv.remove();
                
                window.uploadedImages = window.uploadedImages.filter(image => image.dataUrl !== e.target.result);
                
                if (window.uploadedImages.length === 0) {
                    const fileInput = document.getElementById('images');
                    console.log('Removed image. Current images:', window.uploadedImages.length);
                }
                const imageField = document.getElementById('images');
                const parentElement = imageField.closest('.form-group');
                const error = parentElement ? parentElement.querySelector('.error-message') : null;
                if (error && window.uploadedImages.length > 0) {
                    error.remove();
                    if (imageField.closest('.file-upload')) {
                        imageField.closest('.file-upload').style.borderColor = '';
                    }
                }
            });
            
            previewDiv.appendChild(img);
            previewDiv.appendChild(removeBtn);
            previewContainer.appendChild(previewDiv);
            
            if (window.uploadedImages.length < maxImages) {
                window.uploadedImages.push({
                    name: file.name,
                    type: file.type,
                    size: file.size,
                    dataUrl: e.target.result 
                });
            } else {
                alert(`Maximum ${maxImages} images allowed. Skipping ${file.name}.`);
                previewDiv.remove(); 
            }
        };
        
        reader.readAsDataURL(file);
    });

}

// Clear all image previews and the stored images array
function clearImagePreviews() {
    const previewContainer = document.getElementById('imagePreviewContainer');
    previewContainer.innerHTML = '';
    window.uploadedImages = [];
    const imageField = document.getElementById('images');
    const parentElement = imageField.closest('.form-group');
    if (parentElement) {
        const error = parentElement.querySelector('.error-message');
        if (error) error.remove();
        if (imageField.closest('.file-upload')) {
            imageField.closest('.file-upload').style.borderColor = '';
        }
    }
    imageField.value = '';
}