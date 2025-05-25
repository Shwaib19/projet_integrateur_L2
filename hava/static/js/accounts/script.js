export function init() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const sidebarMenu = document.getElementById('sidebarMenu');
    const body = document.body;

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

    const authToggleBtns = document.querySelectorAll('.toggle-btn');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const formsViewport = document.querySelector('.forms-slider-viewport');
    const transitionDuration = 500; // Should match --transition-duration in CSS (in ms)

    // Function to update forms viewport height
    const updateFormsViewportHeight = (targetForm) => {
        if (formsViewport && targetForm) {
            // Ensure the target form is visible before calculating height
            // This might require a slight delay if the form is just becoming visible
             // For sliding animation, the form is already position: absolute and size is calculable
             // but it's better to wait for it to be fully 'in view' or visible
             // A simple approach is to use requestAnimationFrame or a small timeout
            requestAnimationFrame(() => {
                // Ensure form is ready in the DOM for height calculation
                 const formHeight = targetForm.scrollHeight;
                 if (formHeight > 0) {
                     formsViewport.style.height = formHeight + 'px';
                 } else {
                     // Fallback or retry if height is 0 initially
                     setTimeout(() => {
                         formsViewport.style.height = targetForm.scrollHeight + 'px';
                     }, 50); // Small delay
                 }
            });
        }
    };


    // Set initial viewport height
    if (formsViewport && loginForm) {
        // Use the update function for initial height as well
         updateFormsViewportHeight(loginForm);
         // Also update height if the window resizes, as form content might reflow
         window.addEventListener('resize', () => {
             const activeBtn = document.querySelector('.toggle-btn.active');
             if (activeBtn) {
                 const formType = activeBtn.getAttribute('data-form');
                 const currentActiveForm = formType === 'login' ? loginForm : signupForm;
                 updateFormsViewportHeight(currentActiveForm);
             } else {
                  // Default to login form height if no button is active
                 updateFormsViewportHeight(loginForm);
             }
         });
    }


    if (authToggleBtns.length > 0 && loginForm && signupForm && formsViewport) {
        authToggleBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const formType = btn.getAttribute('data-form');

                authToggleBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                let targetForm, outgoingForm;

                if (formType === 'login') {
                    targetForm = loginForm;
                    outgoingForm = signupForm;

                    // Prepare login form to slide in (from wherever it is)
                    loginForm.style.visibility = 'visible'; // Make visible first
                    loginForm.style.transform = 'translateX(0%)';
                    loginForm.style.opacity = '1';
                    loginForm.style.zIndex = '2';

                    // Prepare signup form to slide out (to the right)
                    signupForm.style.transform = 'translateX(100%)';
                    signupForm.style.opacity = '0';
                    signupForm.style.zIndex = '1';
                    // Hide it completely after the transition
                    setTimeout(() => {
                        signupForm.style.visibility = 'hidden';
                        // Reset transform slightly after hiding to avoid brief flash on next reveal
                        // This might not be necessary with opacity 0 but is safer.
                         signupForm.style.transform = 'translateX(100%)';
                    }, transitionDuration);

                } else { // formType === 'signup'
                    targetForm = signupForm;
                    outgoingForm = loginForm;

                    // Prepare signup form to slide in (from wherever it is)
                    signupForm.style.visibility = 'visible'; // Make visible first
                    signupForm.style.transform = 'translateX(0%)';
                    signupForm.style.opacity = '1';
                    signupForm.style.zIndex = '2';

                    // Prepare login form to slide out (to the left)
                    loginForm.style.transform = 'translateX(-100%)';
                    loginForm.style.opacity = '0';
                    loginForm.style.zIndex = '1';
                     // Hide it completely after the transition
                    setTimeout(() => {
                        loginForm.style.visibility = 'hidden';
                        // Reset transform slightly after hiding
                         loginForm.style.transform = 'translateX(-100%)';
                    }, transitionDuration);
                }

                // Adjust viewport height to the target form's height
                if (targetForm) {
                    updateFormsViewportHeight(targetForm);
                }
            });
        });
    }

    const authForms = document.querySelectorAll('.auth-form-content');
    authForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const formData = new FormData(form);
            const formContainer = form.closest('.auth-form'); // Get the #login-form or #signup-form
            const formType = formContainer ? formContainer.id : null;


            if (formType === 'signup-form') {
                const password = formData.get('password');
                const confirmPassword = formData.get('confirm-password');

                if (password !== confirmPassword) {
                    alert('Les mots de passe ne correspondent pas.');
                    return;
                }

                const termsCheckbox = form.querySelector('input[name="terms"]');
                if (termsCheckbox && !termsCheckbox.checked) {
                    alert('Vous devez accepter les conditions d\'utilisation.');
                    return;
                }
            }

            const submitBtn = form.querySelector('.submit-btn');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = formType === 'login-form' ? 'Connexion en cours...' : 'Création en cours...';
            submitBtn.disabled = true;

            setTimeout(() => {
                const success = Math.random() < 0.8;

                if (success) {
                    alert(formType === 'login-form' ? 'Connexion réussie!' : 'Compte créé avec succès!');
                    form.reset();
                    if (formType === 'signup-form') {
                        // Simulate click on login toggle button to switch back with animation
                        const loginToggleBtn = document.querySelector('.toggle-btn[data-form="login"]');
                        if (loginToggleBtn) {
                            loginToggleBtn.click();
                        }
                    }
                } else {
                    alert(formType === 'login-form' ? 'Échec de la connexion. Veuillez vérifier vos identifiants.' : 'Échec de la création du compte. Veuillez réessayer.');
                }

                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    });
}