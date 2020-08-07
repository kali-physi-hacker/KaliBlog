// Script for applying a parsed image src to a div as a background to the div

const images = document.querySelectorAll('.carousel-bg-image');

for (let i=0; i<images.length; i++) {
    const image_source = images[i].getAttribute("img_src");
    images[i].style.backgroundImage = `url(${image_source})`
}