
const creditCardIcon = document.getElementById('creditCardIcon');
const paypalIcon = document.getElementById('paypalIcon');
const satispayIcon = document.getElementById('satispayIcon');

const collapseCreditCard = document.getElementById('collapseCreditCard');
const collapsePaypal = document.getElementById('collapsePaypal');
const collapseSatispay = document.getElementById('collapseSatispay');

const icons = [creditCardIcon, paypalIcon, satispayIcon];
const collapses = [collapseCreditCard, collapsePaypal, collapseSatispay];

icons.forEach(iconCollapse => {
    iconCollapse.addEventListener('click', () => {
    collapses.forEach(collapse => {
        collapse.classList.remove('show'); // Remove show class from all collapses before opening the new one
    });
    iconCollapse.dataset.bsTarget.classList.add('show'); // Add show class only to the clicked icon's target collapse
    });
});
        

const cardNumberInput = document.getElementById('cardNumber');

cardNumberInput.addEventListener('input', function() {
    const cardNumber = this.value.replace(/\D/g, '');
    const cardValid = /^\d{16}$/.test(cardNumber);

    if (!cardValid) {
        this.setCustomValidity('Il numero della carta di credito deve contenere esattamente 16 cifre.');
    } else {
        this.setCustomValidity('');
    }
});


const cvvInput = document.getElementById('CVV');

cvvInput.addEventListener('input', function() {
    const cvv = this.value.replace(/\D/g, '');
    const cvvValid = /^\d{3}$/.test(cvv);

    if (!cvvValid) {
        this.setCustomValidity('Il CVV della carta di credito deve contenere esattamente 3 cifre.');
    } else {
        this.setCustomValidity('');
    }
});
