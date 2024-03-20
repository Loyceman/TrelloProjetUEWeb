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
updateNotifs()

let notif_project_id
$(document).on('click', '#notif-instance', function () {
    notif_project_id = $(this).val()
    window.location.href = "/projects/standard_view/" + notif_project_id;
});

$(document).on('click', '#notif-delete', function () {
    notif_id = $(this).val()
    console.log(notif_id)
    delete_notif(notif_id)
});

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
                let counter = 0;
                notif_badge = document.getElementById("notif-badge")
                if (Array.isArray(notifs) && notifs.length > 0) {
                    notifs.forEach((notif) => {
                        if (notif["users"].includes(current_user.username)) {
                            counter ++;
                            let text_project = ""
                            let text_date = ""
                            let text_message = ""
                            let is_task = false
                            if (notif.task) is_task = true
                            switch (true) {
                                case (notif["type"] === "Assigned" && is_task) :
                                    text_project = "<b>" + notif.project_name + "</b>"
                                    text_date = notif.date + " " + notif.time
                                    text_message = "Vous avez été assignée à la tâche : <i>" + notif.task + "</i>"
                                    break;
                                case (notif["type"] === "Assigned" && !is_task):
                                    text_project = "<b>" + notif.project_name + "</b>"
                                    text_date = notif.date + " " + notif.time
                                    text_message = "Vous avez été assigné au projet"
                                    break;
                                case (notif["type"] === "Modified" && is_task):
                                    text_project = "<b>" + notif.project_name + "</b>"
                                    text_date = notif.date + " " + notif.time
                                    text_message = "Tâche : <i>" + notif.task + "</i> modifiée"
                                    break;
                                case (notif["type"] === "Modified" && !is_task):
                                    text_project = "<b>" + notif.project_name + "</b>"
                                    text_date = notif.date + " " + notif.time
                                    text_message = "Nouvelle modification"
                                    break;
                            }

                            const notifBox = document.createElement("div")
                            notifBox.className = "popover-notif-element d-flex layout-center"

                            const notifCore = document.createElement("span")
                            notifCore.id = "notif-instance"
                            notifCore.className = "flex-grow-1"
                            notifCore.value = notif["project_id"]
                            const newColorBar = document.createElement("div")
                            newColorBar.className = "notif-colorbar"
                            newColorBar.style.backgroundColor = notif["color"]
                            const newTextHead = document.createElement("div")
                            newTextHead.className = "d-flex"
                            const newTextProject = document.createElement("div")
                            newTextProject.innerHTML = text_project
                            const newTextDate = document.createElement("div")
                            newTextDate.className = "text-secondary ms-2"
                            newTextDate.innerHTML = text_date
                            const newTextMessage = document.createElement("div")
                            newTextMessage.innerHTML = text_message

                            const iconRead = document.createElement("img")
                            iconRead.className = "icon-popover-notif clickable"
                            iconRead.src = "/static/img/mail-close.svg"
                            const iconDelete = document.createElement("img")
                            iconDelete.id = "notif-delete"
                            iconDelete.className = "icon-popover-notif layout-center clickable"
                            iconDelete.value = notif["id"]
                            console.log(window.location.host)
                            iconDelete.src = "/static/img/close-icon.svg"

                            newTextHead.appendChild(newTextProject)
                            newTextHead.appendChild(newTextDate)
                            notifCore.appendChild(newColorBar)
                            notifCore.appendChild(newTextHead)
                            notifCore.appendChild(newTextMessage)
                            notifBox.appendChild(notifCore)
                            notifBox.appendChild(iconRead)
                            notifBox.appendChild(iconDelete)
                            listNotif.appendChild(notifBox)
                        }
                    })
                }
                if (counter > 0) {
                    notif_badge.style.display = "block"
                    notif_badge.textContent = "" + counter
                }
                else {
                    notif_badge.style.display = "none"
                    const NoNotif = document.createElement("div")
                    NoNotif.className = "popover-notif-element"
                    NoNotif.textContent = "Aucune notification"
                    NoNotif.style.backgroundColor = "inherit"
                    listNotif.appendChild(NoNotif)
                }
            })
        }
    })
}

function delete_notif(notif_id) {
    get_current_user(function (current_user) {
        $.ajax({
            url: "/delete_notif",
            method: "POST",
            timeout: 2000,
            data: {
                type: 'notif',
                id_notif: notif_id,
                id_user: current_user.id
            },
            success: function () {
                updateNotifs()
            }
        })
    })
}
