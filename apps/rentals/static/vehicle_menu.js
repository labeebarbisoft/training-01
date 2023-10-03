document.addEventListener("DOMContentLoaded", function () {
    const cardElements = document.querySelectorAll(".card-clickable");
    
    cardElements.forEach(function (cardElement) {
        cardElement.addEventListener("click", function () {
            const vehicleId = this.getAttribute("data-vehicle-id");
            console.log(vehicleId)
            const radioInput = document.getElementById(vehicleId);
            
            if (radioInput) {
                radioInput.checked = true;
                cardElements.forEach(function (element) {
                    element.classList.remove("selected");
                });
                this.classList.add("selected");
            }
        });
    });
});

