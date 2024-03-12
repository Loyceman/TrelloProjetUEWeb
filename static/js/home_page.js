$(onLoad)

function onLoad() {

    // redirige vers la page projet
    $("#listProject").on("click", "#buttonProject", function() {
        window.location.href = "/projects/standard_view/" + $(this).val();
    });

    $('#SelectedUser').select2({ // permet le fonctionnement correct de la selection multiple des utilisateurs
        theme: "bootstrap-5",
        width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
        placeholder: $(this).data('placeholder'),
        closeOnSelect: false,
    });

    let change_icon_unfold = function() {
        if (document.getElementById("project-collapser").getAttribute("aria-expanded") === "true") {
            icon_projects_unfold.src = icon_projects_unfold.src.replace("down","up")
        }
        else {
            icon_projects_unfold.src = icon_projects_unfold.src.replace("up","down")
        }
        if (document.getElementById("task-collapser").getAttribute("aria-expanded") === "true") {
            icon_tasks_unfold.src = icon_tasks_unfold.src.replace("down","up")
        }
        else {
            icon_tasks_unfold.src = icon_tasks_unfold.src.replace("up","down")
        }
    }

    function validTextField() {

      if (textField.value.trim() === '') {
        textField.classList.add('is-invalid');
      } else {
        textField.classList.remove('is-invalid');
      }
    }

    const textField = document.getElementById('name_new_project');
    textField.addEventListener("click", validTextField);
    textField.addEventListener("input", validTextField);

    const icon_projects_unfold = document.getElementById("icon-unfold-projects")
    icon_projects_unfold.addEventListener("click", change_icon_unfold)
    const icon_tasks_unfold = document.getElementById("icon-unfold-tasks")
    icon_tasks_unfold.addEventListener("click", change_icon_unfold)
    change_icon_unfold()

    $("#button_create_project").click(function () {
        let name = $("#name_new_project").val()
        let description = $("#description_new_project").val()
        let color = $("#colorProjectDisplay").val()
        let endDate = $("#dateProjectEnd").val();
        let startDate = $("#dateProjectStart").val();
        let users_selected = $('#SelectedUser').val(); // Array des membres du projets

        if (name !== "") {
            if (startDate !== "" || endDate !== "") {
                if (endDate < startDate) {
                    alert("La date de fin ne peut pas être antérieure à la date de début");
                } else {
                    create_button(name, description, color, startDate, endDate, users_selected)
                }
            } else {
                alert("Veuillez renseigner des dates pour le projet")
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
        success: function (xhr) {
            $("#modalCreateProject").modal("hide"); // Hide modal
            updateProjectList();
        },

        error: function(xhr) {
            alert(xhr.responseJSON.error)
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
                        newLayout.className = "btn-project-layout p-2 col-xl-3 col-sm-6 col-12"
                    const newBackground = document.createElement("div")
                        newBackground.className = "btn-project-layout flex-grow-1 h-100"
                        newBackground.style.backgroundColor = "#ffffff"
                    const newButton = document.createElement('button');
                        newButton.className = "btn btn-project";
                        newButton.id = "buttonProject";
                        newButton.value = project["id"];
                        newButton.style.borderColor = project["color"]
                        newButton.style.backgroundColor = project["color"].concat("0A");
                        newButton.style.boxShadow = "0 0 5px 0 ".concat(project["color"]).concat("33")
                    const newColorBar = document.createElement("span")
                        newColorBar.className = "btn-project-colorbar"
                        newColorBar.style.backgroundColor = project["color"]
                    const newTitle = document.createElement("span")
                        newTitle.className = "btn-project-title"
                        newTitle.textContent = project["name"];
                    const newDesc = document.createElement("span");
                        newDesc.className = "btn-project-desc";
                        newDesc.textContent = project["description"];


                    newLayout.appendChild(newBackground)
                    newBackground.appendChild(newButton)
                    newButton.appendChild(newColorBar)
                    newButton.appendChild(newTitle)
                    newButton.appendChild(newDesc)
                    document.getElementById("listProject").appendChild(newLayout);

                    }
                )
            }


            // // Créer le bouton de création de projet
            // const ButtonCreateProject = document.createElement('button');
            // ButtonCreateProject.classList.add("btn", "btn-create-project");
            // ButtonCreateProject.setAttribute("data-bs-toggle", "modal");
            // ButtonCreateProject.setAttribute("data-bs-target", "#modalCreateProject");
            // ButtonCreateProject.textContent = "Créer un nouveau projet";
            // document.getElementById("listProject").appendChild(ButtonCreateProject);
        }
    })
}