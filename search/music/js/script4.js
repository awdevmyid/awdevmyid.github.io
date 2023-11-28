function map_song() {
    for (let i = 0; i < playlist.length; i++) {
        song_map[i] = i;
    }
}


function shuffle() {
    pause_music();
    body__cover[3].style.left = body__cover[2].offsetLeft + 'px';
    body__cover[4].style.width = 0;
    song_map = shuffleArray(song_map);
    Music_index = 0;
    Music = new Audio(music_list[song_map[Music_index]]);
    body__cover[1].src = song_img[song_map[Music_index]] == '*' ? 'img/helo.jpg' : song_img[song_map[Music_index]];
    load_song_complete();
    show_menu(); show_playlist();
}




function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array;
}