let befScrollTop = 0;
let headerOpacity = 1;


const DIVISIONS = [
  { amount: 60, name: "seconds" },
  { amount: 60, name: "minutes" },
  { amount: 24, name: "hours" },
  { amount: 7, name: "days" },
  { amount: 4.34524, name: "weeks" },
  { amount: 12, name: "months" },
  { amount: Number.POSITIVE_INFINITY, name: "years" },
];

const observer = new IntersectionObserver(entries => {
  entries.forEach((entry, index) => {
    entry.target.setAttribute("isIntersecting", entry.isIntersecting);
    progressList[index].classList.toggle("isIntersecting", entry.isIntersecting);
  });
});


const RELATIVE_DATE_FORMATTER = new Intl.RelativeTimeFormat(undefined, { numeric: "auto", });
function formatRelativeDate(toDate, fromDate = new Date()) {
  let duration = (toDate - fromDate) / 1000;

  for (let i = 0; i <= DIVISIONS.length; i++) {
    const division = DIVISIONS[i];
    if (Math.abs(duration) < division.amount) {
      return RELATIVE_DATE_FORMATTER.format(Math.round(duration), division.name);
    }
    duration /= division.amount;
  }
}

const Logo = document.querySelector(".svgLogo");
const weekProgress = document.querySelectorAll(".weekProgress");
const progressList = document.querySelectorAll(".sectionLink");
const dateSection = document.querySelectorAll(".sectionDate");
const Header = document.querySelector('header');
const dropDownMenu = document.querySelector(".progressDropDownMenu");
const images = document.querySelectorAll(".descriptionImage");
const imageContainer = document.querySelector(".imageShow");
dateSection.forEach(weekDate => {
  const initialDate = new Date(weekDate.getAttribute("initialDate"));
  const newDate = formatRelativeDate(initialDate);
  const dateLabel = weekDate.querySelector(".progressDate");
  weekDate.setAttribute("initialDate", initialDate.toLocaleDateString());
  weekDate.setAttribute("newDate", newDate);
  dateLabel.innerText = newDate;
});

weekProgress.forEach((Progress, index) => {
  observer.observe(Progress);
});


dropDownMenu.addEventListener("click", () => {
  let isMenuToggled = dropDownMenu.getAttribute("dropDownToggled");
  let isObjectExpanded = document.body.getAttribute("anObjectExpanded");
  if (isMenuToggled === "false" && isObjectExpanded === "false") {
    dropDownMenu.setAttribute("dropDownToggled", true);
  } else if (isMenuToggled === "true") {
    dropDownMenu.setAttribute("dropDownToggled", false);
  }
});


Logo.addEventListener('click', () => {
  window.location.href = './index.html';
});

const videoTest = document.querySelectorAll(".testComponentsVideo");


videoTest.forEach(video => {
  video.addEventListener("click", () => {

    if (video.getAttribute("isPlaying") === "false") {
      video.play();
      video.setAttribute("isPlaying", true);
    }
    else if (video.getAttribute("isPlaying") === "true") {
      video.pause();
      video.setAttribute("isPlaying", "false");
    }
  });
});


images.forEach(image => {
  image.addEventListener("click", ()=>{
    const isImageExpanded = image.getAttribute("isToggled");
    if (isImageExpanded === "false"){
        image.setAttribute("isToggled", true);
        imageContainer.classList.toggle("ObjectExpanded");
        document.body.setAttribute("anObjectExpanded", true);
    }
    else if (isImageExpanded === "true")
    {
      imageContainer.classList.remove("ObjectExpanded");

      image.setAttribute("isToggled", false);
      document.body.setAttribute("anObjectExpanded", false);
    }
  });
});

//const Images = document.querySelectorAll(".image");
//let isMain = Images.getAttribute("isMain");
//let descImage = document.querySelector(".descriptionImage");

/* 
window.onscroll = ('onscroll', () => {

  let curScrollTop = window.scrollY || document.documentElement.scrollTop;
  // on header hover 
  if (curScrollTop <= 100) {
    Header.setAttribute("isInteracting", true);
  }
  else {
    if (curScrollTop <= 100) {
      Header.setAttribute("isInteracting", false);
    }
  }
  if (befScrollTop < curScrollTop) {
    headerOpacity = 0.5;
  }
  else {
    headerOpacity = 1;
  }

  befScrollTop = curScrollTop;
  Header.style.opacity = headerOpacity;


  Header.addEventListener("mouseover", () => {
    Header.style.opacity = (headerOpacity + 0.5);

  });
  Header.addEventListener("mouseleave", () => {
      Header.style.opacity = headerOpacity;
  });
});
 */


/*
  window.addEventListener('onLoad', ()=>{
    progressDate.forEach(date => {
        let itemDate = date.getAttribute()
        RELATIVE_DATE_FORMATTER((int(date) - currentDate))
      });
  }) */
/* function newImage(items){
    items.
} */

/*  */
