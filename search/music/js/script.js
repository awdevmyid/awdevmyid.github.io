let control_btn = document.getElementsByClassName('list--buttons')[0].children;
let body__cover = document.getElementsByClassName('body__cover')[0].children;
let body__info = document.getElementsByClassName('body__info')[0].children;
body__cover[3].style.left = body__cover[2].offsetLeft + 'px';
body__cover[4].style.left = body__cover[2].offsetLeft + 'px';
body__cover[4].style.width = 0;
body__info[1].style.left = 0;
let abc, xx, Music, Music_index = 0, timeint = -1, song_int = -1, music_list = [], playlist = [], error_song = 6, error_music, flag = 0, temp_count = 0, repeat_status = 0, song_map = [], song_img = [], signed = false, main_user = -1, total_account = 0;
let ele = document.getElementById('file');
let menu = document.getElementsByClassName('menu')[0];
let songs = document.getElementsByClassName('songs')[0];
let playlist_ele = menu.parentElement.children[2];
let settings_ele = menu.parentElement.children[3];
let options = menu.parentElement.children[4];
let signin = menu.parentElement.children[5];
let signup = menu.parentElement.children[6];
let user_pro = menu.parentElement.children[7];
let semaphore = 1;
let line_width = body__cover[2].clientWidth;

ele.addEventListener('change', () => {
    load_song();
})

control_btn[1].addEventListener('click', () => {
    if (playlist.length == 0) {
        show_error('list is empty <span onclick="error_handle()" style="color: blue; cursor: pointer; ">click me</span> and Load songs');
        return;
    }
    if (Music.paused) {
        play_music();
    }
    else pause_music();
})

body__cover[2].addEventListener('click', (e) => {
    if (playlist.length == 0) {
        show_error('list is empty <span onclick="error_handle()" style="color: blue;cursor: pointer;">click me</span> and Load songs');
        return;
    }
    seek_music(e.clientX);
})


body__cover[4].addEventListener('click', (e) => {
    if (playlist.length == 0) {
        show_error('list is empty <span onclick="error_handle()" style="color: blue;cursor: pointer;">click me</span> and Load songs');
        return;
    }
    seek_music(e.clientX);
})



function load_song() {
    for (let i = 0; i < ele.files.length; i++) {
        let myfile = ele.files[i];
        myfile = new File([myfile], `${myfile.name}` + ".mp3", {
            type: "audio/mp3",
            lastModified: new Date(),
        });
        const reader = new FileReader();
        let temp_music;
        reader.onload = function () {
            var str = this.result;
            music_list[i] = str;
        };
        reader.readAsDataURL(myfile);
        playlist[i] = ele.files[i].name;
    }
    map_song();
    run_test();
    process_song_img();
}



function run_test() {
    setTimeout(() => {
        Music = new Audio(music_list[song_map[Music_index]]);
        body__cover[1].src = song_img[song_map[Music_index]] == '*' ? 'img/helo.jpg' : song_img[song_map[Music_index]];
        let new_song_name = song_name(playlist[song_map[Music_index]]);
        document.getElementsByClassName('info__song')[0].innerHTML = `${new_song_name}`;
        menu.children[2].children[1].children[3].children[1].innerText = playlist.length;
        load_song_complete();
    }, 2000);
}



function load_song_complete() {
    let new_song_name = song_name(playlist[song_map[Music_index]]);
    document.getElementsByClassName('info__song')[0].innerHTML = `${new_song_name}`;
    songs.innerHTML = '';
    for (let ii = 0; ii < music_list.length; ii++) {
        songs.innerHTML += `<div class="song" id="${ii}">${playlist[song_map[ii]]}</div>`
    }
    Array.from(songs.children).forEach(song_key => {
        song_key.addEventListener('click', () => {
            play_musicNum(parseInt(song_key.getAttribute('id')));
        })
    })
}



