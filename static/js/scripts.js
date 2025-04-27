document.addEventListener("DOMContentLoaded", function () {
    flatpickr("#fecha", {
        dateFormat: "d/m/Y",
        allowInput: true,
        placeholder: "Selecciona una fecha"
    });
});