document.addEventListener('DOMContentLoaded', function() {
    // Set up dropdown triggers
    const dropdownTriggers = document.querySelectorAll('.dropdown-trigger');
    let activeDropdown = null;

    // Handle dropdown clicks
    dropdownTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            const targetId = this.getAttribute('data-dropdown');
            const dropdown = document.getElementById(targetId);

            // Close any open dropdown first
            if (activeDropdown && activeDropdown !== dropdown) {
                activeDropdown.classList.remove('dropdown-active');
            }

            // Toggle current dropdown
            dropdown.classList.toggle('dropdown-active');

            // Update active dropdown reference
            if (dropdown.classList.contains('dropdown-active')) {
                activeDropdown = dropdown;
            } else {
                activeDropdown = null;
            }
        });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (activeDropdown && !e.target.closest('.nav-item')) {
            activeDropdown.classList.remove('dropdown-active');
            activeDropdown = null;
        }
    });

    // Mobile menu toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');

    mobileToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
    });
});