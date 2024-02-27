$(onLoad)

function onLoad() {

    console.log("hello world")


    $("#button_create_project").click(function () {
        let name = $("#name_new_project").val()
        let description = $("#description_new_project").val()
        if (name !== "") {
            create_button(name, description)
        }
    });
}

function create_button(name_project, description_project) {
    $.ajax({
        url: "/home_page",
        method: "POST",
        timeout: 2000,
        data: {
            name: name_project,
            description: description_project
        },
        success: function (response) {
            $("#modalCreateProject").modal("hide"); // Hide modal
            updateProjectList(name_project)
        },
        error: function (){
            alert("erreur : envoi de données impossible")
        }
    });
}

// Function to handle form submission
function updateProjectList(name_project) {
    $.ajax({
        url: "/home_page",
        method: "GET",
        success: function (projects) {
            $("#listProject").empty(); // Clear existing project listing

            // Append new project buttons to the project list
            /*projects.forEach(function (project) {
                let buttonHtml = '<button class="btn btn-outline-secondary">' + name_project + '</button>';
                $("#listProject").append(buttonHtml);
            });*/
        }
    });
}