/**
 * Admin Custom JavaScript
 * Bootstrap 5 Based Admin Interface
 */

document.addEventListener('DOMContentLoaded', function () {
    // ============================================
    // 1. SIDEBAR TOGGLE (mobile)
    // ============================================
    const sidebarToggle = document.querySelector('.navbar-toggler');
    const sidebar = document.querySelector('.admin-sidebar');

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function () {
            if (sidebar) {
                sidebar.classList.toggle('show');
            }
        });
    }

    // Close sidebar when a link is clicked
    const sidebarLinks = document.querySelectorAll('.admin-sidebar-nav a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function () {
            if (sidebar && window.innerWidth < 768) {
                sidebar.classList.remove('show');
            }
        });
    });

    // ============================================
    // 2. TABLE CHECKBOX SELECTION
    // ============================================
    const checkAllCheckbox = document.getElementById('id_check_all');
    if (checkAllCheckbox) {
        checkAllCheckbox.addEventListener('change', function (e) {
            const checkboxes = document.querySelectorAll('.admin-checkbox');
            checkboxes.forEach(checkbox => checkbox.checked = e.target.checked);
        });

        // Update "check all" status based on individual checkboxes
        const adminCheckboxes = document.querySelectorAll('.admin-checkbox');
        adminCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function () {
                const allChecked = Array.from(adminCheckboxes).every(cb => cb.checked);
                const someChecked = Array.from(adminCheckboxes).some(cb => cb.checked);
                checkAllCheckbox.checked = allChecked;
                checkAllCheckbox.indeterminate = someChecked && !allChecked;
            });
        });
    }

    // ============================================
    // 3. THEME TOGGLE INTEGRATION
    // ============================================
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            // Check if theme.js is available
            if (typeof toggleTheme === 'function') {
                toggleTheme();
                updateThemeIcon();
            }
        });
        updateThemeIcon();
    }

    function updateThemeIcon() {
        const isDarkTheme = document.body.classList.contains('dark-theme');
        const icon = themeToggle.querySelector('i');
        if (icon) {
            icon.className = isDarkTheme ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    // ============================================
    // 4. FORM VALIDATION
    // ============================================
    const forms = document.querySelectorAll('.admin-form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // ============================================
    // 5. BULK ACTION CONFIRMATION
    // ============================================
    const changelist_form = document.getElementById('changelist-form');
    if (changelist_form) {
        changelist_form.addEventListener('submit', function (e) {
            const action = document.querySelector('[name="action"]');
            const checkedBoxes = document.querySelectorAll('.admin-checkbox:checked');

            if (action && action.value && action.value === 'delete_selected') {
                if (!confirm('确定要删除选中的项目吗？')) {
                    e.preventDefault();
                    return false;
                }
            }
        });
    }

    // ============================================
    // 6. SEARCH BOX AUTO-FOCUS
    // ============================================
    const searchbar = document.getElementById('searchbar');
    if (searchbar) {
        const searchInput = searchbar.querySelector('input[name="q"]');
        if (searchInput && searchInput.value === '') {
            // Auto-focus search when page loads if empty
            setTimeout(() => searchInput.focus(), 100);
        }
    }

    // ============================================
    // 7. RESPONSIVE ADJUSTMENTS
    // ============================================
    function handleResize() {
        if (window.innerWidth > 768 && sidebar) {
            sidebar.classList.remove('show');
        }
    }

    window.addEventListener('resize', debounce(handleResize, 250));

    // ============================================
    // 8. UTILITY FUNCTIONS
    // ============================================
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // ============================================
    // 9. KEYBOARD SHORTCUTS
    // ============================================
    document.addEventListener('keydown', function (e) {
        // Ctrl/Cmd + S to save form
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const saveButton = document.querySelector('.admin-form button[name="_save"]');
            if (saveButton) {
                saveButton.click();
            }
        }

        // Escape to close modals or go back
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const bsModal = new bootstrap.Modal(modal);
                bsModal.hide();
            });
        }
    });

    // ============================================
    // 10. INITIALIZE BOOTSTRAP COMPONENTS
    // ============================================
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    console.log('Admin interface loaded successfully');
});
