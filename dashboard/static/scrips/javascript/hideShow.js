let geoVisible = true;

function toggleCharts() {
    var worldMapRadio = document.getElementById('worldMapRadio');
    var lineMapRadio = document.getElementById('lineMapRadio');
    var geoPlotContainer = document.getElementById('geo-plot-container');
    var linePlotContainer = document.getElementById('line-plot-container');

    if (worldMapRadio.checked) {
        geoPlotContainer.style.display = 'block';
        linePlotContainer.style.display = 'none';
    } else if (lineMapRadio.checked) {
        geoPlotContainer.style.display = 'none';
        linePlotContainer.style.display = 'block';
    }
}