let form2 = document.getElementById('form-2');
form2.addEventListener('submit', (e) => {
    e.preventDefault();
    let data = {
        username: "user_name",
        email: "email",
        password: "password",
        user_profile: "*"
    }
    let user_name = form2.children[0].value;
    data.username = user_name;
    let user_email = form2.children[2].value;
    data.email = user_email;
    let user_password = form2.children[4].value;
    data.password = user_password;
    if (img_data != '*') {
        data.user_profile = img_data;
    }
    data = JSON.stringify(data);
    total_account = localStorage.length;
    localStorage.setItem('data-' + total_account, data);
    close_signup();
    signed = true;
    main_user = total_account;
    setTimeout(() => {
        show_menu();
    }, 1000);
})

let form1 = document.getElementById('form-1');
form1.addEventListener('submit', (e) => {
    e.preventDefault();
    if (localStorage.length == 0) {
        show_error('Account Not Exist Please Log Up');
        goto_logup();
    }
    else {
        let check = true;
        let user_email = form1.children[0].value;
        let user_password = form1.children[2].value;
        for (let i = 0; i < localStorage.length; i++) {
            let data = JSON.parse(localStorage.getItem('data-' + i));
            if (data.email == user_email && data.password == user_password) {
                close_signin();
                signed = true;
                main_user = i;
                check = false;
                setTimeout(() => {
                    show_menu();
                }, 1000);
            }
        }
        setTimeout(() => {
            if (check)
                show_error('wrong details');
        }, 200);
    }
})


function feed_user_profile(num) {
    let data = localStorage.getItem("data-" + num);
    data = JSON.parse(data);
    if (num != main_user) {
        user_pro.children[1].innerHTML = `
                   <div class="user-img">
                        <label for="user-img"><img src="${data.user_profile != '*' ? data.user_profile : "img/fake_user.jpg"}" alt="${data.username}"></label>
                        <h2>${data.username}</h2>
                            <p>Email: ${data.email}</p>
                            <p>Last visite: 5hr Ago</p>
                            <div class="btn"><button>SignIn</button></div>
                    </div>`
    }
    else {
        user_pro.children[1].innerHTML = `
                               <div class="user-img">
                                    <label for="user-img"><img src="${data.user_profile != '*' ? data.user_profile : "img/fake_user.jpg"}" alt="${data.username}"></label>
                                    <h2>${data.username}</h2>
                                        <p>Email: ${data.email}</p>
                                        <p>Last visite: 5hr Ago</p>
                                        <div class="btn"><button onclick="close_user_profile();logout()" style="background:rgb(78, 210, 107);margin-bottom:1rem">Log Out</button></div>
                                        <div class="btn"><button onclick="delete_acc()" style="background:red;">Delete Account</button></div>
                                </div>`
    }
}

function delete_acc() {
    close_user_profile();
    close_single_window();
    if (main_user == localStorage.length - 1) {
        localStorage.removeItem("data-" + main_user);
    }
    else {
        let ta = localStorage.length;
        localStorage.removeItem("data-" + main_user);
        for (let i = main_user + 1; i < ta; i++) {
            localStorage.setItem("data-" + (i - 1), localStorage.getItem("data-" + i));
        }
        localStorage.removeItem("data-" + (ta - 1));
    }
    logout();
}