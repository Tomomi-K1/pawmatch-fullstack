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
const $showMyPetBtn = $('.show-my-pets')


// =========== users_pets.html==============
const $deleteFav = $('.users-pets_delete-form');
const $deleteMaybe = $('.delete-maybe-form');
const $petComment = $('.pet-comment');

// =========questions.html===================
const $searchStartBtn = $('.search-start');

// =======org_search.html ==================
const $orgSearch = $('.org-search');

// ==========org_results.html==============
const $orgComment = $('.org-comment');

$deleteFav.on('click', 'button', async function(e){
    e.preventDefault();
    try{
        let response =await axios({method: 'delete', url:'/delete-fav', data:{animal: e.currentTarget.dataset.animal}})
    } catch(e){
        console.log(e);
    }
    $('.data-'+ e.currentTarget.dataset.animal).parent().remove() 
})


// adding a comment on Favpet and maybe pet
$petComment.on('click', 'button', function(e){
    e.preventDefault();
    let pet_id=e.target.dataset.animal
    let comment = $(`.data-${pet_id}`).find('.pet-textarea').val()
        
    // call to backend to add a comment to database
    let response =axios({method: 'post', url:`/comments/${pet_id}`, data:{animal: pet_id, comment:comment}})

    // take comment and update the HTML page
    let commentSection = $(`.pet-comment-${pet_id} h3`);
    let newElem = $('<p>').text(comment);
    commentSection.after(newElem);
    
    // clear entries
    $(`.data-${pet_id}`).find('.pet-textarea').val('')   
    

    console.log(comment)
    console.log(response)
})

$searchStartBtn.on("click", function(e){
    console.debug(`loader working?`, $searchStartBtn);
    console.log(e)
    $('.question-area').hide();
    $loader.show();  
    
    if ($('document').find('.match-result')){
        $loader.hide();
        $('.match-display-area').show();
    }
})


//============matched_pet=======//

let yBtn = document.getElementById('matched-pet_btn-yes');
let nBtn = document.getElementById('matched-pet_btn-no');
let container = document.getElementById('matched-pet_outline');
let body = document.getElementsByTagName('body');

yBtn?.addEventListener('click',handleClick);
nBtn?.addEventListener('click',handleClick);

async function handleClick(e){
    let lastItem = container.lastElementChild;
    let userId = container.dataset.user;
    setTimeout(()=>{
        lastItem.remove(); 
        if(container.children.length === 0){
            $matchDisplayArea.hide();
            $loader.show();
            document.location.href =`/pets/users/${userId}`
        }        
    }, 800);

    if(e.target.id =='matched-pet_btn-yes'){
        try{
            let response =await axios({method: 'post', url:'/likes', data:{animal: lastItem.dataset.animal}})
        }catch(e){
            console.log(e);
        }
        if(lastItem.classList.contains('move-left')){
            lastItem.classList.remove('move-left')
        }
        lastItem.classList.add('move-right')
    } else if(e.target.id =='matched-pet_btn-no'){
        if(lastItem.classList.contains('move-right')){
            lastItem.classList.remove('move-right')
        }
        lastItem.classList.add('move-left')
    }
   
}





