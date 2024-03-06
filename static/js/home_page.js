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


    $("#dateProjectStart").on('change', function () {
        let startDate = $(this).val();
        $("#dateProjectEnd").attr('min', startDate);
    });


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
                        const newButton = document.createElement('button');
                        newButton.className = "btn btn-project";
                        newButton.id = "buttonProject";
                        newButton.value = project["id"];
                        newButton.textContent = project["name"];
                        newButton.style.backgroundColor = project["color"];
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
