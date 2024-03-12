$(onLoadProject)

function onLoadProject() {

    // redirige vers la page projet
    $("#listProjectSidebar").on("click", "#buttonProjectSidebar", function() {
        window.location.href = "/projects/standard_view/" + $(this).val();
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

                let firstProjects = projects.slice(0, 3)
                firstProjects.forEach((project) => {

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