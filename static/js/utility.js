// Setting the backgrounds of the various sections
const categories = document.getElementsByClassName('category')
for (let Ndx=0; Ndx<categories.length; Ndx++) {
    let imageUrl = categories[Ndx].getAttribute("img_src")
    categories[Ndx].style.backgroundImage = `url(${imageUrl})`
}