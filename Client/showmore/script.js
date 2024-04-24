function toggleContent() {
    var content = document.getElementById("moreContent");
    var button = document.getElementById("toggleButton");

    // Check if the more content is displayed
    if (content.style.display === "none") {
        content.style.display = "block";
        button.textContent = "Show Less";
    } else {
        content.style.display = "none";
        button.textContent = "Show More";
    }
}
