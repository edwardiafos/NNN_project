function toggleCatalogueDropdown() {
    dropdown_menu = document.getElementById("catalogue-dropdown");

    if (dropdown_menu.style.display == 'none') {
        dropdown_menu.style.display = 'block';
    }
    else {
        dropdown_menu.style.display = 'none';
    }
}


//Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropdown')) {
        let dropdown_menus = document.getElementsByClassName("dropdown-content");
        for(let i = 0; i < dropdown_menus.length; i++) {
            dropdown_menus[i].style.display = 'none';
        }
    }
}


function showImage(event) {
    let selectedFile = event.target.files[0];
    let reader = new FileReader();

    let image = document.getElementById("selected-image-file");
    image.title = selectedFile.name;

    reader.onload = function(event) {
        image.src = event.target.result;
    }

    reader.readAsDataURL(selectedFile);
}