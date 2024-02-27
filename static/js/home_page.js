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
    console.log("coucou le projet : " + name_project + " avec une description : " + description_project)

    // Send AJAX request to Flask backend
    $.ajax({
        url: "/home_page",
        method: "POST",
        data: {
            name: name_project,
            description: description_project
        },
        success: function (response) {
            // If project creation is successful, update project listing
            if (response.success) {
                console.log("ça marche nickel le sang")
                //$("#createProjectModal").modal("hide"); // Hide modal
                //updateProjectList(); // Update project listing
            } else {
                console.log("que des erreurs")
            }
        }
    });
}

// Function to handle form submission
function updateProjectList() {
    $.ajax({
        url: "/home_page",
        method: "GET",
        success: function (projects) {
            $("#projectList").empty(); // Clear existing project listing

            // Append new project buttons to the project list
            projects.forEach(function (project) {
                let buttonHtml = '<button class="btn btn-outline-secondary">' + project.name + '</button>';
                $("#projectList").append(buttonHtml);
            });
        }
    });
}