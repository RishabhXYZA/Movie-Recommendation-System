function openSidebar() {
    if (window.innerWidth <= 600) {
        document.getElementById("sidebar").classList.add("active");
    }
}

function closeSidebar() {
    if (window.innerWidth <= 600) {
        document.getElementById("sidebar").classList.remove("active");
    }
}
