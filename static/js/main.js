const elButton = document.querySelector('.fas-item .button');
const liElement =document.querySelector('.fas-item .wrapper');

const purLiElement=document.querySelector('.purchase-item-fas');
elButton.addEventListener('click',(evt)=>{
    console.log(liElement);
    purLiElement.innerHTML+=`${liElement}`;
});
