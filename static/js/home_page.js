$(onLoad)

function onLoad() {

    console.log("hello world")


    $("#buttonProject").click(function () {
        //console.log("/"+ $(this).val() +" project")
        //window.location.href = "/" ;
    });

    $("#button_create_project").click(function () {
        let name = $("#name_new_project").val()
        let description = $("#description_new_project").val()
        let color = $("#colorProjectDisplay").val()
        if (name !== "") {
            create_button(name, description, color)
        } else {
            alert("Veuillez entrer un nom de projet")
        }
    });
    updateProjectList();
}

function create_button(name_project, description_project, color_project) {
    $.ajax({
        url: "/home_page",
        method: "POST",
        timeout: 2000,
        data: {
            type: 'project',
            name: name_project,
            description: description_project,
            color: color_project
        },
        success: function (response) {
            $("#modalCreateProject").modal("hide"); // Hide modal
            updateProjectList();

        }
    });
}

// Function to handle form submission
function updateProjectList() {
    $.ajax({
        url: "/projects",
        method: "GET",
        success: function (projects) {
            let listProject = document.getElementById("listProject");
            while (listProject.firstChild) {
                listProject.removeChild(listProject.firstChild);
            }


            if (projects !== null) {
                projects.forEach((project) => {
                        const newButton = document.createElement('button');
                        newButton.className = "btn btn-project"
                        newButton.textContent = project["name"];
                        newButton.style.backgroundColor = project["color"]
                        console.log(project["color"])
                        console.log(" nom du projet : " + project["name"])
                        document.getElementById("listProject").appendChild(newButton);
                    }
                )
            }

            // Créer le bouton de création de projet
            const ButtonCreateProject = document.createElement('button');
            ButtonCreateProject.classList.add("btn", "btn-create-project");
            ButtonCreateProject.setAttribute("data-bs-toggle", "modal");
            ButtonCreateProject.setAttribute("data-bs-target", "#modalCreateProject");
            ButtonCreateProject.textContent = "Créer un nouveau projet";
            document.getElementById("listProject").appendChild(ButtonCreateProject);
        }
    })
}
