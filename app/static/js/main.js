// Optional enhancements. Registration and login also work without JavaScript.
document.querySelectorAll('[data-toggle-password]').forEach(function (button) {
  button.addEventListener('click', function () {
    const input = document.getElementById(button.dataset.togglePassword);
    const showing = input.type === 'password';
    input.type = showing ? 'text' : 'password';
    button.textContent = showing ? 'Hide' : 'Show';
    button.setAttribute('aria-pressed', String(showing));
    button.setAttribute('aria-label', (showing ? 'Hide' : 'Show') + ' password');
  });
});
document.querySelectorAll('form[data-loading]').forEach(function (form) {
  form.addEventListener('submit', function () {
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    button.dataset.originalLabel = button.innerHTML;
    button.textContent = 'Please wait…';
  });
});
// A restored page should not retain a disabled submit button.
window.addEventListener('pageshow', function () {
  document.querySelectorAll('[data-original-label]').forEach(function (button) {
    button.disabled = false;
    button.innerHTML = button.dataset.originalLabel;
  });
});
