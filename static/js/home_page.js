$(onLoad)

function onLoad() {

    const searchButton = document.querySelector('#button-addon1');

    searchButton.addEventListener('click', function () {
        window.location.reload(); // Actualiser la page
    });

    $('#SelectedUserTaskModified').select2({ // permet le fonctionnement correct de la selection multiple des utilisateurs
        theme: "bootstrap-5",
        width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
        placeholder: $(this).data('placeholder'),
        closeOnSelect: false,
    });

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
        get_current_user(function (current_user) {
            if (current_user.role === "Developer") {
                $("#modalSavedProject").modal("hide"); // Hide modal
                window.location.href = "/projects/standard_view/" + open_project_id;
            }
        })
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

    $('#SelectedUserTaskModified').select2({ // permet le fonctionnement correct de la selection multiple des utilisateurs
        theme: "bootstrap-5",
        width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
        placeholder: $(this).data('placeholder'),
        closeOnSelect: false,
    });

    $("#button_delete_task").click(function () {
        let task_id = $(this).val()
        console.log("on supprime la tâche :" + task_id)
        delete_task(task_id);
    });

    $("#button_save_task").click(function () {
        let name = $("#name_modified_task").val();
        let description = $("#description_modified_task").val();
        let dueDate = $("#dueDateTaskModified").val();
        let priority = $("input[name='flexRadioPriorityModified']:checked").val();
        let status = $("input[name='flexRadioStatusModified']:checked").val();
        let users_selected = $('#SelectedUserTaskModified').val(); // Array des utilisateurs sélectionnés pour la tâche
        let task_id = $(this).val()

        if (name !== "") {
            modify_task(task_id, name, description, dueDate, priority, status, users_selected);
        } else {
            alert("Veuillez entrer un nom de tâche");
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
            if (endDate < startDate) {
                alert("La date de fin ne peut pas être antérieure à la date de début");
            } else {
                create_project(name, description, color, startDate, endDate, users_selected)
            }
        } else {
            alert("Veuillez entrer un nom de projet")
        }
    });

    const searchBar = document.querySelector('#searchBar');
    const projectSelect = document.querySelector('#projectSelect');
    const statusSelect = document.querySelector('#StatusSelect');
    const prioritySelect = document.querySelector('#PrioritySelect');
    const dateSelect = document.querySelector('#DateSelect');

    searchBar.addEventListener('input', updateFormData);
    projectSelect.addEventListener('change', updateFormData);
    statusSelect.addEventListener('change', updateFormData);
    prioritySelect.addEventListener('change', updateFormData);
    dateSelect.addEventListener('change', updateFormData);

    updateProjectList();
    updateFormData()
}

function updateFormData() {
    const searchBarValue = document.querySelector('#searchBar').value;
    const projectSelectValue = document.querySelector('#projectSelect').value;
    const statusSelectValue = document.querySelector('#StatusSelect').value;
    const prioritySelectValue = document.querySelector('#PrioritySelect').value;
    const dateSelectValue = document.querySelector('#DateSelect').value;

    post_filter_input_research(searchBarValue, projectSelectValue, statusSelectValue, prioritySelectValue, dateSelectValue);
}

function get_task_value(task_id) {
    $.ajax({
        url: "/get_tasks",
        method: "GET",
        success: function (tasks) {
            console.log("on get task")
            tasks.forEach(function (task) {
                if (parseInt(task.id) === parseInt(task_id)) {
                    $("#name_modified_task").val(task.name);
                    $("#description_modified_task").val(task.description);
                    $("#dueDateTaskModified").val(task.dueDate);
                    $("input[name='flexRadioPriorityModified'][value='" + task.priority + "']").prop("checked", true);
                    $("input[name='flexRadioStatusModified'][value='" + task.status + "']").prop("checked", true);
                    $("#SelectedUserTaskModified").val(task.users);
                    $("#ModalModifyTask").modal("show");
                    $("#button_delete_task").val(task_id)
                    $("#button_save_task").val(task_id)
                }
            });
            $("#ModalModifyTask").modal("show");
        },
        error: function () {
            alert("error : tasks cant be retrieve from the database");
        }
    });
}

