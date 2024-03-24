$(onLoadProject)

function onLoadProject() {

    // redirige vers la page projet
    $("#listProjectSidebar").on("click", "#buttonProjectSidebar", function () {
        window.location.href = "/projects/standard_view/" + $(this).val();
    });

    $("#CreateCategorie").click(function () {
            let new_category_name = $("#name_new_category").val()

            if (new_category_name === "") {
                alert("Veuillez entrer un nom de projet")
            } else {
                createCategory(new_category_name)

            }
        }
    )

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

function createCategory(new_category_name) {
    $.ajax({
        url: "/create_category",
        method: "POST",
        data: {
            category_name: new_category_name,
        },
        success: function (projects) {
            $("#ModalCreationCategory").modal("hide"); // Hide modal
        },
        error: function (projects) {
            alert('category cant be create')
        }
    });
}