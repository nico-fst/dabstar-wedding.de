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
    blurAmount = Math.min(blurAmount, 75); // Erhöhe den maximalen Blur-Effekt auf einen höheren Wert
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

// Click auf Hamburger öffnet Navbar
const hamburger = document.getElementById('hamburger');
const header = document.querySelector('.header');
hamburger.addEventListener('click', () => {
  let opened = header.classList.contains("active");
  if (opened) {
    header.style.transform = "translateY(-90%)";
  } else {
    header.style.transform = "translateY(0)";
  }
  header.classList.toggle("active");
});

// Click auf Link in Header schließt wieder
const links = document.querySelectorAll('.header a');
links.forEach(link => {
  link.addEventListener('click', () => {
    // header.classList.remove('active');
    header.style.transform = "translateY(-90%)";
  })
});

// Navbar bei Scrollen ausblenden

let lastScrollTop = 0;
const mediaQuery = window.matchMedia("(max-width: 880px)");

function handleScroll() {
  let currentScroll = window.scrollY || document.documentElement.scrollTop;

  if (currentScroll > lastScrollTop) {
    // scroll down
    header.style.transform = "translateY(-110%)";
  } else {
    // scroll up
    header.style.transform = "translateY(-90%)";
  }
  lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
}

// Führe den Scroll-Effekt nur aus, wenn die Bildschirmgröße <= 880px ist
function checkMediaQuery() {
  if (mediaQuery.matches) {
    window.addEventListener("scroll", handleScroll);
  } else {
    window.removeEventListener("scroll", handleScroll);
    header.style.transform = "translateY(0)"; // Navbar zurücksetzen, wenn die Größe > 880px ist
  }
}

// Initiale Prüfung und auch bei Fenstergrößenänderungen überwachen
mediaQuery.addEventListener("change", checkMediaQuery);
checkMediaQuery();