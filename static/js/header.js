var options_profile = {
    html: true,
    title: "Votre Profil",
    content: document.getElementById('popover-profile-content'),
    // trigger: 'focus'
}

var options_notifs = {
    html: true,
    title: "Notifications",
    content: document.getElementById('popover-notifs-content'),
    // trigger: 'focus',
}
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    var options = options_profile
    if (popoverTriggerEl.id === "popover-notifs") {
        options = options_notifs
    }
    return new bootstrap.Popover(popoverTriggerEl, options)
})

// const popover = new bootstrap.Popover('.popover-dismiss')
// var exampleEl = document.getElementById('example')

function get_current_user(callback) {
    $.ajax({
        url: "/current_user",
        method: "GET",
        success: function (current_user) {
            callback(current_user); // Appel du callback avec l'utilisateur récupéré
        },
        error: function (error) {
            console.error("Erreur lors de la récupération de l'utilisateur : " + error);
        }
    });
}

const popover_notif = document.getElementById("popover-notifs")
popover_notif.addEventListener("click", updateNotifs)

function updateNotifs() {
    $.ajax({
        url: "/notifs",
        method: "GET",
        success: function (notifs) {
            let listNotif = document.getElementById("listNotif");
            if (!listNotif.firstChild) console.log("here")
            while (listNotif.firstChild) {
                listNotif.removeChild(listNotif.firstChild);
            }

            get_current_user(function (current_user) {
                if (Array.isArray(notifs) && notifs.length > 0) {
                    notifs.forEach((notif) => {
                        if (notif["users"].includes(current_user.username)) {
                            console.log(notif)
                            let message = ""
                            let is_task = false
                            if (notif.task) is_task = true
                            switch (true) {
                                case (notif["type"] === "Assigned" && is_task) :
                                    message = "<b>" + notif.project + "</b>" + ":<br> Vous avez été assignée à la tâche: \"" + notif.task + "\""
                                    break;
                                case (notif["type"] === "Assigned" && !is_task):
                                    message = "Vous avez été assignée au projet: \"" + notif.project + "\""
                                    break;
                                case (notif["type"] === "Modified" && is_task):
                                    message = "<b>" + notif.project + "</b>" + " :<br> Tâche: \"" + notif.task + "\" modifiée"
                                    break;
                                case (notif["type"] === "Modified" && !is_task):
                                    message = "<b>" + notif.project + "</b>" + " :<br> Nouvelle modification"
                                    break;
                            }
                            const NotifHTML = document.createElement("div")
                            NotifHTML.id = "notif-instance"
                            NotifHTML.className = "popover-element"
                            NotifHTML.innerHTML = message
                            listNotif.appendChild(NotifHTML)
                        }
                    })
                }
                else {
                    const NoNotif = document.createElement("div")
                    NoNotif.className = "popover-element"
                    NoNotif.textContent = "Aucune notification"
                    listNotif.appendChild(NoNotif)
                }
            })
        }
    })
}