function modify_task(idTask, name, description, dueDate, priority, status, users_selected) {
    $.ajax({
        url: "/modify_task",
        method: "POST",
        timeout: 2000,
        data: {
            idTask: idTask,
            name: name,
            description: description,
            dueDate: dueDate,
            priority: priority,
            status: status,
            users: users_selected
        },
        success: function (xhr) {
            console.log(idTask)
            $("#ModalModifyTask").modal("hide"); // Masquer le modal
            updateNotifs()
            window.location.reload();
        }
    });
}

function delete_task(task_id) {
    $.ajax({
        url: "/delete_task",
        method: "POST",
        timeout: 2000,
        data: {
            type: 'task',
            id: task_id
        },
        success: function () {
            $("#ModalModifyTask").modal("hide"); // Hide modal
            updateNotifs()
            window.location.reload();
        },
        error: function () {
            alert("error : you cant delete this task")
        }
    })
}


function post_filter_input_research(input_search_bar, input_select_project, input_select_status, input_select_priority, input_select_date_order) {
    $.ajax({
        url: "/update_dash_board",
        method: "POST",
        timeout: 4000,
        data: {
            input_search_bar: input_search_bar,
            input_select_project: input_select_project,
            input_select_status: input_select_status,
            input_select_priority: input_select_priority,
            input_select_date_order: input_select_date_order
        },
        success: function () {
            console.log("navbar input send")
        },
        error: function () {
            alert("error : posting navbar input do not work")
        }
    });
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
            updateNotifs()

        },
        error: function () {
            alert("error : posting modifications do not work")
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
            updateNotifs()
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
        success: function (xhr) {
            $("#modalCreateProject").modal("hide"); // Hide modal
            updateProjectList();
            updateNotifs()
        },

        error: function (xhr) {
            alert(xhr.responseJSON.error)
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
            let listProject = document.getElementById("listProject");
            while (listProject.firstChild) {
                listProject.removeChild(listProject.firstChild);
            }

            get_current_user(function (current_user) {
                if (Array.isArray(projects) && projects.length > 0) {
                    projects.forEach((project) => {
                        if (project["members"].includes(current_user.username)) {
                            const newLayout = document.createElement("div")
                            newLayout.className = "btn-project-layout p-2 col-xl-3 col-sm-6 col-12"
                            const newBackground = document.createElement("div")
                            newBackground.className = "btn-project-layout flex-grow-1 h-100"
                            newBackground.style.backgroundColor = "#ffffff"
                            const newButton = document.createElement('button');
                            newButton.className = "btn btn-project";
                            if (current_user.role === 'ProjectManager') {
                                newButton.setAttribute("data-bs-toggle", "modal");
                                newButton.setAttribute("data-bs-target", "#modalSavedProject");
                            }
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
                    })
                }

                if (current_user.role === 'ProjectManager' && !document.getElementById("btn-new-project")) {
                    // Création de l'élément button
                    let button = document.createElement("button");
                    button.id = "btn-new-project";
                    button.className = "btn btn-primary layout-center";
                    button.type = "button";
                    button.setAttribute("data-bs-toggle", "modal");
                    button.setAttribute("data-bs-target", "#modalCreateProject");

                    // Création de l'élément img
                    let img = document.createElement("img");
                    img.className = "icon";
                    img.src = "static/img/add-square.svg";

                    // Création de l'élément span
                    let span = document.createElement("span");
                    span.className = "m-1";
                    span.textContent = "Créer un nouveau projet";

                    // Ajout de l'élément img et span à l'élément button
                    button.appendChild(img);
                    button.appendChild(span);

                    // Ajout du bouton à l'élément avec la classe "m-2 px-2"
                    document.querySelector(".m-2.px-2").appendChild(button);
                }
            });
        }
    })
}