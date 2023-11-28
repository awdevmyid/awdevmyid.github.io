let words = ['music', 'fashion', 'fun', 'feeling', 'love', 'attraction', 'happiness'], play_word_timer;

let user = document.getElementById('user');
function feed_user() {
    if (signed) {
        let data = JSON.parse(localStorage.getItem('data-' + main_user));
        user.innerHTML = ` <div onclick="show_user_profile(${main_user})" class="user-show">
                            <div class="user-pic"><img src="${data.user_profile != '*' ? data.user_profile : "img/fake_user.jpg"}" alt="user" id="menu-pic"></div>
                            <div class="username">${data.username}</div>
                        </div>
                        `
    }
    else {
        user.innerHTML = ` <ul>
                            <li class="options" onclick="sign_in()"><i class="fa fa-sign-in" aria-hidden="true"></i>Sign
                                In</li>
                            <li class="options" onclick="sign_up()"><i class="fa fa-user-plus"
                                    aria-hidden="true"></i>Sign Up</li>
                        </ul>`
    }
}

function sign_in() {
    signin.classList.add('my-playlist');
    setTimeout(() => {
        signin.classList.add('full-width');
        setTimeout(() => {
            signin.children[1].classList.remove('login');
            play_fashion_word(0);
        }, 500);
    }, 500);
}

function play_fashion_word(num) {
    let ind = 0;
    play_word_timer = setInterval(() => {
        ind++;
        if (ind == words.length) ind = 0;
        document.getElementsByClassName('show-off-word')[num].innerText = words[ind];
    }, 1000);
}

function close_signin() {
    signin.children[1].classList.add('login');
    clearInterval(play_word_timer);
    setTimeout(() => {
        signin.classList.remove('full-width');
        setTimeout(() => {
            signin.classList.remove('my-playlist');
        }, 500);
    }, 500);
}


function sign_up() {
    setTimeout(() => {
        signup.classList.add('my-playlist');
        setTimeout(() => {
            signup.classList.add('full-width');
            setTimeout(() => {
                signup.children[1].classList.remove('login');
                play_fashion_word(1);
            }, 500);
        }, 500);
    }, 200);

}

function close_signup() {
    signup.children[1].classList.add('login');
    clearInterval(play_word_timer);
    setTimeout(() => {
        signup.classList.remove('full-width');
        setTimeout(() => {
            signup.classList.remove('my-playlist');
        }, 500);
    }, 500);
}


function goto_login() {
    close_signup();
    setTimeout(() => {
        sign_in();
    }, 900);
}


function goto_logup() {
    close_signin();
    setTimeout(() => {
        sign_up();
    }, 900);
}

function logout() {
    signed = false;
    main_user = -1;
    setTimeout(() => {
        show_menu();
        show_settings();
        show_settings();
    }, 500);
}


function show_user_profile(num) {
    setTimeout(() => {
        user_pro.classList.add('my-playlist');
        setTimeout(() => {
            user_pro.classList.add('full-width');
            setTimeout(() => {
                feed_user_profile(num);
                user_pro.children[1].classList.remove('login');
            }, 500);
        }, 500);
    }, 200);

}


function close_user_profile() {
    user_pro.children[1].classList.add('login');
    setTimeout(() => {
        user_pro.classList.remove('full-width');
        setTimeout(() => {
            user_pro.classList.remove('my-playlist');
            show_menu();
        }, 500);
    }, 500);
}


let img_data = "*";
let ele4 = document.getElementById('user-img');
ele4.onchange = function () {
    console.log("with updatd img");
    const imagefiles = ele4.files;
    const image = imagefiles[0];
    var filereader = new FileReader();
    filereader.readAsDataURL(image);
    filereader.onload = function (event) {
        img_data = event.target.result;
        ele4.parentNode.children[0].children[0].setAttribute('src', img_data);
    }
}

