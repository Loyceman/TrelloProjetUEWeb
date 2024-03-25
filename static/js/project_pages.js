$(onLoadProject)

function onLoadProject() {

    $('#SelectedUserTask').select2({ // permet le fonctionnement correct de la selection multiple des utilisateurs
        theme: "bootstrap-5",
        width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
        placeholder: $(this).data('placeholder'),
        closeOnSelect: false,
    });

    // redirige vers la page projet
    $("#listProjectSidebar").on("click", "#buttonProjectSidebar", function () {
        window.location.href = "/projects/standard_view/" + $(this).val();
    });

    $("#CreateCategory").click(function () {
            let new_category_name = $("#name_new_category").val()

            if (new_category_name === "") {
                alert("Veuillez entrer un nom de projet")
            } else {
                createCategory(new_category_name, projectId)

            }
        }
    )
    // Lorsque le bouton "Ajouter une tâche" est cliqué
    $(document).on("click", ".add-card-btn", function () {
        let categoryId = $(this).data("category-id");
        $("#CreateTaskButton").attr("data-category-id", categoryId); // Stocker l'ID de la catégorie dans le bouton "Créer"
    });

    // Lorsque le bouton "Créer" est cliqué
    $("#CreateTaskButton").click(function () {
        let name = $("#name_new_task").val();
        let description = $("#description_new_task").val();
        let dueDate = $("#dueDateTask").val();
        let priority = $("input[name='flexRadioPriority']:checked").val();
        let status = $("input[name='flexRadioStatus']:checked").val();
        let users_selected = $('#SelectedUserTask').val(); // Array des utilisateurs sélectionnés pour la tâche
        let categoryId = $(this).attr("data-category-id"); // Récupérer l'ID de la catégorie

        if (name !== "") {
            create_task(name, description, dueDate, priority, status, users_selected, categoryId);
        } else {
            alert("Veuillez entrer un nom de tâche");
        }
    });


    updateProjectListSidebar()
}

function updateProjectListSidebar() {
    $.ajax({
        url: "/projects",
        method: "GET",
        success: function (projects) {
            let listProjectSidebar = document.getElementById("listProjectSidebar");
            while (listProjectSidebar.firstChild) {
                listProjectSidebar.removeChild(listProjectSidebar.firstChild);
            }

            if (projects !== null) {

                get_current_user(function (current_user) {
                    if (Array.isArray(projects) && projects.length > 0) {
                        let firstProjects = projects.slice(0, 3)
                        firstProjects.forEach((project) => {
                            if (project["members"].includes(current_user.username)) {
                                const newLayoutSidebar = document.createElement("div");
                                newLayoutSidebar.className = "btn-project-sidebar-layout"
                                const newButtonSidebar = document.createElement("button")
                                newButtonSidebar.className = "btn btn-project-sidebar";
                                newButtonSidebar.id = "buttonProjectSidebar";
                                newButtonSidebar.value = project["id"];
                                newButtonSidebar.style.borderColor = project["color"]
                                newButtonSidebar.style.backgroundColor = project["color"].concat("0A");
                                newButtonSidebar.style.boxShadow = "0 0 5px 0 ".concat(project["color"]).concat("33")
                                const newColorBarSidebar = document.createElement("span")
                                newColorBarSidebar.className = "btn-project-sidebar-colorbar"
                                newColorBarSidebar.style.backgroundColor = project["color"]
                                const newTitleSidebar = document.createElement("span")
                                newTitleSidebar.className = "btn-project-sidebar-title"
                                newTitleSidebar.textContent = project["name"];

                                newLayoutSidebar.appendChild(newButtonSidebar);
                                newButtonSidebar.appendChild(newColorBarSidebar);
                                newButtonSidebar.appendChild(newTitleSidebar);
                                document.getElementById("listProjectSidebar").appendChild(newLayoutSidebar);
                            }


                        })
                    }
                })

            }
        }
    })
}

function createCategory(category_name, project_id) {
    $.ajax({
        url: "/create_category",
        method: "POST",
        data: {
            category_name: category_name,
            project_id: project_id
        },
        success: function (projects) {
            $("#ModalCreationCategory").modal("hide"); // Hide modal
            window.location.reload();
        },
        error: function (projects) {
            alert('category cant be created')
        }
    });
}

function create_task(name, description, dueDate, priority, status, users_selected, categoryID) {
    $.ajax({
        url: "/create_task",
        method: "POST",
        timeout: 2000,
        data: {
            name: name,
            description: description,
            dueDate: dueDate,
            priority: priority,
            status: status,
            users: users_selected,
            categoryId: categoryID
        },
        success: function (xhr) {
            console.log("categoryID : " + categoryID)
            $("#ModalCreationTask").modal("hide"); // Masquer le modal
            window.location.reload();
        },
        error: function (xhr) {
            alert(xhr.responseJSON.error);
        }
    });
}

