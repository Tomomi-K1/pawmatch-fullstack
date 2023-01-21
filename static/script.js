const $readyBtn =$('.ready-btn');
const $loader =$('.loader');


const $matchDisplayArea =$('.match-display-area');
const $matchedPet = $('.matched-pet');
const $nextBtn = $('.nextbtn');

// =========== match_result.html========

const $favBtn = $('.favorite')
const $maybeBtn = $('.maybe')
const $noBtn = $('.no')
const $formUserLikes = $('.form-user-likes')

$formUserLikes.on('click', 'button', function(e){
    e.preventDefault();
    // if the button is clicked, depending on the type of button we clicked, we will send axios request to backend with /likes, /maybe, /no  with POST request.
    //in app.py, write a view function with each route /likes, /maybe, /no. For /likes, /maybe, store add info to DB. for no create a list of no's so next time we don't show those pets.
    console.log(e.target.className);

})









// $readyBtn.on('click', function{

// })



// function hidePageCompornent(){
//     $matchDisplayArea.hide()
// }

// function showFirstItem(){
//     $matchedPet.
// }

