const hamburger = document.querySelector(".hamburger");
const nav = document.querySelector("nav");
const navLinks = document.querySelectorAll("nav a");

hamburger.addEventListener("click", () => {
  nav.classList.toggle("open");
});

// close menu after clicking a link
navLinks.forEach(link => {
  link.addEventListener("click", () => {
    nav.classList.remove("open");
  });
});

let slides = document.querySelectorAll(".slide");
let current = 0;

function showSlide(index){
    slides.forEach(slide => slide.classList.remove("active"));
    slides[index].classList.add("active");
}

function nextSlide(){
    current++;
    if(current >= slides.length) current = 0;
    showSlide(current);
}

function prevSlide(){
    current--;
    if(current < 0) current = slides.length - 1;
    showSlide(current);
}

setInterval(nextSlide, 5000);

