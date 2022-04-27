const speedBar = document.querySelector("#speedBar");
const video = document.querySelector("#videoStream");
const expandMenu = document.querySelector("#expandMenu");
const sideBar = document.querySelector(".asideControllersMain"); 

// side menu buttons
function menuExpanded(isExpanded) {
    expandMenu.setAttribute("isExpanded", isExpanded);
    sideBar.setAttribute("aria-expanded", isExpanded);
}

expandMenu.addEventListener("click", ()=> {
    let isExpanded = expandMenu.getAttribute("isExpanded");
    if(isExpanded === "false"){
        menuExpanded(isExpanded = true);
    }
    else if (isExpanded === "true"){
        menuExpanded(isExpanded = false);
    }     
});

speedBar.addEventListener("click", ()=>{
    speedBar.setAttribute("value", speedBar.value);
});



// Video

async function videoStream(){
const stream = await navigator.mediaDevices.getUserMedia({video : true})
video.srcObject = stream;
}

videoStream();