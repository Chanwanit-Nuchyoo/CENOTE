let galleryImages=document.querySelectorAll(".gallery-img");
let getLastestOpenedImg;
let windowWidth = window.innerWidth;
const fruits=[];
if(galleryImages){

    galleryImages.forEach(function(image, index){
        let getElementCssZ=window.getComputedStyle(image);
        let getFullImgUrlZ=getElementCssZ.getPropertyValue("background-image");
        let getImgUrlPosZ = getFullImgUrlZ.split("8000/");
        
        let SetNewImgUrlZ = getImgUrlPosZ[1].replace('")','');
        fruits.push(SetNewImgUrlZ);
        
        image.onclick=function() {
            let getElementCss=window.getComputedStyle(image);
            let getFullImgUrl=getElementCss.getPropertyValue("background-image");
            let getImgUrlPos = getFullImgUrl.split("8000/");
            
            let SetNewImgUrl = getImgUrlPos[1].replace('")','');
                
            getLastestOpenedImg = index+1;

            let container = document.body;
            let newImgWindow = document.createElement("div");
            container.appendChild(newImgWindow);
            newImgWindow.setAttribute("class", "img-window");
            newImgWindow.setAttribute("onclick", "closeImg()");
            
            let newImg = document.createElement("img");
            newImgWindow.appendChild(newImg);
            newImg.setAttribute("src", "../"+SetNewImgUrl);
            newImg.setAttribute("id", "current-img");

            newImg.onload = function() {
                let imgWidth = this.width;
                let calcImgToEdge = ((windowWidth - imgWidth)/2)-100;

                let newNextBtn = document.createElement("a");
                
                let btnNextText = document.createTextNode("next");
                newNextBtn.appendChild(btnNextText);
                container.appendChild(newNextBtn);
                newNextBtn.setAttribute("class","img-btn-next");
                newNextBtn.setAttribute("onclick","changeImg(1)");
                newNextBtn.style.cssText="right: " + calcImgToEdge + "px;";

                let newPrevBtn = document.createElement("a");
                let btnPrevText = document.createTextNode("prev");
                newPrevBtn.appendChild(btnPrevText);
                container.appendChild(newPrevBtn);
                newPrevBtn.setAttribute("class","img-btn-prev");
                newPrevBtn.setAttribute("onclick","changeImg(0)");
                newPrevBtn.style.cssText="left: " + calcImgToEdge + "px;";
            }
            

        }
    });
}

function closeImg(){
    document.querySelector(".img-window").remove();
    document.querySelector(".img-btn-next").remove();
    document.querySelector(".img-btn-prev").remove();

}

function changeImg(changeDir){
    // alert(fruits[0]);
    document.querySelector("#current-img").remove();
    let getImgWindow = document.querySelector(".img-window");
    let newImg = document.createElement("img");
    getImgWindow.appendChild(newImg);
    
    let calcNewImg;
    if(changeDir === 1){
        calcNewImg = getLastestOpenedImg +1;
        if(calcNewImg > galleryImages.length) { 
            calcNewImg = 1;
        }
    }
    else if(changeDir ===0){
        calcNewImg = getLastestOpenedImg - 1;
        if(calcNewImg<1){
            calcNewImg = galleryImages.length;
        }
    }

    
    newImg.setAttribute("src","../" + fruits[calcNewImg-1]);
    newImg.setAttribute("id", "current-img");
    getLastestOpenedImg = calcNewImg;
    
    newImg.onload = function(){
        let imgWidth = this.width;
        let calcImgtoEdge = ((windowWidth-imgWidth)/2)-100;
        let nextBtn = document.querySelector(".img-btn-next");
        nextBtn.style.cssText="right: "+calcImgtoEdge + "px;";

        let prevBtn = document.querySelector(".img-btn-prev");
        prevBtn.style.cssText="left: "+calcImgtoEdge + "px;";
        
    }
}