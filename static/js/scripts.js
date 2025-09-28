// static/js/scripts.js
// Custom JavaScript for your Django site

document.addEventListener("DOMContentLoaded", function () {
  // -----------------------------
  // Bootstrap Tooltips
  // -----------------------------
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // -----------------------------
  // Bootstrap Popovers
  // -----------------------------
  const popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  popoverTriggerList.forEach(function (popoverTriggerEl) {
    new bootstrap.Popover(popoverTriggerEl);
  });

  // -----------------------------
  // Client-side Form Validation
  // -----------------------------
  const forms = document.querySelectorAll(".needs-validation");

  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add("was-validated");
      },
      false
    );
  });

  // -----------------------------
  // Example: Auto-dismiss alerts
  // -----------------------------
  const alerts = document.querySelectorAll(".alert-dismissible");
  alerts.forEach(function (alert) {
    setTimeout(() => {
      bootstrap.Alert.getOrCreateInstance(alert).close();
    }, 5000); // close after 5 seconds
  });
});

document.querySelector('input[name="csrfmiddlewaretoken"]').value
