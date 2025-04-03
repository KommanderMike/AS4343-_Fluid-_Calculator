document.addEventListener('DOMContentLoaded', () => {
    const pipeSizeInput = document.getElementById('pipeSize');
    const fluidGroupInput = document.getElementById('fluidGroup');
    const pressureInput = document.getElementById('pressure');
    const temperatureInput = document.getElementById('temperature');
    const locationFactorInput = document.getElementById('locationFactor');
    const leakageFactorInput = document.getElementById('leakageFactor');
    const calculateButton = document.getElementById('calculate');
    const hazardRatingDisplay = document.getElementById('hazardRating');
    const resultDiv = document.querySelector('.result');

    function convertHazardRating(rating) {
        const ranges = {
            A: Math.pow(10, 8.5),
            B: Math.pow(10, 4),
            C: Math.pow(10, 3),
            D: Math.pow(10, 2.5),
        };

        if (rating < ranges.D) return 'E';
        if (rating >= ranges.D && rating < ranges.C) return 'D';
        if (rating >= ranges.C && rating < ranges.B) return 'C';
        if (rating >= ranges.B && rating < ranges.A) return 'B';
        return 'A'; // rating >= ranges.A
    }

    calculateButton.addEventListener('click', () => {
        const pipeSize = parseFloat(pipeSizeInput.value);
        const fluidGroup = parseFloat(fluidGroupInput.value);
        const pressureBar = parseFloat(pressureInput.value);
        const temperature = parseFloat(temperatureInput.value);
        const locationFactor = parseFloat(locationFactorInput.value);
        const leakageFactor = parseFloat(leakageFactorInput.value);

        if (isNaN(pipeSize) || isNaN(fluidGroup) || isNaN(pressureBar) || isNaN(temperature) || isNaN(locationFactor) || isNaN(leakageFactor)) {
            alert('Please enter valid numerical values.');
            return;
        }

        const pressureMPa = pressureBar * 0.1; // Convert Bar to MPa
        const hazardIndex = fluidGroup * pressureMPa;
        const hazardRating = hazardIndex * pipeSize * locationFactor * leakageFactor * (temperature / 100);

        hazardRatingDisplay.textContent = convertHazardRating(hazardRating);
        resultDiv.style.display = 'block'; // Show the result div
    });
});