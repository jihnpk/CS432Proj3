## CS 432 Project 3 Github Page

{% include CovidData.html %}
This is an interactive visualization that allows you to select an area to change the area of focus and select/de-select different data points in the legend. You can also hover over the line to check for values at each time.

{% include sentimentOverTime.html %}
This is an interactive visualization that allows you to select an area to change the area of focus. You can also hover over the line to check for values at each time.

<button onclick="func()">Hide/Show Geospat</button>
### WARNING SLOW VISUALIZATION

<div id="geoSpat">
  {% include sentimentScatterGeo.html %}
</div>
This is an interactive visualization that allows you to zoom in and out and hover over data points to find actual sentiment values and coordinates. Blue indicates positive sentiment, red negative, and white/grey indicates neutral.

<script>
function func() {
  var x = document.getElementById("geoSpat");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
</script>
