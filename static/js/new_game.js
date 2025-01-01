document.getElementById('toggle-advanced').addEventListener('click', function () {
    const advancedOptions = document.getElementById('advanced-options');
    const icon = this.querySelector('i');

    if (advancedOptions.classList.contains('hidden')) {
        advancedOptions.classList.remove('hidden');
        this.classList.add('expanded');
    } else {
        advancedOptions.classList.add('hidden');
        this.classList.remove('expanded');
    }
});


function updateEndConditionInput() {
    const select = document.getElementById("end_condition_select");
    const customInput = document.getElementById("end_condition_custom");
    
    if (select.value === "Custom") {
        customInput.style.display = "block";
        customInput.required = true;
    } else {
        customInput.style.display = "none";
        customInput.required = false;
    }
}

