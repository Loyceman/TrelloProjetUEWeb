$(onLoad)

function onLoad() {

    console.log("hello world")


    $("#button_create_project").click(function () {
        let name = $("#name_new_project").val()
        let description = $("#description_new_project").val()
        if (name !== "") {
            create_button(name, description)
        } else {
            alert("nom pas valide ou inexistant")
        }
    });
    updateProjectList();
}

function create_button(name_project, description_project) {
    $.ajax({
        url: "/home_page",
        method: "POST",
        timeout: 2000,
        data: {
            type: 'project',
            name: name_project,
            description: description_project
        },
        success: function (response) {
            $("#modalCreateProject").modal("hide"); // Hide modal
            updateProjectList(name_project);
        }
    });
}

// Function to handle form submission
function updateProjectList(name_project) {
    $.ajax({
        url: "/projects",
        method: "GET",
        success: function (projects) {
            console.log("append a button")
            //$("#listProject").append('<button class="btn btn-project col-xl-auto col-sm-auto col-auto p-5"> Projet Test 2 </button>')
            // ne fonctionne pas pour le moment 
        }
    });
}