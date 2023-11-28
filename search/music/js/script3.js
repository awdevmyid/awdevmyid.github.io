let colors = ['#e4f2fb', 'rgb(255, 136, 136)', 'rgb(190, 255, 190)', 'rgb(255, 255, 187)', 'rgb(175, 175, 175)', '#9b459e', 'rgb(136, 255, 245)', 'rgb(148, 85, 85)', 'rgb(255, 123, 237)', 'rgb(60, 255, 0)'];
let fonts = [`"Roboto", Arial, Verdana, sans-seri`, `'Anek Devanagari', sans-serif`, `'BhuTuka Expanded One', cursive`, `'Lato', sans-serif`, `'Nerko One', cursive`, `'Rubik Microbe', cursive`];
let color_index = 0, font_index = 0;


function repeat_action(number) {
    repeat_status = number;
    options.children[0].children[0].innerHTML = 'Repeat All'
    mark_defult(number);
}


function alarm_action(number) {
    error_song = number + 1;
    mark_defult(number);
}


function color_action(number) {
    color_index = number;
    document.getElementById('main_body').style.background = colors[number];
    mark_defult(number);
}

function font_action(number) {
    font_index = number;
    document.getElementById('main_body').style.fontFamily = fonts[number];
    mark_defult(number);
}

function mark_defult(number) {
    Array.from(options.children[1].children).forEach(tone => {
        tone.classList.remove('selected_repeat');
    })
    options.children[1].children[number].classList.add('selected_repeat');
}



function feed_option_content(number) {
    // return;
    options.innerHTML = '';
    if (number == 0) {
        options.innerHTML = `<div class="header" style="background-color: #2196f3;">
        <div class="name_com">Alarm</div>
                    <div class="cancel" onclick="close_option()"><svg class="w-6 h-6" fill="none" stroke="currentColor"
                            viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M6 18L18 6M6 6l12 12"></path>
                            </svg></div>
                            </div>
                <div class="songs" style="text-align: center;">
                    <div onclick="alarm_action(0)" class="song">Alarm-1</div>
                    <div onclick="alarm_action(1)" class="song">Alarm-2</div>
                    <div onclick="alarm_action(2)" class="song">Alarm-3</div>
                    <div onclick="alarm_action(3)" class="song">Alarm-4</div>
                    <div onclick="alarm_action(4)" class="song">Alarm-5</div>
                    <div onclick="alarm_action(5)" class="song selected_repeat">Alarm-6</div>
                    <div onclick="alarm_action(6)" class="song">Alarm-7</div>
                    <div onclick="alarm_action(7)" class="song">Alarm-8</div>
                    <div onclick="alarm_action(8)" class="song">Alarm-9</div>
                    </div>`
        mark_defult(error_song - 1);
    }
    else if (number == 1) {
        options.innerHTML = `<div class="header" style="background-color: #2196f3;">
        <div class="name_com">Colors</div>
        <div class="cancel" onclick="close_option()"><svg class="w-6 h-6" fill="none" stroke="currentColor"
        viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg></div>
        </div>
        <div class="songs" style="text-align: center;">
        <div onclick="color_action(0)" style="background-color: #e4f2fb;" class="song selected_repeat">Blue</div>
        <div onclick="color_action(1)" style="background-color: rgb(255, 136, 136);" class="song">Red</div>
        <div onclick="color_action(2)" style="background-color: rgb(190, 255, 190);" class="song">Green</div>
        <div onclick="color_action(3)" style="background-color: rgb(255, 255, 187);" class="song">Yellow</div>
        <div onclick="color_action(4)" style="background-color: rgb(175, 175, 175);" class="song">Black</div>
        <div onclick="color_action(5)" style="background-color: #9b459e;" class="song">voilet</div>
        <div onclick="color_action(6)" style="background-color: rgb(136, 255, 245);" class="song">Water</div>
        <div onclick="color_action(7)" style="background-color: rgb(148, 85, 85);" class="song">Dark Red</div>
        <div onclick="color_action(8)" style="background-color: rgb(255, 123, 237);" class="song">Pink</div>
        <div onclick="color_action(9)" style="background-color: rgb(60, 255, 0);" class="song">Light Green</div>
        </div>`
        mark_defult(color_index);

    }
    else if (number == 2) {
        options.innerHTML = ` <div class="header" style="background-color: #2196f3;">
        <div class="name_com">Choose</div>
        <div class="cancel" onclick="close_option()"><svg class="w-6 h-6" fill="none"
        stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M6 18L18 6M6 6l12 12"></path>
                        </svg></div>
                </div>
                <div class="songs" style="text-align: center;">
                <div onclick="repeat_action(0)" class="song selected_repeat">No Reapet</div>
                <div onclick="repeat_action(1)" class="song">Reapet One</div>
                <div onclick="repeat_action(2)" class="song">Reapet All</div>
                </div>`
        mark_defult(repeat_status);
    }
    else if (number == 3) {
        options.innerHTML = ` <div class="header" style="background-color: #2196f3;">
        <div class="name_com">Font Family</div>
        <div class="cancel" onclick="close_option()"><svg class="w-6 h-6" fill="none" stroke="currentColor"
                viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"></path>
            </svg></div>
    </div>
    <div class="songs" style="text-align: center;">
        <div onclick="font_action(0)" style='font-family: "Roboto", Arial, Verdana, sans-seri;'
            class="song selected_repeat">Choose me</div>
        <div onclick="font_action(1)" style="font-family: 'Anek Devanagari', sans-serif;" class="song">
            Choose me</div>
        <div onclick="font_action(2)" style="font-family: 'BhuTuka Expanded One', cursive;" class="song">
            Choose me</div>
        <div onclick="font_action(3)" style="font-family: 'Lato', sans-serif;" class="song">Choose me</div>
        <div onclick="font_action(4)" style="font-family: 'Nerko One', cursive;" class="song">Choose me
        </div>
        <div onclick="font_action(5)" style="font-family: 'Rubik Microbe', cursive;" class="song">Choose me
        </div>
    </div>`
        mark_defult(font_index);
    }
    else if (number == 4) {
        options.innerHTML = `<div class="header" style="background-color: #2196f3;">
        <div class="name_com">Users</div>
        <div class="cancel" onclick="close_option()"><svg class="w-6 h-6" fill="none" stroke="currentColor"
                viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"></path>
            </svg></div>
    </div>
    <div class="songs" style="text-align: center;">
     </div >`
        for (let i = 0; i < localStorage.length; i++) {
            let data = localStorage.getItem("data-" + i);
            data = JSON.parse(data);
            options.children[1].innerHTML += `<div onclick="show_user_profile(${i})" style="cursor: pointer;" class="user-show">
                            <div class="user-pic"><img src="${data.user_profile != '*' ? data.user_profile : "img/fake_user.jpg"}" alt="user" id="menu-pic"></div>
                            <div class="username">${data.username}</div>
                        </div>`
        }
        mark_defult(main_user);
    }
}