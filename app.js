AOS.init({
  // Global settings:
  disable: false, // accepts following values: 'phone', 'tablet', 'mobile', boolean, expression or function
  startEvent: "DOMContentLoaded", // name of the event dispatched on the document, that AOS should initialize on
  initClassName: "aos-init", // class applied after initialization
  animatedClassName: "aos-animate", // class applied on animation
  useClassNames: false, // if true, will add content of `data-aos` as classes on scroll
  disableMutationObserver: false, // disables automatic mutations' detections (advanced)
  debounceDelay: 50, // the delay on debounce used while resizing window (advanced)
  throttleDelay: 99, // the delay on throttle used while scrolling the page (advanced)

  // Settings that can be overridden on per-element basis, by `data-aos-*` attributes:
  offset: 120, // offset (in px) from the original trigger point
  delay: 0, // values from 0 to 3000, with step 50ms
  duration: 600, // values from 0 to 3000, with step 50ms
  easing: "ease-in", // default easing for AOS animations
  once: false, // whether animation should happen only once - while scrolling down
  mirror: false, // whether elements should animate out while scrolling past them
  anchorPlacement: "top-bottom", // defines which position of the element regarding to window should trigger the animation
});

// This function is toggling the Nav in mobile type devices
const nav = () => {
  const bars = document.querySelector(".bars");
  const listItems = document.querySelector(".nav_links");
  bars.addEventListener("click", () => {
    listItems.classList.toggle("nav-active");
    bars.classList.toggle("toogle");
  });
};

nav();

// this function will take the use to the top of the page
const topButton = document.querySelector(".top");
topButton.addEventListener("click", () => {
  window.scrollTo(0, 0);
});

// for the leader
window.addEventListener("load", () => {
  const loader = document.querySelector(".loader");
  setTimeout(() => {
    loader.style.transform = "translateX(100%)";
  });
});

// slider
var swiper = new Swiper(".swiper-container", {
  effect: "cube",
  grabCursor: true,
  loop: true,
  autoplay: true,
  cubeEffect: {
    shadow: true,
    slideShadows: true,
    shadowOffset: 20,
    shadowScale: 0.94,
  },
  pagination: {
    el: ".swiper-pagination",
  },
});

const currentYear = new Date().getFullYear();
document.querySelector("#year").textContent = currentYear;
