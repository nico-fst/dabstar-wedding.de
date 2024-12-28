// Blurr Background image
window.addEventListener("scroll", function () {
  const image = document.getElementById("paar-back");
  const storyElement = document.getElementById("story");

  const scrollDistance = window.scrollY; // Wie weit wurde gescrollt?
  const viewportHeight = window.innerHeight; // Höhe des Viewports (Sichtbereich)

  // Berechne die Position des Elements #story im Dokument
  const storyPosition =
    storyElement.getBoundingClientRect().top + scrollDistance;

  // Berechne die Mitte des Viewports
  const middleOfViewport = viewportHeight / 2;

  // Definiere die Schwelle für den Blur-Effekt (Mittig im Viewport)
  const scrollThreshold = storyPosition - middleOfViewport;

  // Berechnung des Blur-Effekts
  let blurAmount = 0;
  if (scrollDistance > scrollThreshold) {
    // Der Blur-Effekt wird hier schneller und stärker angewendet
    blurAmount = (scrollDistance - scrollThreshold) / 10; // Schnellere Zunahme des Blur-Effekts
    blurAmount = Math.min(blurAmount, 1000); // Erhöhe den maximalen Blur-Effekt auf einen höheren Wert
  }

  // Sanfter Übergang: Setze den Blur-Wert, aber mit Übergang
  image.style.transition = "filter 0.1s ease-out"; // Schnellere Übergänge für einen dynamischeren Effekt
  image.style.filter = `blur(${blurAmount}px)`; // Anwenden des Blur-Effekts
});


// Curtain Animation,
document.querySelector('.curtain-left').addEventListener('animationend', function () {
  document.querySelector('.curtain').style.display = 'none';
})

// Curtain Overlay davor ausblenden - ginge auch mit animation-delay
setTimeout(function() {
    document.querySelector('.curtain-overlay').classList.add('hide');
}, 1000); // 3000ms (3 Sekunden) nach Beginn der Animation


// Eror Popup ausblenden
setTimeout(function () {
  const popup = document.getElementById('error-container');
  if (popup) {
    popup.style.opacity = '0';
    setTimeout(() => {
      popup.style.display = 'none';
    }, 500);
  }
}, 5000);
