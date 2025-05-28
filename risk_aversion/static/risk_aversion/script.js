const selectInput = document.querySelector('select[name=inv1]');
const max_investment = parseFloat("{{C.MAX_INVESTMENT }}");
const kept = document.getElementById('kept');
const gains_if_yellow = document.getElementById('gains_if_yellow');
const gains_if_purple = document.getElementById('gains_if_purple');
  

function updateMessage() {
    const selected = selectInput.value;
    kept_value = max_investment - selected;
    kept.textContent = kept_value;
    gains_if_yellow.textContent = kept_value + " jetons gardés + 3 x " + selected + " jetons gagnés = " + (kept_value+3*selected)
    gains_if_purple.textContent = kept_value + " jetons gardés"
}

selectInput.addEventListener('change', updateMessage);
document.addEventListener('DOMContentLoaded', updateMessage);
