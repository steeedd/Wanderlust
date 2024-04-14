
const continentSelect = document.getElementById('continente');
const countrySelect = document.getElementById('nazione');

const countriesByContinent = {
    Africa: ['Algeria', 'Angola', 'Egitto', 'Etiopia', 'Nigeria', 'Sudafrica', 'Tanzania', 'Kenya', 'Marocco', 'Uganda', 'Seychelles'],
    Asia: ['Cina', 'India', 'Indonesia', 'Giappone', 'Giordania', 'Pakistan', 'Bangladesh', 'Filippine', 'Vietnam', 'Iran', 'Turchia', 'Maldive'],
    Europa: ['Francia', 'Germania', 'Italia', 'Spagna', 'Regno Unito', 'Russia', 'Olanda', 'Svezia', 'Polonia', 'Austria'],
    NordAmerica: ['Stati Uniti', 'Canada', 'Messico', 'Cuba', 'Giamaica', 'Costa Rica', 'Panama', 'Haiti', 'El Salvador', 'Honduras'],
    SudAmerica: ['Brasile', 'Argentina', 'Colombia', 'Perù', 'Venezuela', 'Cile', 'Cuba', 'Ecuador', 'Bolivia', 'Paraguay', 'Uruguay'],
    Oceania: ['Australia', 'Nuova Zelanda', 'Fiji', 'Papua Nuova Guinea', 'Isole Salomone', 'Vanuatu', 'Samoa', 'Tonga', 'Kiribati', 'Nauru']
};

continentSelect.addEventListener('change', function() {
    const selectedContinent = this.value;
    countrySelect.innerHTML = '<option value=""></option>';

    if (selectedContinent) {
        countriesByContinent[selectedContinent].forEach(function(country) {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            countrySelect.appendChild(option);
        });
        countrySelect.disabled = false;
    } else {
        countrySelect.disabled = true;
    }
});