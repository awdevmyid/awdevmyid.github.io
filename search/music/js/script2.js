window.addEventListener('click', (e) => {
    if (semaphore && menu.classList.length > 1) {
        setTimeout(() => {
            if (playlist_ele.classList.length > 1) {
                if (e.clientX < (menu.offsetLeft) || e.clientX > (menu.offsetLeft + 2 * menu.offsetWidth)) {
                    menu.classList.remove('menu_show');
                    playlist_ele.classList.remove('my-playlist');
                    if (options.classList.length > 1) {
                        options.classList.remove('menu_show');
                    }
                }
            }
            else if (settings_ele.classList.length > 1) {
                if (e.clientX < (menu.offsetLeft) || e.clientX > (menu.offsetLeft + 2 * menu.offsetWidth)) {
                    menu.classList.remove('menu_show');
                    settings_ele.classList.remove('my-playlist');
                    if (options.classList.length > 1) {
                        options.classList.remove('menu_show');
                    }
                }
            }
            else {
                if (e.clientX < menu.offsetLeft || e.clientX > (menu.offsetLeft + menu.offsetWidth)) {
                    menu.classList.remove('menu_show');
                }
                if (e.clientX < menu.offsetLeft || e.clientX > (menu.offsetLeft + menu.offsetWidth)) {
                    if (options.classList.length > 1) {
                        options.classList.remove('menu_show');
                    }
                }
            }
        }, 200);
    }
})


function show_menu() {
    feed_user();
    menu.classList.add('menu_show');
}


function show_playlist() {
    if (settings_ele.classList.length > 1)
        close_single_window();
    if (playlist_ele.classList.length > 1)
        playlist_ele.classList.remove('my-playlist');
    else {
        playlist_ele.classList.add('my-playlist');
    }
}


function show_settings() {
    if (playlist_ele.classList.length > 1)
        close_single_window();
    if (settings_ele.classList.length > 1) {
        settings_ele.children[1].innerHTML = '';
        settings_ele.classList.remove('my-playlist');
    }
    else {
        settings_ele.classList.add('my-playlist');
        setTimeout(() => {


            if (signed) {
                settings_ele.children[1].innerHTML = ` <div onclick="show_option(0)" class="song"><i class="fa fa-bell-o" aria-hidden="true"></i>Error
                        Tones</div>
                    <div onclick="show_option(1)" class="song"><i class="fa fa-paint-brush" aria-hidden="true"></i>App
                        Colour</div>
                    <div onclick="show_option(2)" class="song"><i class="fa fa-refresh" aria-hidden="true"></i>Reapet
                        Status</div>
                    <div onclick="show_option(3)" class="song"><i class="fa fa-font" aria-hidden="true"></i>Font-family
                    </div>
             <div onclick="logout()" class="song"><i class="fa fa-sign-out" aria-hidden="true"></i>LogOut</div>
                    <div onclick="show_option(4)" class="song"><i class="fa fa-group" aria-hidden="true"></i>Other Accounts</div>`
            }
            else {
                settings_ele.children[1].innerHTML = ` <div onclick="show_option(0)" class="song"><i class="fa fa-bell-o" aria-hidden="true"></i>Error
                        Tones</div>
                    <div onclick="show_option(1)" class="song"><i class="fa fa-paint-brush" aria-hidden="true"></i>App
                        Colour</div>
                    <div onclick="show_option(2)" class="song"><i class="fa fa-refresh" aria-hidden="true"></i>Reapet
                        Status</div>
                    <div onclick="show_option(3)" class="song"><i class="fa fa-font" aria-hidden="true"></i>Font-family
                    </div>
                    <div onclick="show_option(4)" class="song"><i class="fa fa-group" aria-hidden="true"></i>All Accounts</div>
                    `
            }
        }, 500);
    }
}

function show_option(number) {
    options.classList.add('menu_show');
        feed_option_content(number);
}

function close_option() {
    console.log('hello');
    if (options.classList.length > 1) {
        options.classList.remove('menu_show');
    }
}

function close_single_window() {
    semaphore = 0;
    if (playlist_ele.classList.length > 1)
        playlist_ele.classList.remove('my-playlist');
    else if (settings_ele.classList.length > 1)
        settings_ele.classList.remove('my-playlist');
    if (options.classList.length > 1) {
        options.classList.remove('menu_show');
    }
    setTimeout(() => {
        semaphore = 1;
    }, 500);
}




function close_double_window() {
    if (playlist_ele.classList.length > 1) {
        menu.classList.remove('menu_show');
        playlist_ele.classList.remove('my-playlist');
    }
    else if (settings_ele.classList.length > 1) {
        menu.classList.remove('menu_show');
        settings_ele.classList.remove('my-playlist');
    }
    else {
        menu.classList.remove('menu_show');
    }
}


let error_ele = document.getElementsByClassName('demo-preview')[0];
function show_error(mytext) {
    console.log(mytext)
    error_ele.style.zIndex = 7;
    error_ele.children[0].children[2].innerHTML = mytext;
    error_music = new Audio('/error_songs/Alarm0' + error_song + '.wav');
    error_music.play();
}


function hide_error() {
    error_ele.style.zIndex = -1;
    error_music.pause();
}

function error_handle() {
    setTimeout(() => {
        show_menu();
        hide_error();
    }, 200);
}


function song_name(song_name) {
    if (song_name.length > 25) {
        flag = 1;
        let new_song_name = (song_name + "____" + song_name + "____" + song_name + "____" + song_name + "____" + song_name);
        return new_song_name;
    }
    else {
        flag = 0;
        return song_name;
    }
}

function run_song_name() {
    console.log('hello');
    body__info[1].classList.add('info__song_run')
    let temp_w = -body__info[1].offsetWidth;
    console.log(temp_w);
    song_int = setInterval(() => {
        temp_count -= 2;
        body__info[1].style.left = temp_count + 'px';
        if (temp_count <= temp_w) temp_count = 270;
    }, 50);
}