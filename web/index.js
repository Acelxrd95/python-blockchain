let dashboard = document.getElementById("dashboard");
let wallet = document.getElementById("wallet");
let chain = document.getElementById("chain");
let mine = document.getElementById("mine");
let settings = document.getElementById("settings")
let logarea = document.getElementById("logarea");

function displaydiv(id, link) {
    let divs = [dashboard, wallet, chain, mine, settings];
    //get element with both classes nav-link active
    let activelink = document.getElementsByClassName("nav-link active");
    activelink[0].classList.add("text-white")
    activelink[0].classList.remove("active");
    let activeli = document.getElementsByClassName("nav-item");
    activeli[0].classList.remove("nav-item");

    link.classList.add("active")
    link.classList.remove("text-white")
    link.parentElement.classList.add("nav-item")
    for (let i = 0; i < divs.length; i++) {
        if (divs[i].id === id) {
            //    add class Active
            divs[i].classList.add("active");
            divs[i].classList.remove("inactive");
        } else {
            //    remove class Active
            divs[i].classList.remove("active");
            divs[i].classList.add("inactive");
        }
    }
}

eel.expose(logger, "logger")

function logger(message) {
    // if message is not empty
    if (message.length > 0) {
        console.log(message)
        let currentDate = new Date();
        let time = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds();
        logarea.innerHTML += time + "  |  " + message + "<br>";
    }
}

function update_balance() {
    eel.get_balance()(function (data) {
        document.getElementById("balance").innerHTML = data;
    });
    // document.getElementById("balance").innerHTML = "100";
}

function send_crypto() {
    let address = document.getElementById("address").value;
    let amount = document.getElementById("amount").value;
    console.log(address, amount)
    eel.send_crypto(address, amount)(function (data) {
        console.log(data)
    });
}

function update_history() {
    eel.get_history()(function (data) {
        let history = document.getElementById("history-wallet");
        history.innerHTML = "";
        for (let i = 0; i < data.length; i++) {
            history.innerHTML += "<tr> <td>"
                + data[i][5] + "</td><td>"
                + data[i][0] + "</td><td>"
                + data[i][1] + "</td><td>"
                + data[i][2] + "</td><td>"
                + data[i][3] + "</td></tr>";
        }
    });
}

function refresh_chain() {
    eel.get_chain()(function (data) {
        // load data from json
        console.log(data)
        // data = JSON.parse(data);
        let chain = document.getElementById("chain-table");
        chain.innerHTML = "";
        chain.innerHTML = data;
        // for (let i = 0; i < data.length; i++) {
        //     chain.innerHTML += "<tr> <td>"
        //         + data[i][5] + "</td><td>"
        //         + data[i][0] + "</td><td>"
        //         + data[i][1] + "</td><td>"
        //         + data[i][2] + "</td><td>"
        //         + data[i][3] + "</td><td>"
        //         + data[i][4] + "</td><td>"
        //         + data[i][5] + "</td></tr>";
        // }
    });
}

function minefunc(bool) {
    eel.mine(bool)(function (data) {
        console.log(data)
        logger(data)
    });
}
let minestart = document.getElementById("start_mining");
let minestop = document.getElementById("stop_mining")

eel.expose(enable_mining_button, "enable_mining_button")

function enable_mining_button(bool) {
    if (bool) {
        minestart.classList.add("disabled");
        minestop.classList.remove("disabled");
    } else {
        minestart.classList.remove("disabled");
        minestop.classList.add("disabled");
    }
}