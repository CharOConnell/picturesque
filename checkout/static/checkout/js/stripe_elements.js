/*
    COre logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here:
    https://stripe.com/docs/stripe-js
*/

var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
// sliced to remove quotation marks
var client_secret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
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
    iconColor: '#dc3545'
  }
};
// invalid set to bootstrap text-danger

var card = elements.create('card', {style: style});
card.mount('#card-element');