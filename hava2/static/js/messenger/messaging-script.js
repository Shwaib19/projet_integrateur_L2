document.addEventListener('DOMContentLoaded', function() {
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    // Animation for the messaging interface
    const messagingElements = [
        document.querySelector('.contacts-sidebar'),
        document.querySelector('.chat-header'),
        document.querySelector('.chat-messages'),
        document.querySelector('.chat-input')
    ];

    messagingElements.forEach((element, index) => {
        // Set initial state for animation
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 150 + 100);
    });

    // Contact filtering functionality
    const filterButtons = document.querySelectorAll('.filter-btn');
    const contacts = document.querySelectorAll('.contact');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            const filterValue = this.getAttribute('data-filter');
            
            contacts.forEach(contact => {
                if (filterValue === 'all') {
                    contact.style.display = 'flex';
                } else if (filterValue === 'unread' && contact.classList.contains('unread')) {
                    contact.style.display = 'flex';
                } else if (filterValue === 'clients' && contact.getAttribute('data-type') === 'client') {
                    contact.style.display = 'flex';
                } else if (filterValue === 'agents' && contact.getAttribute('data-type') === 'agent') {
                    contact.style.display = 'flex';
                } else {
                    contact.style.display = 'none';
                }
            });
        });
    });

    // Search contacts functionality
    const searchInput = document.getElementById('search-contact');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        contacts.forEach(contact => {
            const contactName = contact.querySelector('h3').textContent.toLowerCase();
            
            if (contactName.includes(searchTerm)) {
                contact.style.display = 'flex';
            } else {
                contact.style.display = 'none';
            }
        });
    });

    // Contact selection
    contacts.forEach(contact => {
        contact.addEventListener('click', function() {
            // Remove active class from all contacts
            contacts.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked contact
            this.classList.add('active');
            
            // If contact has unread messages, remove unread status
            if (this.classList.contains('unread')) {
                this.classList.remove('unread');
                const unreadBadge = this.querySelector('.unread-badge');
                if (unreadBadge) {
                    unreadBadge.remove();
                }
            }
            
            // Update chat header with contact info
            const contactName = this.querySelector('h3').textContent;
            const contactAvatar = this.querySelector('img').src;
            const statusIndicator = this.querySelector('.status-indicator');
            let statusText = 'Hors ligne';
            
            if (statusIndicator.classList.contains('online')) {
                statusText = 'En ligne';
            } else if (statusIndicator.classList.contains('away')) {
                statusText = 'Absent(e)';
            }
            
            document.querySelector('.chat-avatar').src = contactAvatar;
            document.querySelector('.chat-contact-info h3').textContent = contactName;
            document.querySelector('.status').textContent = statusText;
            
            // In a real application, we would load the conversation history here
            // For this demo, we'll keep the existing messages
        });
    });

    // Send message functionality
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-message');
    const chatMessages = document.getElementById('chat-messages');
    
    function sendMessage() {
        const messageText = messageInput.value.trim();
        
        if (messageText) {
            // Get current time
            const now = new Date();
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const currentTime = `${hours}:${minutes}`;
            
            // Create message element
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message sent';
            messageDiv.innerHTML = `
                <div class="message-content">
                    <p>${messageText}</p>
                    <span class="message-time">${currentTime}</span>
                    <span class="message-status">
                        <i class="fas fa-check"></i>
                    </span>
                </div>
            `;
            
            // Add message to chat
            chatMessages.appendChild(messageDiv);
            
            // Clear input
            messageInput.value = '';
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Simulate reply after 2 seconds (demo only)
            setTimeout(() => {
                const replyDiv = document.createElement('div');
                replyDiv.className = 'message received';
                replyDiv.innerHTML = `
                    <div class="message-content">
                        <p>Merci pour votre message. Je vous réponds dès que possible.</p>
                        <span class="message-time">${currentTime}</span>
                    </div>
                `;
                
                chatMessages.appendChild(replyDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 2000);
        }
    }
    
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Set the initial scroll position to the bottom of the chat
    chatMessages.scrollTop = chatMessages.scrollHeight;
});


function chargerMessages(discussionId) {
    fetch(`/messages-discussion/${discussionId}/`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('chat-messages');
            container.innerHTML = '';

            data.forEach(msg => {
                const isSent = msg.expediteur__first_name === "{{ user.first_name|escapejs }}";

                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message', isSent ? 'sent' : 'received');

                const contentDiv = document.createElement('div');
                contentDiv.classList.add('message-content');

                const p = document.createElement('p');
                p.textContent = msg.contenu;

                const timeSpan = document.createElement('span');
                timeSpan.classList.add('message-time');
                timeSpan.textContent = new Date(msg.date_envoi).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                contentDiv.appendChild(p);
                contentDiv.appendChild(timeSpan);

                if (isSent) {
                    const statusSpan = document.createElement('span');
                    statusSpan.classList.add('message-status');
                    statusSpan.innerHTML = '<i class="fas fa-check-double"></i>';
                    contentDiv.appendChild(statusSpan);
                }

                messageDiv.appendChild(contentDiv);
                container.appendChild(messageDiv);
            });

            // Scroll vers le bas
            container.scrollTop = container.scrollHeight;
        })
        .catch(error => console.error("Erreur lors du chargement des messages :", error));
}