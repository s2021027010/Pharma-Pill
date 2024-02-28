//swipper js
var swiper = new Swiper(".team-slider",{
    loop: true,
    grabCursor: true,
    spaceBetween: 20,
    breakpoints:{
      0: {
      slidesPerView:1,  
      },
      768: {
      slidesPerView:2,  
      }, 
      991: {
      slidesPerView:3,  
      },
    }
  });

  