$(document).ready(function(){
  // Add smooth scrolling to all links
    $("a").on('click', function(event) {
        console.log('400000000000000000000000000000000000');
        if (this.hash !== "") {
        event.preventDefault();

        // Store hash
        var hash = this.hash;
        $('html, body').animate({
            scrollTop: $(hash).offset().top
        }, 1000, function(){
    
            window.location.hash = hash;
        });
        } // End if
    });
});
var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'))
var dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
    return new bootstrap.Dropdown(dropdownToggleEl)
})