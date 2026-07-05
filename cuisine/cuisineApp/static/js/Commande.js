document.addEventListener('DOMContentLoaded', function() {
    const cuisineDropdown = document.getElementById('id_Cuisine');
    const prixCommandeField = document.getElementById('id_Prix_commande');
    const prixTransportField = document.getElementById('id_Prix_Transport');
    const cuisineSearch = document.getElementById('cuisineSearch');

    function updatePrixCommande() {
        const selectedOption = cuisineDropdown.options[cuisineDropdown.selectedIndex];
        const cuisinesData = JSON.parse(cuisineDropdown.getAttribute('data-cuisines'));
        const selectedCuisineData = cuisinesData.find(c => c.pk == selectedOption.value);

        if (selectedCuisineData) {
            const prixVente = parseFloat(selectedCuisineData.Prix_vente);
            const prixTransport = parseFloat(prixTransportField.value);
            if (!isNaN(prixVente) && !isNaN(prixTransport)) {
                const prixCommande = prixVente + prixTransport;
                prixCommandeField.value = prixCommande.toFixed(2);
                return;
            }
        }
        prixCommandeField.value = '';
    }
    cuisineDropdown.addEventListener('change', function() {
        updatePrixCommande();
    });
    prixTransportField.addEventListener('input', function() {
        updatePrixCommande();
    });
    
    cuisineSearch.addEventListener('input', function() {
        const searchTerm = cuisineSearch.value.toLowerCase();
        const options = cuisineDropdown.options;
        for (let i = 0; i < options.length; i++) {
            const optionText = options[i].textContent.toLowerCase();
            const isVisible = optionText.includes(searchTerm);
            options[i].style.display = isVisible ? '' : 'none';
        }
    });
});