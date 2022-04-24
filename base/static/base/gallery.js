let galleryImages=document.querySelectorAll(".gallery-img");
let getLastestOpenedImg;
let windowWidth = window.innerWidth;

if(galleryImages){
    galleryImages.forEach(function(image, index){
        image.onclick=function() {
            let getElementCss=window.getComputedStyle(image);
            let getFullImgUrl=getElementCss.getPropertyValue("background-image");
            let getImgUrlPos = getFullImgUrl.split("8000/");
            
            let SetNewImgUrl = getImgUrlPos[1].replace('")','');
            alert(SetNewImgUrl);
            getLastestOpenedImg = index+1;

            let container = document.body;
            let newImgWindow = document.createElement("div");
            container.appendChild(newImgWindow);
            newImgWindow.setAttribute("class", "img-window");
            newImgWindow.setAttribute("onclick", "closeImg()");
            
            let newImg = document.createElement("img");
            newImgWindow.appendChild(newImg);
            newImg.setAttribute("src", "../"+SetNewImgUrl);
        }
    });
}

function closeImg(){
    document.querySelector(".img-window");

}