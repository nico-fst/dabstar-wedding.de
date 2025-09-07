// Click auf Hamburger öffnet Navbar
const hamburger = document.getElementById("hamburger");
const header = document.querySelector(".header");
hamburger.addEventListener("click", () => {
  let opened = header.classList.contains("active");
  if (opened) {
    header.style.transform = "translateY(-90%)";
  } else {
    header.style.transform = "translateY(0)";
  }
  header.classList.toggle("active");
});

const mediaQuery = window.matchMedia("(max-width: 880px)");

// Click auf Link in Header schließt wieder
function handleClosingNav() {
  if (mediaQuery.matched) {
    // nur bei mobile genutzt (s. unten)
    const links = document.querySelectorAll(".header a");

    links.forEach((link) => {
      link.addEventListener("click", () => {
        // header.classList.remove('active');
        header.style.transform = "translateY(-90%)";
      });
    });
  }
}

// Navbar bei Scrollen ausblenden
let lastScrollTop = 0;
function handleScroll() {
  // nur bei Mobile genutzt (s. unten)
  let currentScroll = window.scrollY || document.documentElement.scrollTop;

  if (currentScroll > lastScrollTop) {
    // scroll down
    header.classList.remove("active");
    header.style.transform = "translateY(-110%)";
  } else {
    // scroll up
    header.style.transform = "translateY(-90%)";
  }
  lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
}

// Scroll Effekt und Header ausblenden nur bei Mobile
function checkMediaQuery() {
  if (mediaQuery.matches) {
    window.addEventListener("scroll", handleScroll);
    handleClosingNavClosingNav();
  } else {
    window.removeEventListener("scroll", handleScroll);
    header.style.transform = "translateY(0)"; // Navbar zurücksetzen, wenn die Größe > 880px ist
  }
}

// Initiale Prüfung und auch bei Fenstergrößenänderungen überwachen
checkMediaQuery();
mediaQuery.addEventListener("change", checkMediaQuery);
