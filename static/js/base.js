/*======================================================
                    JS For Modal
========================================================*/

const shareLink = document.getElementById("share")
const modal = document.getElementById("modal")
const closeModalBtn = document.getElementById("close-modal")

shareLink.onclick = (e) => {
    e.preventDefault()
    modal.style.visibility = "visible"
}

const closeModal = (e) => {
    e.preventDefault()
    modal.style.visibility = "hidden"
}

closeModalBtn.onclick = closeModal
modal.onclick = closeModal