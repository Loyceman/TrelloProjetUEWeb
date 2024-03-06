$(onLoad)

function onLoad() {

    // $("#listProject").on("click", "#buttonProject", function() {
    //     window.location.href = "/projects/standard_view/" + $(this).val();
    // });

    $('#SelectedUser').select2({ // permet le fonctionnement correct de la selection multiple des utilisateurs
        theme: "bootstrap-5",
        width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
        placeholder: $(this).data('placeholder'),
        closeOnSelect: false,
    });

    const icon_unfold = document.getElementById("icon-unfold-projects")
    icon_unfold.addEventListener("click", function() {
        if (icon_unfold.src.includes("chevron-down")) {
            icon_unfold.src = icon_unfold.src.replace("down","up")
        }
        else {
            icon_unfold.src = icon_unfold.src.replace("up","down")
        }
    })

    $("#button_create_project").click(function () {
        let name = $("#name_new_project").val()
        let description = $("#description_new_project").val()
        let color = $("#colorProjectDisplay").val()
        let endDate = $("#dateProjectEnd").val();
        let startDate = $("#dateProjectStart").val();
        let users_selected = $('#SelectedUser').val(); // Array des membres du projets

        if (name !== "") {
            if (endDate < startDate) {
                alert("La date de fin ne peut pas être antérieure à la date de début");
            } else {
                create_button(name, description, color, startDate, endDate, users_selected)
            }
        } else {
            alert("Veuillez entrer un nom de projet")
        }


    });
    updateProjectList();
}

function create_button(name_project, description_project, color_project, start_date_project, end_date_project, project_members) {
    $.ajax({
        url: "/home_page",
        method: "POST",
        timeout: 2000,
        data: {
            type: 'project',
            name: name_project,
            description: description_project,
            color: color_project,
            startDate: start_date_project,
            endDate: end_date_project,
            members: project_members
        },
        success: function () {
            $("#modalCreateProject").modal("hide"); // Hide modal
            updateProjectList();

        }
    });
}

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
                    const newLayout = document.createElement("div")
                        newLayout.className = "btn-project-layout p-0 col-xl-3 col-sm-6 col-12"
                    const newButton = document.createElement('button');
                        newButton.className = "btn btn-project p-0";
                        newButton.id = "buttonProject";
                        newButton.value = project["id"];
                        newButton.style.border = "2px solid"
                        newButton.style.borderColor = project["color"]
                    const newTitle = document.createElement("span")
                        newTitle.className = "btn-project-title"
                        newTitle.textContent = project["name"];
                        newTitle.style.backgroundColor = project["color"];
                    const newDesc = document.createElement("span");
                        newDesc.className = "btn-project-desc p-2";
                        newDesc.style.backgroundColor = "var(--c-light)"
                        newDesc.textContent = project["description"];


                    newLayout.appendChild(newButton)
                    newButton.appendChild(newTitle)
                    newButton.appendChild(newDesc)
                    document.getElementById("listProject").appendChild(newLayout);
                    }
                )
            }


            // // Créer le bouton de création de projet
            const ButtonCreateProject = document.createElement('button');
            ButtonCreateProject.classList.add("btn", "btn-create-project");
            ButtonCreateProject.setAttribute("data-bs-toggle", "modal");
            ButtonCreateProject.setAttribute("data-bs-target", "#modalCreateProject");
            ButtonCreateProject.textContent = "Créer un nouveau projet";
            document.getElementById("listProject").appendChild(ButtonCreateProject);
        }
    })
}