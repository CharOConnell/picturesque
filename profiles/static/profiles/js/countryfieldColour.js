// Sort the colour of the country field in the form
let countrySelected = $('#id_default_country').val();
// Colour the placeholder bootstrap text-info
if (!countrySelected) {
    $('#id_default_country').css('color', '#17a2b8');
}
// On a change of the country field
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if (!countrySelected) {
        // If default, colour the placeholder bootstrap text-info
        $(this).css('color', '#17a2b8');
    } else {
        // Colour the input white
        $(this).css('color', '#fff');
    }
});