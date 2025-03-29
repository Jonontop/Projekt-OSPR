document.addEventListener('DOMContentLoaded', function() {
  const dropdownTriggers = document.querySelectorAll('.dropdown-trigger');
  let activeDropdown = null;

  // Dropdown click handling
  dropdownTriggers.forEach(trigger => {
      trigger.addEventListener('click', function(e) {
          e.preventDefault();
          e.stopPropagation();

          const dropdown = document.getElementById(this.dataset.dropdown);

          if (activeDropdown && activeDropdown !== dropdown) {
              activeDropdown.classList.remove('dropdown-active');
          }

          dropdown.classList.toggle('dropdown-active');

          activeDropdown = dropdown.classList.contains('dropdown-active') ? dropdown : null;
      });

      // Dropdown hover handling
      trigger.addEventListener('mouseenter', function() {
          const dropdown = document.getElementById(this.dataset.dropdown);
          dropdown.classList.add('dropdown-active');
      });

      trigger.parentElement.addEventListener('mouseleave', function() {
          const dropdown = document.getElementById(trigger.dataset.dropdown);
          dropdown.classList.remove('dropdown-active');
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
