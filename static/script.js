const $readyBtn =$('.ready-btn');
const $loader =$('.loader');


const $matchDisplayArea =$('.match-display-area');
const $matchedPet = $('.matched-pet');
const $nextBtn = $('.nextbtn');

// =========== match_result.html========

const $favBtn = $('.favorite');
const $maybeBtn = $('.maybe');
const $noBtn = $('.no');
const $formUserLikes = $('.form-user-likes');
const $formUserMaybe = $('.form-user-maybe');
const $formUserNo = $('.form-user-no');

$formUserLikes.on('click', 'button', function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    let response =axios({method: 'post', url:'/likes', data:{animal: e.target.dataset.animal}})
    // if the button is clicked, depending on the type of button we clicked, we will send axios request to backend with /likes, /maybe, /no  with POST request.
    //in app.py, write a view function with each route /likes, /maybe, /no. For /likes, /maybe, store add info to DB. for no create a list of no's so next time we don't show those pets.
    console.log(response)
});

$formUserMaybe.on('click', 'button', function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    let response =axios({method: 'post', url:'/maybe', data:{animal: e.target.dataset.animal}})
    // if the button is clicked, depending on the type of button we clicked, we will send axios request to backend with /likes, /maybe, /no  with POST request.
    //in app.py, write a view function with each route /likes, /maybe, /no. For /likes, /maybe, store add info to DB. for no create a list of no's so next time we don't show those pets.
    console.log(response)
})

$formUserNo.on('click', 'button', function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    let response =axios({method: 'post', url:'/no', data:{animal: e.target.dataset.animal}})
    // if the button is clicked, depending on the type of button we clicked, we will send axios request to backend with /likes, /maybe, /no  with POST request.
    //in app.py, write a view function with each route /likes, /maybe, /no. For /likes, /maybe, store add info to DB. for no create a list of no's so next time we don't show those pets.
    console.log(response)
})









// $readyBtn.on('click', function{

// })



// function hidePageCompornent(){
//     $matchDisplayArea.hide()
// }

// function showFirstItem(){
//     $matchedPet.
// }

