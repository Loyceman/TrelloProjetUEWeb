$(onLoad)

function onLoad() {
    $('#SelectedUserSaved').select2({ // permet le fonctionnement correct de la selection multiple des utilisateurs
        theme: "bootstrap-5",
        width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
        placeholder: $(this).data('placeholder'),
        closeOnSelect: false,
    });

    $("#dateProjectStart").on('change', function () { // evite la selection de la date de fin antérieur à la date de debut
        let startDate = $(this).val();
        $("#dateProjectEnd").attr('min', startDate);
    });

    $('#SelectedUser').select2({ // permet le fonctionnement correct de la selection multiple des utilisateurs
        theme: "bootstrap-5",
        width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
        placeholder: $(this).data('placeholder'),
        closeOnSelect: false,
    });

    let change_icon_unfold = function () {
        if (document.getElementById("project-collapser").getAttribute("aria-expanded") === "true") {
            icon_projects_unfold.src = icon_projects_unfold.src.replace("down", "up")
        } else {
            icon_projects_unfold.src = icon_projects_unfold.src.replace("up", "down")
        }
        if (document.getElementById("task-collapser").getAttribute("aria-expanded") === "true") {
            icon_tasks_unfold.src = icon_tasks_unfold.src.replace("down", "up")
        } else {
            icon_tasks_unfold.src = icon_tasks_unfold.src.replace("up", "down")
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

    $("#dateProjectEndSaved").attr('min', $("#dateProjectStartSaved").val());


    let open_project_id
    $(document).on('click', '#buttonProject', function () {
        open_project_id = $(this).val()
        get_project(open_project_id)
    });

    $("#button_open_project").click(function () {
        window.location.href = "/projects/standard_view/" + open_project_id;
    });

    $("#button_delete_project").click(function () {
        delete_project(open_project_id);
    });


    $("#button_save_project").click(function () {
        let name = $("#name_saved_project").val()
        let description = $("#description_saved_project").val()
        let color = $("#colorProjectDisplaySaved").val()
        let endDate = $("#dateProjectEndSaved").val();
        let startDate = $("#dateProjectStartSaved").val();
        let users_selected = $('#SelectedUserSaved').val(); // Array des membres du projet

        if (name !== "") {
            if (endDate < startDate) {
                alert("La date de fin ne peut pas être antérieure à la date de début");
            } else {
                saved_project(name, description, color, startDate, endDate, users_selected)
            }
        } else {
            alert("Veuillez entrer un nom de projet")
        }
    });

    $("#button_create_project").click(function () {
        let name = $("#name_new_project").val()
        let description = $("#description_new_project").val()
        let color = $("#colorProjectDisplay").val()
        let endDate = $("#dateProjectEnd").val();
        let startDate = $("#dateProjectStart").val();
        let users_selected = $('#SelectedUser').val(); // Array des membres du nouveau projet

        if (name !== "") {
            if (startDate !== "" || endDate !== "") {
                alert("par default, votre projet commence aujourd'hui jusqu'au 30 decembre 2024")
            }
            if (endDate < startDate) {
                alert("La date de fin ne peut pas être antérieure à la date de début");
            } else {
                create_project(name, description, color, startDate, endDate, users_selected)
            }

        } else {
            alert("Veuillez entrer un nom de projet")
        }
    });


    updateProjectList();
}

function saved_project(name_project, description_project, color_project, start_date_project, end_date_project, project_members) {
    $.ajax({
        url: "/save_project",
        method: "POST",
        timeout: 4000,
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
            $("#modalSavedProject").modal("hide"); // Hide modal
            updateProjectList();

        },
        error: function () {
            console.log("error : posting modifications do not work")
        }
    });
}

function delete_project(project_id) {
    $.ajax({
        url: "/delete_project",
        method: "POST",
        timeout: 2000,
        data: {
            type: 'project',
            id: project_id
        },
        success: function () {
            $("#modalSavedProject").modal("hide"); // Hide modal
            alert("Votre projet a bien été supprimé")
            updateProjectList()
        }
    })
}

function create_project(name_project, description_project, color_project, start_date_project, end_date_project, project_members) {
    $.ajax({
        url: "/create_project",
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

function formatDate(date) {
    // Formater la date en AAAA-MM-JJ
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return year + "-" + month + "-" + day;
}

function get_project(project_id) {
    $.ajax({
        url: "/projects",
        method: "GET",
        success: function (projects) {
            projects.forEach(function (project) {
                if (parseInt(project.id) === parseInt(project_id)) {
                    // Compléter la modale avec les infos de project_id
                    $("#name_saved_project").val(project.name)
                    $("#description_saved_project").val(project.description)
                    $("#colorProjectDisplaySaved").val(project.color)
                    $("#dateProjectEndSaved").val(formatDate(new Date(project.endDate))); // new Date() permet de s'assurer que c'est bien un objet Date javascript
                    $("#dateProjectStartSaved").val(formatDate(new Date(project.startDate)));
                    $("#SelectedUserSaved").val(project.members)
                }
            });
        }
    })
}

function updateProjectList() {
    $.ajax({
        url: "/projects",
        method: "GET",
        success: function (projects) {
            console.log("on update")
            let listProject = document.getElementById("listProject");
            while (listProject.firstChild) {
                listProject.removeChild(listProject.firstChild);
            }

            console.log(projects)
            if (Array.isArray(projects) && projects.length > 0) {
                projects.forEach((project) => {
                        const newLayout = document.createElement("div")
                        newLayout.className = "btn-project-layout p-0 col-xl-3 col-sm-6 col-12"
                        const newButton = document.createElement('button');
                        newButton.className = "btn btn-project";
                        newButton.setAttribute("data-bs-toggle", "modal");
                        newButton.setAttribute("data-bs-target", "#modalSavedProject");
                        newButton.id = "buttonProject";
                        newButton.value = project["id"];
                        newButton.style.borderColor = project["color"]
                        newButton.style.backgroundColor = project["color"].concat("0A");
                        newButton.style.boxShadow = "0 0 5px 0".concat(project["color"]).concat("33")
                        const newColorBar = document.createElement("span")
                        newColorBar.className = "btn-project-colorbar"
                        newColorBar.style.backgroundColor = project["color"]
                        const newTitle = document.createElement("span")
                        newTitle.className = "btn-project-title"
                        newTitle.textContent = project["name"];
                        const newDesc = document.createElement("span");
                        newDesc.className = "btn-project-desc";
                        newDesc.textContent = project["description"];


                        newLayout.appendChild(newButton)
                        newButton.appendChild(newColorBar)
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