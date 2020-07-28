// Style for making post image responsive by exchanging img with div

const image_divs = document.querySelectorAll('.post-image')

for (let i=0; i<image_divs.length; i++) {
    const img_source = image_divs[i].getAttribute('img_src')
    image_divs[i].style.backgroundImage = `url(${img_source})`
}