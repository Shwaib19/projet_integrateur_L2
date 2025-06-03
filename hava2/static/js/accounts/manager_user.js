
export function initUsersManagement() {
    // Get DOM elements
    const selectAllCheckbox = document.getElementById('select-all');
    const userCheckboxes = document.querySelectorAll('.users-table tbody input[type="checkbox"]');
    const addUserBtn = document.querySelector('.add-user-btn');
    const modal = document.getElementById('userModal');
    const modalOverlay = document.getElementById('modalOverlay');
    const closeModalBtn = document.querySelector('.close-modal');
    const closeModalFooterBtn = document.querySelector('.close-modal-btn');
    const saveUserBtn = document.querySelector('.save-user-btn');
    const userForm = document.getElementById('userForm');
    const filterStatus = document.getElementById('filter-status');
    const filterRole = document.getElementById('filter-role');
    const searchInput = document.getElementById('search-users');
    const sortButtons = document.querySelectorAll('.users-table th i.fa-sort');
    const actionButtons = document.querySelectorAll('.action-btn');
    const paginationButtons = document.querySelectorAll('.pagination-btn');
    
    // Handle select all checkbox
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', () => {
            userCheckboxes.forEach(checkbox => {
                checkbox.checked = selectAllCheckbox.checked;
            });
        });
    }
};
