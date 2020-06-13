const readURL = (input, previewId) => {
    if (input.files && input.files[0]) {
        let reader = new FileReader()

        reader.onload = function (e) {
            document.getElementById(`${previewId}`).style.backgroundImage = `url('${e.target.result}')`
            document.getElementById(`${previewId}`).style.border = "none"
        }
        reader.readAsDataURL(input.files[0])
    }
}

// document.getElementById("upload_image").onchange = function(){
//     readURL(this)
//     document.querySelector("#add_category_preview h3").style.color = "#fff"
// }

// document.getElementById("category_title").oninput = function(e) {
//     document.querySelector("#add_category_preview h3").innerHTML = `${e.target.value}`
// }


// Auto Resize Textarea
var observe;
if (window.attachEvent) {
    observe = function (element, event, handler) {
        element.attachEvent('on'+event, handler);
    };
}
else {
    observe = function (element, event, handler) {
        element.addEventListener(event, handler, false);
    };
}

var observe;
if (window.attachEvent) {
    observe = function (element, event, handler) {
        element.attachEvent('on'+event, handler);
    };
}
else {
    observe = function (element, event, handler) {
        element.addEventListener(event, handler, false);
    };
}
function init (textareaId) {
    var text = document.getElementById(textareaId);
    function resize () {
        text.style.height = 'auto';
        text.style.height = text.scrollHeight+'px';
    }
    /* 0-timeout to get the already changed text */
    function delayedResize () {
        window.setTimeout(resize, 0);
    }
    observe(text, 'change',  resize);
    observe(text, 'cut',     delayedResize);
    observe(text, 'paste',   delayedResize);
    observe(text, 'drop',    delayedResize);
    observe(text, 'keydown', delayedResize);

    text.focus();
    text.select();
    resize();
}
