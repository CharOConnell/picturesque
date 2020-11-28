# Picturesque
## Full Stack Frameworks with Django Milestone Project - Code Institute
### Table of Contents:
1. [Project Purpose](#1.-project-purpose)
2. [User Experience](#2.-user-experience)
    - [Strategy](#strategy)
    - [Scope](#scope)
    - [Structure](#structure)
    - [Skeleton](#skeleton)
    - [Surface](#surface)
3. [Features](#3.-features)
    - [Existing Features](#existing-features)
    - [Features Left to Implement](#features-left-to-implement)
4. [Technologies Used](#4.-technologies-used)
5. [Testing](#5.-testing)
    - [Automated Testing](#automated-testing)
    - [Manual Testing](#manual-testing)
    - [Validators](#validators)
    - [Screen Sizes](#screen-sizes)
    - [Browser Details](#browser-details)
    - [Bugs Found](#bugs-found)
6. [Running The App](#6.-running-the-app)
7. [Deployment Via Heroku](#7.-deployment-via-heroku)
8. [Credits](#8.-credits)
    - [Content](#content)
    - [Media](#media)
    - [Acknowledgements](#acknowledgements)

## 1. Project Purpose
Picturesque is an e-commerce website built to sell prints of photographs displayed on the site.
The prints can be chosen to be in an array of sizes with prices which reflect the change of size.
The photographs showcased are from my personal holiday collection.

There is a landing page which tells the user more about the inspiration and photography side of the website.
There is a gallery of different collections as the photographs are subdivided into categories.
The user is able to look at a specific photograph in more details before choosing which size to purchase.
There is a user profile page where the user is able to view their order history and can update their saved details.
Finally, there is a contact page where there are FAQs about the products and a contact form for the users to contact the site owner directly.

## 2. User Experience
### Strategy
The site user stories are listed below.
- Navigation and Viewing:
    - As a shopper, I want to be able to view a list of products, so that I can select products to purchase
    - As a shopper, I want to be able to view a particular category of the product, so that I can quickly filter through products I am interested in
    - As a shopper, I want to be able to view an individual products details, so that I can see the price, description, category, image and available sizes
    - As a shopper, I want to be able to easily view the total of my purchases at any time, so that I can avoid spending more money than desired

- Filtering and Searching:
    - As a shopper, I want to be able to sort the list of available products, so I can easily see the categorised products
    - As a shopper, I want to be able to sort a specific category of products, so that I can find my favourite product in a specific category and sort the category by name
    - As a shopper, I want to be able to sort multiple categories of products simultaneously, so that I can find the most appropriate product across broad categories
    - As a shopper, I want to be able to search for a product by name or description, so that I can find a specific product that I would like to purchase
    - As a shopper, I want to be able to easily see what I have searched for and the number of results, so that I can decide quickly if the product I want is available

- Purchasing and Checkout:
    - As a shopper, I want to be able to easily select the size and quantity of the product when purchasing it, so that I can ensure that I do not accidentally select the wrong product, quantity or size
    - As a shopper, I want to be able to view items in my shopping bag to be purchased, so that I can identify the total cost of my purchase and all the items I will receive
    - As a shopper, I want to be able to adjust the quantity of individual items in the cart, so that I can easily make changes to my purchase before I checkout
    - As a shopper, I want to be able to easily enter payment information, so that I can checkout quickly and easily
    - As a shopper, I want to be able to feel that my personal and payment information is secure, so that I can confidently provide the needed information to make a purchase
    - As a shopper, I want to be able to view an order confirmation after payment, so that I can verify that my items have been purchased correctly without any mistakes
    - As a shopper, I want to be able to receive an email confirmation of my purchase, so that I can keep the information of my purchase for personal records

- Registration and User Accounts:
    - As a site user, I want to be able to easily register for an account, so that I can have my own personal account and view my profile
    - As a site user, I want to have a personalised user profile, so that I can view my order history, order confirmations and to save my payment and shipping information
    - As a site user, I want to be able to easily log in or out of my account, so that I can access my personal account information
    - As a site user, I want to be able to recover any forgotten passwords in case I forget it, so that I can recover the access to my account
    - As a site user, I want to receive an email confirmation after registering my account, so that I can verify that my account registration was successful to the site

- Store Management and Administration:
    - As a store owner, I want to be able to add a product to the website, so that I can update new items to the store
    - As a store owner, I want to be able to edit or update an existing product on the website, so that I can change product prices, descriptions, sizes and/or images on the site
    - As a store owner, I want to be able to delete an existing product from the website, so that I can remove items that are no longer for sale

### Scope
Key features to include are:
- A navigation panel which is collapsible for smaller screen sizes
- A search function, so the user can search for a particular item or category
- A product detail page showing more information about the specific product
- The edit / delete options to be hidden on products page unless a store admin so that no accidental removals or edits occur
- A user profile page with order history and details, and saved personal information
- A self-updating bag total and bag details page
- A contact form and FAQs for any user enquiries
- Links to social media accounts of the product owner

### Structure
The page will have a standard header and footer in the site colour theme. The header navigation is collapsible for smaller screen sizes.

The main pages are:
- Home page with link to the main collections page and an about section to describe the website and inspiration behind the photographs
- The main collections page where the user can choose from the different categories of products
- The main products page which shows the products with prices, images, categories. This page can show search results and filtering based on categories
- The bag page shows the contents of a users bag with the ability to proceed to checkout or to modify the bag items
- The checkout page is where the user can input their data in order to complete the purchase
- The login / logout pages are utilising the Allauth templates and allow the user to log in or out or recover their password easily
- The order confirmation page allows the user to go back shopping after looking over a review of their latest purchase
- The user profile page shows the personal information saved and order history of the user which can be viewed at any point

The schema is as follows:
| Collection | Fields        |
|------------|---------------|
| Products   | id            |
|            | name          |
|            | description   |
|            | sku           |
|            | category      |
|            | image         |
| Category   |  id           |
|            | name          |
|            | friendly_name |

### Skeleton
The mockups for the website were created using GNU Pencil software. The full versions can be found [here](media/mockups/mockups.pdf).

### Surface
The dark turquoise, light turquoise and white colour scheme was designed to feel chic yet intuitive and user-friendly.
The information should be easily picked out from the background colour, and the darker background makes the pages easier for the photographs to stand out.
The colour scheme is fairly muted which would appeal hopefully to users of all ages without any abrupt or harsh colours.


## 3. Features
- This website is built using Django with added Bootstrap frameworks, CSS, JavaScript where applicable.
- The functionality of bootstrap classes and the flexible framework it provides allowed for an easily structured webpage.
- JavaScript and JQuery additions to selected buttons allowed for posting form updates to the backend Python scripts and other page updates.
- Using the Bootstrap navbar allowed for a seamless collapsible navbar, along with the smooth functionality of the Boostrap accordion menu for the FAQs.
- A PostgreSQL database is used to host the database and the whole project is deployed through an Heroku app.

### Existing Features
- On the products page, there is a "Back To Top" button which allows the users to easily go back to the top of the page
- The navbar is sticky, so the user can always see the amount in the cart and the navigation menu
- Autofill forms for the personal details (if they exist) in the profile and checkout pages
- Forms which allow users to input information into the database such as profile information, payment information and product information for admin users
- Font Awesome icons for the socials menu on the footer

### Features Left to Implement
- Price selection dropdown menu for the inputting of new products into the database
- Review functionality for the products from users after purchasing

## 4. Technologies Used
- [HTML5](https://en.wikipedia.org/wiki/HTML5) 
    - The project uses **HTML5** as a base language for the webpage
- [CSS3](https://en.wikipedia.org/wiki/CSS)
    - The project is styled mainly using **CSS3** 
- [Bootstrap 4.5.3](https://getbootstrap.com/)
    - The project is structured using the **Bootstrap** grid system, implementing the flex and accordion attributes
- [JQuery 3.5.1](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation
- [JavaScript](https://www.javascript.com/)
    - The project uses **JavaScript** to make the functionality more smooth and interactive
- [Font Awesome 5.15.1](https://fontawesome.com/)
    - The project uses **Font Awesome** for icons within the webpage
- [Python 3.8.6](https://www.python.org/)
    - The project uses **Python** for the main backend processing
- [Django 3.1.3](https://www.djangoproject.com/)
    - The project uses **Django** as the main framework everything is based from
- [PostgreSQL](https://www.postgresql.org/)
    - The main database system is based in **PostgreSQL**
- [Heroku](https://www.heroku.com/)
    - The project is deployed from **Heroku** 
- [Stripe](https://stripe.com/gb?utm_campaign=paid_brand-UK_en_Search_Brand_Stripe-2032860449&utm_medium=cpc&utm_source=google&ad_content=355351450259&utm_term=stripe&utm_matchtype=e&utm_adposition=&utm_device=c&gclid=CjwKCAiA2O39BRBjEiwApB2IktHADHNhDsmsQuWDO45V88VNsY-9bAcoCJ7QRuvK1m4TWR_qRxxTWBoCnhYQAvD_BwE)
    - The project handles payments through **Stripe**


## 5. Testing
### Automated Testing

### Manual Testing
Testing was completed during the building of the site and some final checks at the end of the project.

Testing the contact form:
- Attempt to submit an empty form to check an error message for the designated fields appears
- Check that email address box requires an @ and produces the correct error message

Testing the payment form:
- Attempt to add an incorrect Stripe payment number and check that the error message is shown in the box below
- Attempt to submit an entry anywhere in the form to check that the error message is shown

Testing for the bag adjustments:
- The changing size option was tested using python testing separately then put into the contexts file
- Multiple sizes with multiple items were tried to ensure that no issues were seen
- An id mix up occured, but this has been fixed to ensure that the correct item is adjusted

Testing the email using Django send_mail:
- After initial setting up, the email was sent to the terminal until the emails were set up in the deployment phase
- Checked that an email was sent from my account with the correct template

Testing the search form:
- Attempt to submit an empty form to check an error message for the designated fields appears
- Check the functionality of the queries being sent to the database
- Check that the results section show up "no results" if none are found
- Check that the number of results is shown

### Validators
- HTML validity was checked using the online validator [W3C Markup Validator](validator.w3.org)
    - Errors were thrown when the html-lang and head elements were not set in template files
    - Errors also thrown when the Django template tags were assigned within the html
- CSS was checked uing the online validator [W3C CSS Jigsaw Validator](http://www.css-validator.org/)
    - No errors were thrown, but warnings were advised about the webkit-transition variables used to colour the autofill boxes in forms throughout the site
- JS was checked using the online validator [JSHint](https://jshint.com/)
    - Errors were thrown with the 'template literal syntax' used
    - Errors were thrown with the use of the $ identifier as it was not recognised in JSHint
- Python was checked to be to the flake8 standard and linted as per this standard
    - Linting was not completed for Django generated migrations

### Screen Sizes
- The website was checked for all the screen sizes available on Chrome Developer Tools
- Special attention was shown for the smallest mobile screen sizes as the fonts were too large, and the navbar had to be styled differently
- Bag summary was changed for the smaller screen sizes for ease of viewing

### Browser Details
- All development was done within Chrome browser
- Mozilla was checked and the same functionality was found 
- Safari was also checked and the same functionaly was found, but only in mobile view

### Bugs Found
There were a few bugs found within the project with only two minor outstanding issue remaining unfixed.

Fixed Bugs:
- Google autofill boxes colours are manually changed within the CSS to overwrite the standard colours from Google
- Added the sizing prices into several backend files to ensure the variable prices are covered within the project
- Changing the size of the product in the bag template. At first you could not change the size of the product but as the project progressed, it felt necessary to have this option, but indexing caused issues at first and the sizing JavaScript forced the code to be positioned in the contexts.py rather than the views.py

Remaining Bugs:
- The update button does not pass both product size and quantity to the backend, so pressing the update button updates one at a time
- The size update to the toast gives the wrong product size when multiple adjustments have been made


## 6. Running The App
To run this app locally, you will need to clone the existing repository first by doing the following:
- Navigate to the repository url: https://github.com/CharOConnell/picturesque
- Click on "Clone or Download"
- To clone the repository using HTTPS, under "Clone with HTTPS", copy the link inside the box
- To clone the repository using an SSH key, including a certificate issued by your organization's SSH certificate authority, click Use SSH, then copy the link inside the box
- Open the Git Bash
- Change the current working directory to the location where you want to clone the directory
- Type git clone, and then paste the URL you copied before
    - $ git clone https://github.com/CharOConnell/picturesque
- Press Enter and your clone will be created
- Navigate into your new project "picturesque" within your python virtual environment
- Install the requirements into your new directory by running the following code:
    - $ pip3 install requirements.txt
- Provide the values into your env.py like the env_sample.txt which is included in this app
    - Make sure that these values are not committed to version control
- Now you can run locally by running:
    - $ python3 manage.py runserver

## 7. Deployment Via Heroku
The process involved consists of:
- Running the app locally
- Adding regularly to the Git branch, committing with comments each time
- Pushing this Git branch to GitHub
- Pushing it to the Heroku branch
- Creating the necessary Procfile and requirements.txt files
- Deploying to the Heroku webpage

In order to push to Heroku from Git:
- Make sure that there is a Procfile and requirements.txt files within the repository
- Ensure any environment variables are not within version control
- Create your own Heroku app to deploy to
- Within the app, you will need to add the configuration files listed in the file env_heroku_sample.txt
- Ensure that you have your env.py setup within your local directory using the env_sample.txt file
    - For the STRIPE_SECRET_KEY and STRIPE_PUBLIC_KEY variables, these will be the same for both environmental and heroku variables
    - Note that the STRIPE_WH_KEY is related directly to the particular endpoint of the webhook on Stripe
    - Note also that the SECRET_KEY is different for both environmental and heroku variables and can be created using a Django secret key generator
- Finalise all commits and push to the GitHub repository
- To push to Heroku, you must enter the following inside the Git bash terminal:
    - $ heroku login
    - $ heroku apps
    - $ heroku git:remote -a picturesque-prints
    - $ git push heroku master
- The webpage was then deployed to Heroku


## 8. Credits
### Content
All text and descriptions on this website have been written by me.

### Media
- All the photos used were taken from my personal holiday photograph collection which I have taken.
- The mockups were drawn up by me using the software GNU Pencil.
- The no image photo was taken from a Code Institute project whos repository can be found [here](https://github.com/CharOConnell/e-commerce-learning-django)

### Acknowledgements
All elements which I have used within this page that were inspired by, or are from external sources, are linked below:
- For the base information to create the flex system, I used [this page](https://getbootstrap.com/docs/4.0/utilities/flex/) as a reference
- The dropdown menu was styled using the Bootstrap "navbar" item, found [here](https://getbootstrap.com/docs/4.0/components/navbar/)
- The FAQ menu was styled using the Bootstrap "accordion" functionality, found [here](https://getbootstrap.com/docs/4.0/components/collapse/)
- For the base django template, I used a previous Code Institute learning project for help, whos repository can be found [here](https://github.com/CharOConnell/e-commerce-learning-django)
- For changing the background in forms for autofill elements, I found the relevant css from [this website](https://css-tricks.com/snippets/css/change-autocomplete-styles-webkit-browsers/)
- For box highlighting help in the profile app, I used [this](https://css-tricks.com/snippets/css/glowing-blue-input-highlights/)
- For cloning a GitHub repository, the instructions were taken from [here](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)