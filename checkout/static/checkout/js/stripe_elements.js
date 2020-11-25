/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    And old repositories

    CSS from here:
    https://stripe.com/docs/stripe-js
*/

// Sliced to remove quotation marks
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
// Create a stripe element using the public key
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

var style = {
  base: {
    color: '#17a2b8',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#17a2b8'
    }
  },
  invalid: {
    color: '#dc3545',
    iconColor: '#dc3545',
  }
};
// Invalid set to bootstrap text-danger

var card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.on('change', function(event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    };
});

// Handle form submit
var form = document.getElementById('payment-form')

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    // Prevent the button being pressed whilst processing
    card.update({'disabled': true});
    $('#submit-button').attr('disabled', true);
    
    // Display loading overlay
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // Add data to the payment intent (save info, username, etc)
    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    var url = '/checkout/cache_checkout_data/';

    // Post data to the payment intent before passing to stripe
    $.post(url, postData).done(function() {
        // Pass the data to Stripe in the payment intent
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name_value),
                phone: $.trim(form.phone_number.value),
                address:{
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town.value),
                    state: $.trim(form.county.value),
                    postal_code: $.trim(form.postcode.value),
                    country: $.trim(form.country.value),
                }
            },
        }).then(function(result) {
            if (result.error) {
                // Display an error
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>
                `;
                $(errorDiv).html(html);
                // Allow user to fix error and re-submit
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                // The payment has been processed
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                };
            };
        });
    }).fail(function() {
        // Load the page again to show the error message if it fails without charging user
        location.reload();
    });
});
