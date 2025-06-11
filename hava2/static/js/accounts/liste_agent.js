// Simulate fetching data
const fetchData = async () => {
    // In a real application, this would be an API call
    // For this example, we use static data
    return {
        agents: [
            { id: 1, name: "Sophie Dupont" },
            { id: 2, name: "Marc Dubois" },
            { id: 3, name: "Léa Martin" },
            { id: 4, name: "David Petit" },
        ],
        clients: [
            { id: 101, agentId: 1, name: "Client A", details: "Recherche appartement centre ville" },
            { id: 102, agentId: 1, name: "Client B", details: "Vente maison banlieue" },
            { id: 103, agentId: 2, name: "Client C", details: "Recherche bureau quartier affaires" },
            { id: 104, agentId: 3, name: "Client D", details: "Vente terrain agricole" },
            { id: 105, agentId: 1, name: "Client E", details: "Investissement locatif" },
            { id: 106, agentId: 4, name: "Client F", details: "Recherche local commercial" },
            { id: 107, agentId: 2, name: "Client G", details: "Vente appartement T3" },
        ]
    };
};

// Store the loaded data
let appData = { agents: [], clients: [] };
let currentAgentId = null;
let nextClientId = 200; // Simple counter for new clients, starting after existing IDs


const displayClients = (agentId, allClients) => {
    const clientListElement = document.getElementById('client-list');
    // Find and keep the 'Add Client' button
    const addButton = clientListElement.querySelector('#add-client-btn');

    // Clear all children except the add button if it exists
    while (clientListElement.firstChild && clientListElement.firstChild !== addButton) {
        clientListElement.removeChild(clientListElement.firstChild);
    }

    const agentClients = allClients.filter(client => client.agentId === agentId);

    if (agentClients.length === 0) {
        const noClientMsg = document.createElement('p');
        noClientMsg.textContent = "Aucun client trouvé pour cet agent.";
        // Insert message before the button if it exists, otherwise append
         if (addButton) {
             clientListElement.insertBefore(noClientMsg, addButton);
         } else {
             clientListElement.appendChild(noClientMsg); // Should not happen after initial load
         }

    } else {
        agentClients.forEach(client => {
            const clientDiv = document.createElement('div');
            clientDiv.classList.add('client-item');

            const clientText = document.createElement('span'); // Use span for text content
            clientText.innerHTML = `<strong>${client.name}:</strong> ${client.details}`;
            clientDiv.appendChild(clientText);

            const removeButton = document.createElement('button');
            removeButton.classList.add('remove-button');
            removeButton.textContent = 'Retirer';
            removeButton.dataset.clientId = client.id; // Store client ID

            removeButton.addEventListener('click', handleRemoveClient); // Add listener

            clientDiv.appendChild(removeButton);
            // Insert client item before the add button
            if (addButton) {
                 clientListElement.insertBefore(clientDiv, addButton);
            } else {
                 clientListElement.appendChild(clientDiv); // Should not happen after initial load
            }
        });
    }

    // Ensure the add button is visible and positioned correctly at the end
    if (addButton) {
         clientListElement.appendChild(addButton);
         addButton.style.display = 'block'; // Make sure it's visible once an agent is selected
    }
};

// Handler for adding a client
const handleAddClient = () => {
    if (currentAgentId === null) {
        alert("Veuillez sélectionner un agent d'abord."); // Or display a message on the page
        return;
    }

    // For simplicity, add a dummy client
    const newClient = {
        id: nextClientId++, // Assign unique ID
        agentId: currentAgentId,
        name: `Nouveau Client ${nextClientId - 200}`, // Simple naming
        details: "Détails ajoutés manuellement",
    };

    appData.clients.push(newClient); // Add to main data array

    // Re-display clients for the current agent
    displayClients(currentAgentId, appData.clients);
};

// Handler for removing a client
const handleRemoveClient = (event) => {
    // Find the client ID from the button's data attribute
    const clientIdToRemove = parseInt(event.target.dataset.clientId, 10);

    // Filter out the client to remove from the main data array
    appData.clients = appData.clients.filter(client => client.id !== clientIdToRemove);

    // Re-display clients for the current agent if one is selected
     if (currentAgentId !== null) {
        displayClients(currentAgentId, appData.clients);
     } else {
        // Fallback: if for some reason no agent is selected, just clear the list
        const clientListElement = document.getElementById('client-list');
        const addButton = clientListElement.querySelector('#add-client-btn');
        clientListElement.innerHTML = '';
         if (addButton) {
             clientListElement.appendChild(addButton);
         }
         const message = document.createElement('p');
         message.textContent = "Aucun agent sélectionné.";
          if (addButton) {
            clientListElement.insertBefore(message, addButton);
         } else {
             clientListElement.appendChild(message);
         }
     }
};

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', async () => {
    // Load data
    appData = await fetchData();

    const clientListElement = document.getElementById('client-list');

    // Add the 'Add Client' button and its listener once on load
    const addButton = document.createElement('button');
    addButton.id = 'add-client-btn';
    addButton.classList.add('add-button');
    addButton.textContent = 'Ajouter un Client';
    addButton.addEventListener('click', handleAddClient);
    clientListElement.appendChild(addButton); // Add the button initially

    // Add initial message to the client list section
    const initialMessage = document.createElement('p');
    initialMessage.textContent = "Cliquez sur un agent pour voir ses clients.";
    clientListElement.insertBefore(initialMessage, addButton); // Insert message before the button


    // Display agents in the agent list
    displayAgents(appData.agents);

    // Initially hide the add button until an agent is selected
    addButton.style.display = 'none'; // Hide the button initially
});