function play_music() {
    if (playlist.length == 0) {
        show_error('list is empty <span onclick="error_handle()" style="color: blue;cursor: pointer;">click me</span> and Load songs');
        return;
    }
    load_song_complete();
    document.getElementById(Music_index).style.color = 'red';
    let new_song_name = song_name(playlist[song_map[Music_index]]);
    document.getElementsByClassName('info__song')[0].innerHTML = `${new_song_name}`;
    body__cover[1].src = song_img[song_map[Music_index]] == '*' ? 'img/helo.jpg' : song_img[song_map[Music_index]];
    if (flag)
        run_song_name();
    if (Music.currentTime >= Music.duration) {
        Music = new Audio(music_list[song_map[Music_index]]);
        body__cover[3].style.left = body__cover[2].offsetLeft + 'px';
        body__cover[4].style.width = 0;
    }
    setnotificationMetadata(playlist[song_map[Music_index]]);
    control_btn[1].children[0].innerHTML = '<i class="fa fa-pause"></i>';

    console.log(Music.duration);
    let song_length = Music.duration;
    console.log(song_length);
    xx = line_width / song_length;
    xx /= 10;
    timeint = setInterval(() => {
        body__cover[3].setAttribute('title', parseInt(Music.currentTime));
        body__cover[3].style.left = (parseFloat(body__cover[3].style.left) + xx) + 'px';
        body__cover[4].style.width = (parseFloat(body__cover[4].style.width) + xx) + 'px';
    }, 100);
    Music.play({inline: true});

    Music.addEventListener('ended', () => {
        next_music();
    })
}



function pause_music() {
    Music.pause();
    control_btn[1].children[0].innerHTML = '<i class="fa fa-play"></i>';
    body__info[1].style.left = 0;
    clearInterval(song_int);
    clearInterval(timeint);
}



function next_music() {
    if (playlist.length == 0) {
        show_error('list is empty <span onclick="error_handle()" style="color: blue;cursor: pointer;">click me</span> and Load songs');
        return;
    }
    pause_music();
    body__cover[3].style.left = body__cover[2].offsetLeft + 'px';
    body__cover[4].style.width = 0;
    temp_count = 0;
    timeint = -1;
    Music_index++;
    if (songs_end()) {
        Music = new Audio(music_list[song_map[Music_index]]);
        Music.onloadedmetadata = function () {
            play_music();
        }
    }
}



function previous_music() {
    if (playlist.length == 0) {
        show_error('list is empty <span onclick="error_handle()" style="color: blue;cursor: pointer;">click me</span> and Load songs');
        return;
    }
    pause_music();
    body__cover[3].style.left = body__cover[2].offsetLeft + 'px';
    body__cover[4].style.width = 0;
    temp_count = 0;
    timeint = -1;
    Music_index--;
    Music = new Audio(music_list[song_map[Music_index]]);
    Music.onloadedmetadata = function () {
        play_music();
    }
}



function seek_music(point) {
    let yy = point - body__cover[3].getBoundingClientRect().left;
    let zz = point - body__cover[2].getBoundingClientRect().left;
    body__cover[3].style.left = (parseFloat(body__cover[3].style.left) + yy) + 'px';
    body__cover[4].style.width = (parseFloat(body__cover[4].style.width) + yy) + 'px';
    Music.currentTime = (Music.duration / body__cover[2].clientWidth) * zz;
}



function play_musicNum(x) {
    pause_music();
    body__cover[3].style.left = body__cover[2].offsetLeft + 'px';
    body__cover[4].style.width = 0;
    timeint = -1;
    Music_index = x;
    Music = new Audio(music_list[song_map[Music_index]]);
    Music.onloadedmetadata = function () {
        play_music();
    }
}



function replay() {
    body__info[1].style.left = 0;
    Music.currentTime = 0;
    body__cover[3].style.left = body__cover[2].offsetLeft + 'px';
    body__cover[4].style.width = 0;
}



function songs_end() {
    body__info[1].style.left = 0;
    if (repeat_status == 1) {
        Music_index -= 1;
        return 1;
    }
    if (Music_index == playlist.length) {
        if (repeat_status == 2) {
            Music_index = 0;
            return 1;
        }
        Music_index = 0;
        show_error("Music list Ended");
        body__info[1].style.left = 0;
        body__info[1].classList.remove('info__song_run');
        Music = new Audio(music_list[song_map[Music_index]]);
        let new_song_name = song_name(playlist[Music_index]);
        document.getElementsByClassName('info__song')[0].innerHTML = `${new_song_name}`;
        body__cover[1].src = song_img[song_map[Music_index]] == '*' ? 'img/helo.jpg' : song_img[song_map[Music_index]];
        return 0;
    }
    return 1;
}
