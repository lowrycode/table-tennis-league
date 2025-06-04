

# SPRINT 1 - SETUP

Total Story Points: 17

| Priority | Story Points | Percentage |
|----------|--------------|------------|
| MUST | 8 | 47 % |
| SHOULD | 3 | 18 % |
| COULD | 6 | 29 % |

## COMPLETED

### Set Up Project and Database (MUST) 3SP
As a **developer**, I can **set up the Django project structure and initial database** so that **I can build and run the app locally**.

**Acceptance Criteria**
- A Django project called 'cityanddistrict' is created
- The app can be run locally with current dependencies listed in requirements.txt.
- The project runs successfully using python manage.py runserver.
- A default PostgreSQL database is configured and connected.
- A .env file is used to store secrets and environment-specific variables.
- A Git repository is initialized with .gitignore and initial commit.

**Tasks**
- Create and configure a new Django project.
- Set up environment file and database config (.env, settings.py).
- Add and configure at least one base app (e.g. home, users).
- Create .gitignore and initialize Git repo.
- Install and freeze packages (pip freeze > requirements.txt).
- Test that the server and database run locally without errors.


### Deploy to Heroku (MUST) 5SP
As a **developer**, I can **deploy the Django application to Heroku** so that **the app is accessible online and can be tested in a live environment**.

Acceptance Criteria
- The Django application is successfully deployed and accessible via a Heroku URL.
- Heroku uses a production-ready server (gunicorn) and database (PostgreSQL).
- Static files (e.g., CSS, JS) are served correctly using WhiteNoise.
- Environment variables (e.g., secret keys, debug mode, database URL) are managed securely.
- The application runs without error in the production environment.

**Tasks**
- Create a Procfile to specify how Heroku runs the app.
- Configure requirements.txt (and runtime.txt) appropriately.
- Update settings.py:
- Set DEBUG = False for production.
- Configure ALLOWED_HOSTS to include the Heroku domain.
- Configure static files using WhiteNoise.
- Use dj-database-url and django-environ to handle database and environment settings.
- Create a Heroku app on Heroku website
- Set environment variables on Heroku (e.g., SECRET_KEY, DEBUG, DATABASE_URL).
- Deploy code to Heroku via Git (git push heroku main or similar).
- Test the deployed app in a browser to confirm everything is working correctly.



### Setup Base Template and Layout (SHOULD) 3SP
As a **developer**, I can **create a shared base template with reusable layout components** so that **the site remains DRY, maintainable, and visually consistent across all pages**.

**Acceptance Criteria**
- A base.html template is created with standard layout elements (navigation bar, footer, block
- content tags, link to global stylesheet, load bootstrap and font awesome kit).
- All other templates extend from base.html to reuse common layout.
- The navigation bar includes the brand logo and links to Home, Club, and a placeholder for user dropdown menu.
- A footer is present and consistent across all pages.
- The layout is responsive and styled using Bootstrap.
- The currently active page is visually highlighted in the navbar (if shown).

**Tasks**
- Create base.html template with {% block %} tags for extensibility.
- Implement navigation bar and footer in the base layout.
- Include responsive Bootstrap grid/layout system.
- Add placeholder links (Home, Club, User dropdown).
- Create example pages (e.g. home.html, club.html) that extend the base template.
- Test for visual consistency and responsiveness on multiple devices.


### Setup Cloudinary For Media Storage (COULD) 3SP
As a **developer**, I can **configure Cloudinary and use CloudinaryField for image storage** so that **the application can serve media files reliably in production**.

**Acceptance Criteria**
- Cloudinary is correctly integrated into the Django project using cloudinary and cloudinary_storage.
- Cloudinary credentials are securely stored using environment variables.
- CloudinaryField can be used in at least one model (e.g. for user profile images or club logos).
- Uploaded images are stored in Cloudinary and accessible via their URLs.
- Media files are correctly served locally in development and via Cloudinary in production.
- Admin and forms properly support uploading files using CloudinaryField.

**Tasks**
- Add cloudinary, cloudinary_storage, and any required packages to requirements.txt.
- Add CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET to .env and settings.py.
- Update DEFAULT_FILE_STORAGE and MEDIA_URL to use CloudinaryStorage.
- Add a CloudinaryField to a model
- Run makemigrations and migrate to apply changes.
- Verify that uploading an image via the Django admin or form works and the file is visible on Cloudinary.
- Test that the image displays on a web page using template tags or direct links to display uploaded images.
- Confirm media behaves correctly when deployed to Heroku.

### Custom 404 Error Page (COULD) 1SP
As a **site visitor**, I can **see a friendly custom 404 error page when I visit a broken or non-existent link** so that **I know the page doesn't exist and can easily find my way back to the homepage**.

**Acceptance Criteria**
- A custom 404 page is displayed when the user visits a non-existent URL.
- The page includes:
    - A clear message (e.g. “Page not found”).
    - A link to return to the homepage.
- The page uses the site's branding and consistent layout.
- The 404 page is responsive and works across devices.

**Tasks**
- Create a custom 404.html template with branding and link to home page.
- Update Django settings to use the custom 404 template.
- Ensure the response returns status code 404.
- Test with non-existent URLs to confirm correct behavior.
- Verify mobile responsiveness and styling consistency.


### Custom 500 Error Page (COULD) – 1SP
As a **site visitor**, I can **see a friendly custom 500 error page if something goes wrong on the server** so that **I'm not shown a generic or confusing error and can easily navigate elsewhere**.

**Acceptance Criteria**
- A custom 500 error page is displayed when an internal server error occurs.
- The page includes:
    - A clear message (e.g. “Oops! Even the pros can sometimes drop the ball.”).
    - A link to return to the homepage.
- The page uses the site's branding and consistent styling.
- The 500 page is responsive and styled for mobile, tablet, and desktop.

**Tasks**
- Create a custom 500.html template with site branding and helpful content.
- Ensure Django is set up to use the custom 500 page in production.
- Test the 500 page by simulating an error in a view (only in development or staging).
- Confirm it returns status code 500 and renders correctly.
- Verify responsiveness and styling match the rest of the site.


### Custom 403 Forbidden Page (COULD) – 1SP
As a **site visitor**, I can **see a custom 403 error page if I try to access something I'm not allowed to** so that **I understand the issue and can navigate to another part of the site**.

**Acceptance Criteria**
- A custom 403 page is displayed when a user tries to access a restricted resource they are not authorized to view.
- The page includes:
    - A clear message (e.g. “Access Denied” or “You don't have permission to view this page.”).
    - A link to return to the homepage or previous page.
- The page follows the site's branding and styling.
- The layout is responsive across devices.

**Tasks**
- Create a custom 403.html template with branded messaging and navigation options.
- Configure Django to use the custom 403 page (ensure DEBUG = False in staging/production).
- Simulate a 403 error to test display and behavior.
- Confirm the page returns a 403 response and is styled appropriately.
- Add responsiveness checks for mobile, tablet, and desktop.



# SPRINT 2 - HOME & CONTACT

Total Story Points: 20

| Priority | Story Points | Percentage |
|----------|--------------|------------|
| MUST | 6 |  43 % |
| SHOULD | 3 | 21 % |
| COULD | 5 | 36 % |

*NOTE: I underestimated how much I would get done in this sprint so ended up adding more user stories from the product backlog. These were assigned as 'COULD' user stories.*

## COMPLETED

### Fix Styling Bugs with Navigation and Main body section (MUST) 1SP

**Acceptance Criteria**
- Navbar has even margin/padding spacing above and below nav items
- Main section has narrow containers centred on the page
- Main section stacks content vertically (not horizontally)

**Tasks**
- Remove redundant margins/padding in navbar and add custom margin/padding if needed
- Change styles in main section so that content is stacked vertically and horizontally centred


### View Hero Image  (MUST)  1SP
As a **site visitor**, I can **immediately recognise the purpose of the website through viewing an engaging hero image** so that **I can decide whether to keep browsing the website**.

**Acceptance Criteria**
- A hero image is displayed prominently at the top of the homepage, visible immediately upon entering the site.
- The hero image shows a table tennis player, is visually engaging and helps the user quickly understand the website's theme and purpose.
- The hero image is displayed in high resolution and scales appropriately for different screen sizes (responsive).
- The hero image is visible without the need for user login or any further interactions.

**Tasks**
- Design/select a suitable table tennis-themed hero image.
- Add hero image section to homepage template.
- Ensure responsive styling (CSS media queries or Bootstrap).
- Test image load performance and responsiveness.
- Confirm visibility for unauthenticated users.


### View League Summary  (MUST)  1SP
As a **site visitor**, I can **view general information about the league** so that **I understand what the league is about and how to join the league**.

**Acceptance Criteria**
- Basic details about the league (region, when it was established) are displayed in a section on the homepage.
- Instructions about how to join the league are shown in the FAQ section on the homepage.
- All information is visible without requiring login.

**Tasks**
- Add league description section to homepage.
- Include information about region and established date.
- Create or integrate FAQ section with instructions to join.
- Ensure content is visible without login.
- Test responsiveness and check content.


### View FAQs  (MUST) 3SP
As a **site visitor**, I can **view a section for frequently asked questions** so that **I can find answers to the most common questions quickly**.

**Acceptance Criteria**
- A section titled “FAQs” is visible on the homepage.
- Each FAQ is displayed as a question that can be expanded to reveal an answer (accordion style).
- All FAQs are visible without requiring login.
- The FAQ section is fully responsive and functions well on mobile, tablet and laptop devices.

**Tasks**
- Design and implement FAQ section with accordion-style expand/collapse.
- Populate FAQs.
- Apply responsive layout and spacing.
- Ensure visible to all users (without requiring login) and functionality across devices.


### View Sponsors and Navigate to Websites  (SHOULD) 3SP
As a **league sponsor**, I can **see our brand logo as a clickable link on the homepage** so that **my brand gains exposure to visitors and league participants**.

**Acceptance Criteria**
- A "Sponsors" section is visible on the homepage.
- Each sponsor is represented by a logo image.
- Each logo is a clickable link that opens the sponsor's website in a new browser tab.
- Logos are displayed in an organized and responsive layout across screen sizes.
- The sponsor logos are visible without requiring login.

**Tasks**
- Build layout (e.g. flexbox) to show sponsor logos.
- Make each logo a link to the sponsor site (open in new tab).
- Ensure mobile responsiveness and spacing.
- Test logo load performance and link behavior.


### View News Items  (COULD)  5SP
As a **site visitor**, I can **see news about the league** so that **I can keep up-to-date with any matters relating to the league**.

**Acceptance Criteria**
- A news section is visible on the homepage.
- News items automatically rotate in a carousel and can be manually navigated using arrows and indicators.
- Each news item consists of a short title and a brief excerpt.
- If there are no news items, a message such as "No news updates available" is shown instead.
- News items are visible without requiring login.

**Tasks**
- Create News model.
- Build bootstrap carousel component for rotating news items.
- Add arrows and indicators for manual control.
- Display fallback message if no news is available.
- Style title and excerpt properly for readability.
- Test responsiveness and empty states.

## ADDED LATER AND COMPLETED

### View Contact Information (COULD) 1SP
As a **site visitor**, I can **easily find contact information for the league administrator** so that **I can contact them if I have any queries or requests**.

**Acceptance Criteria**
- A "Contact" link is visible on the footer of every page which navigates to the Contact page when clicked.
- The Contact page displays the league administrator's name, email address and phone number at the top of the page.
- Clicking on the email address opens the user's default email client (mailto link).
- Clicking on the phone number opens the phone dialler (on mobile devices)
- Contact information is clearly styled and the format is responsive on all device sizes.
- Contact information is visible without requiring login.

**Tasks**
- Add "Contact" link to footer.
- Create Contact page view (no login required).
- Build contact.html to show admin name, email (mailto:) and phone (tel:).
- Apply clear, responsive styling.
- Test link navigation, link behavior (email/phone), responsiveness, and public access.

## ADDED LATER BUT NOT COMPLETED (SO MOVED TO ITERATION 3)

### Submit Enquiry via Enquiry Form (COULD) 3SP
As a **site visitor**, I can **submit an enquiry using a contact form** so that **I can ask questions or request help without needing to email directly**.

**Acceptance Criteria**
- Form fields: Name (required), Email (required, valid), Phone (optional, region validated), Subject (required), Message (required).
- Shows success message and clears form on submit.
- Displays field-specific errors for invalid/missing input.
- Displays general error on server failure.
- Form is responsive across devices.
- Submissions are saved to the database for admin access.

**Tasks**
- Create Enquiry model with form fields, User, submitted_at and is_actioned
- Register model in Django admin.
- Build EnquiryForm using ModelForm.
- Add validation (required fields, email type, phone type, char limits).
- Create form view (GET/POST handling, messages, form reset).
- Add URL and contact.html template for form.
- Link "Contact Us" in base template footer.
- Style form for mobile/tablet/desktop.
- Test submission flow, admin visibility, and error handling.



### Admin Receives Contact Messages (COULD) 2SP
As a **league admin**, I can **receive contact form submissions via the dashboard** so that **I can respond to users' enquiries promptly**.

**Acceptance Criteria**
- Contact form submissions are stored in the database.
- Messages are viewable in the Django admin by authenticated admins only.
- Admin list view shows subject, name, submission time, and is_actioned status (most recent first).
- Admins can mark messages as actioned via status field.
- Full message details are viewable on click.
- Enquiry model shows with plural name "Enquiries" in Django Admin Panel

**Tasks**
- Register Enquiry model in Django admin.
- Configure list display: subject, name, submitted_at, is_actioned.
- Set default ordering to most recent.
- Make is_actioned editable from list or detail view.
- Test admin message visibility, and status updates.
- Test plural name in Django Admin Panel


# SPRINT 3 - CONTACT & USER AUTHENTICATION

Total Story Points: 24

| Priority | Story Points | Percentage |
|----------|--------------|------------|
| MUST | 14 | 58 % |
| SHOULD | 5 | 21 % |
| COULD | 5 | 21 % |

## COMPLETED

### Access Contact Page via Navbar (MUST) 1SP
As a **site visitor**, I can **navigate to the Contact page using the top navigation bar** so that **I can easily find contact information without needing to scroll to the footer**.

**Acceptance Criteria**
- A "Contact" link is visible in the top navbar on all pages.
- The "Contact" link navigates to the Contact page when clicked.
- The link is styled consistently with other navbar links and highlights when active.
- The navbar remains responsive and functional on all device sizes.
- The link is accessible without login.

**Tasks**
- Add "Contact" link to the top navbar in the base template.
- Ensure the link routes to the correct URL for the Contact page.
- Match styling and active state behavior with existing navbar links.
- Verify layout and responsiveness across screen sizes.
- Test link functionality and public access.


### Sumbit Enquiry via Enquiry Form (MUST) 3SP
As a **site visitor**, I can **submit an enquiry using a contact form** so that **I can ask questions or request help without needing to email directly**.

**Acceptance Criteria**
- Form fields: Name (required), Email (required, valid), Phone (optional, region validated), Subject (required), Message (required).
- Shows success message and clears form on submit.
- Displays field-specific errors for invalid/missing input.
- Displays general error on server failure.
- Form is responsive across devices.
- Submissions are saved to the database for admin access.

**Tasks**
- Create Enquiry model with form fields, User, submitted_at and is_actioned
- Register model in Django admin.
- Build EnquiryForm using ModelForm.
- Add validation (required fields, email type, phone type, char limits).
- Create form view (GET/POST handling, messages, form reset).
- Add URL and contact.html template for form.
- Link "Contact Us" in base template footer.
- Style form for mobile/tablet/desktop.
- Test submission flow, admin visibility, and error handling.


### Admin Receives Contact Messages (MUST) 2SP
As a **league admin**, I can **receive contact form submissions via the dashboard** so that **I can respond to users' enquiries promptly**.

**Acceptance Criteria**
- Contact form submissions are stored in the database.
- Messages are viewable in the Django admin by authenticated admins only.
- Admin list view shows subject, name, submission time, and is_actioned status (most recent first).
- Admins can mark messages as actioned via status field.
- Full message details are viewable on click.
- Enquiry model shows with plural name "Enquiries" in Django Admin Panel

**Tasks**
- Register Enquiry model in Django admin.
- Configure list display: subject, name, submitted_at, is_actioned.
- Set default ordering to most recent.
- Make is_actioned editable from list or detail view.
- Test admin message visibility, and status updates.
- Test plural name in Django Admin Panel


### Register for a New Account  (MUST) 5SP
As a **new user**, I can **register for an account using a username and password** so that **I can access member-only features and content**.

**Acceptance Criteria**
- A "Sign Up" link is available from the main navigation under the User Profile dropdown which takes users to the registration form.
- The registration form includes required fields for email address, username, password, and password confirmation.
- Password and confirmation must match before the form can be submitted.
- Email field must contain a valid format for an email address before form can be submitted.
- Validation also occurs to check username is unique and password is strong
- Upon successful registration, the user receives a success message (e.g. "Your account has been created. Please log in."), is automatically logged in and redirected to a suitable page (e.g. home page).
- If registration fails, the user remains on the form and sees appropriate error messages.
- Passwords are stored securely (hashed) and never visible or sent in plain text.
- The registration form is responsive and works on mobile, tablet, and desktop devices.
- Only unauthenticated users can view the "Sign Up" navigation item and access the registration form.

**Tasks**
- Add "Sign Up" link to User Profile menu (visible when logged out).
- Create form with required fields (email, username, password, confirm password).
- Add validation for email format, password match, username uniqueness, and password strength.
- Show success message, login and redirect to homepage.
- Display errors on failed submission.
- Ensure password is stored securely using Django defaults.
- Make form responsive across devices.
- Restrict access to signup form to unauthenticated users.
- Test form validation, user creation, and navigation visibility.


### Log In to My Account  (MUST) 3SP
As a **registered user**, I can **log in using my username and password** so that **I can access secure and personalised content**.

**Acceptance Criteria**
- Login page includes username and password fields.
- Form validation:
    - Username and password must not be empty.
    - Password is case-insensitive.
- On correct credentials, user is logged in and redirected to homepage or dashboard.
- On incorrect credentials, show “Incorrect username or password.” message.
- Login page includes:
    - Link: “Forgot your password? Contact the league administrator.”
- If already logged in:
    - Hide “Login” in and "Sign Up" navigation items and show "Logout" and "Account Settings" items.
    - Direct access to login page redirects to homepage/dashboard.

**Tasks**
- Build login view and template with username and password fields.
- Implement form validation and error messaging.
- Add links to Sign Up page and password support message.
- Redirect logged-in users away from login page (e.g. to homepage).
- Hide/show relevant nav items for authenticated users.
- Write tests:
    - Successful login
    - Invalid credentials
    - Access control for already logged-in users

### Add Remember Me Feature TO Login Page (SHOULD) 2SP
As a **registered user**, I can **log in using my username and password** so that **I can access secure and personalised content**.

**Acceptance Criteria**
- Login page includes "Remember me" checkbox.
- "Remember me" checkbox keeps user logged in across sessions.

**Tasks**
- Add remember me checkbox to login page
- Set session expiry based on “Remember me” selection (use allauth).


### Log Out of My Account  (SHOULD) 3SP
As a **logged-in user**, I can **log out of my account** so that **I can end my session securely**.

**Acceptance Criteria**
- Logged-in users see a “Log Out” option in the user menu.
- Clicking it shows a confirmation page with:
    - “Are you sure you want to log out?”
    - Log Out and Go Back buttons.
    - Clicking Go Back returns the user to the previous page.
    - Clicking Sign Out logs the user out and redirects to a suitable page (e.g. the homepage).
- After logout:
    - Unauthenticated users visiting the logout page are redirected to login page.
    - Dropdown navigation shows "Login" and "Sign Up" items

**Tasks**
- Add “Log Out” to user menu (visible only if authenticated).
- Create logout confirmation view and template (or modify allauth template).
- Implement logout logic and redirect (or use default allauth behaviour).
- Add “Go Back” button and behaviour.
- Redirect unauthenticated users away from logout page.
- Test logout behavior.
- Write tests:
    - Logout flow for authenticated users
    - Redirects for unauthenticated access
    - Nav items reflect logged out status

### Update My Password  (COULD) 5SP
As a **logged-in user**, I can **change my password** so that **I can keep my account secure**.

**Acceptance Criteria**
- Only authenticated users see a "Change Password" link in the profile dropdown.
- Clicking the link opens the Change Password page.
- The form includes:
    - Current Password (required, must match user's existing password)
    - New Password (required, must meet strength rules)
    - Confirm New Password (required, must match new password)
- Password strength rules to follow allauth defaults
- Validation errors appear next to relevant fields.
- On success, user password is changed, a success message is shown and the user is redirected to the page they were previously on
- If an unauthenticated user tries to access the change password page
    - they are redirected to the login page
    - after logging in, they are redirected back to the change password page
- The form is fully responsive on all devices.

**Tasks**
- Add "Change Password" link to profile dropdown (visible to authenticated users only).
- Create Change Password view and template (or use allauth defaults).
- For authenticated users, ensure password is changed correctly, success message is shown and user is redirected to previous page
- For unauthenticated users, ensure redirected to the login page which redirects back to change password page on successful login
- Write tests:
    - Access control (unauthenticated users redirected)
    - Form validation and error handling
    - Password update success flow

## ADDED LATER AND COMPLETED

### Account Settings Page and Navigation Link (COULD) 2SP
As a **registered user**, I can **visit my Account Settings page** so that **I can view / edit account details**.

- A logged-in user can see an “Account Settings” item in the User Profile navigation dropdown.
- Clicking the “Account Settings” link takes the user to their Account Settings page.
- The navigation item is hidden from unauthenticated users.
- If an unauthenticated user attempts to visit the Account Settings page via URL, they are redirected to the login page and returned after a successful login
- The page layout is fully responsive and works well on mobile, tablet, and desktop devices.

**Tasks**
- Add “Account Settings” link to User Profile dropdown (visible when logged in).
- Create an account_settings view with login-required protection.
- Redirect unauthenticated users to login if they access the URL directly.
- Build responsive Account Settings page layout.
- Test navigation visibility, redirection behavior, and responsive layout.


### Change Email Address in Account Settings Page (COULD) 3SP
As a **registered user**, I can **view and update my email address from the Account Settings page** so that **I can keep my account information up to date**.

**Acceptance Criteria**
- A user can see their current email address on the Account Settings page.
- The user can click an "Edit button" which navigates to a page with a form for changing their email address.
- The form validates the email before allowing submission.
- If form data is valid, the change is saved, the user is redirected to the Account Settings page and a confirmation message ("Email address updated successfully") is shown.
- If form data is invalid, an appropriate validation error message is displayed.
- Email address must be unique in the database.
- Changes reflect immediately on the Account Settings page.
- Users are only able to change details for their own account (not that of other registered users)

**Tasks**
- Display current email on the Account Settings page.
- Add "Edit" button linking to Change Email page.
- Create view and form to update email (pre-filled with current value).
- Add form validation.
- Save changes on valid submission, show success message, and redirect back to Account Settings page.
- Display validation error on invalid submission.
- Restrict access so users can only edit their own account details.
- Test form functionality, validation behavior, and access control.


### Delete My Account (COULD) 3SP
As a **registered user**, I can **delete my account from the Account Settings page** so that **I can remove my login account when no longer needed**.

**Acceptance Criteria**
- A "Delete Account" button is visible on the Account Settings page.
- Clicking the button directs the user to a confirmation page: "Are you sure you want to delete your account? This action cannot be undone." (or similar)
- The user needs to click a checkbox to confirm that they understand that the action is irreversible before they can delete their account.
- Confirming deletes the user account, logs the user out, redirects to the homepage, and shows a success message.
- Cancelling keeps the account unchanged and returns the user to the Account Settings page.
- Users can only delete their own account.

**Tasks**
- Add "Delete Account" button to the Account Settings page with explanatory text.
- Create a confirmation page for account deletion.
- Delete the user account on confirmation and log the user out.
- Redirect to homepage with a success message after deletion.
- Return to Account Settings if deletion is cancelled.
- Ensure only the logged-in user can delete their own account.
- Test deletion flow, access control, and messaging.

## DECIDED AGAINST INCLUDING IN THIS SPRINT

### Email Verification  (WON'T) 4SP
As a **new user**, I can **receive a confirmation email after registering** so that **I can verify my email address and activate my account**.

**Acceptance Criteria**
- After registering, the user is shown a message instructing them to check their email for a verification link.
- A confirmation email is sent automatically to the registered email address.
- The email contains a unique, time-limited link to activate the user's account.
- The account remains inactive (i.e. cannot log in) until the user clicks the verification link.
- Upon clicking the verification link:
    - The user's email is marked as verified.
    - The account is activated and they are redirected to the login page.
    - If the link has expired or is invalid, an appropriate error message is displayed.
    - Verified users can log in as normal.

**Tasks**
- Install and configure django-allauth (if not already used).
- Update settings to require email verification:
    - ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    - ACCOUNT_EMAIL_REQUIRED = True
    - Set ACCOUNT_AUTHENTICATION_METHOD = "email" if using email login
- Set up email backend (e.g. SMTP or console for development).
- Customize or verify default email templates
- Test email is sent on registration and that the activation link works correctly.
- Test expired or reused token scenarios for proper error handling.


# SPRINT 4 - CLUBS PAGE & CLUB ADMIN PAGE

Total Story Points: 22

| Priority | Story Points | Percentage |
|----------|--------------|------------|
| MUST | 18 | 53 % |
| SHOULD | 9 | 26 % |
| COULD | 7 | 21 % |

## COMPLETED

### View Information About Clubs  (MUST) 3SP
As a **prospective player**, I can **view summary information about clubs near me** so that **I can decide which club to join**.

**Acceptance Criteria**
- Navbar includes a "Clubs" link that highlights when active.
- "Clubs" page lists only approved clubs, sorted alphabetically.
- If no approved clubs exist, a message like "No clubs found" is shown.
- Club summaries are populated from the ClubInfo model and displayed on the page.
- The layout is responsive across mobile, tablet, and desktop devices.
- No login is required to view the Clubs page.

**Tasks**
- Add "Clubs" item to navbar with active-page highlighting.
- Create ClubInfo model (according to detailed planning ERD)
- Create view and template to list approved clubs from ClubInfo.
- Show a fallback message if no clubs exist.
- Apply responsive styling for layout across devices.
- Test page visibility and layout for public access.

### View Club Contact Details  (MUST)  2SP
As a **prospective player**, I can **view club contact details** so that **I can contact the club to ask any questions**.

**Acceptance Criteria**
- Each club's summary includes the following contact details: contact name, email address, and phone number.
- Email addresses are displayed as clickable mailto: links that open the user's default email client.
- Phone numbers are displayed as clickable tel: links for mobile devices.
- All contact details are visible without requiring login.
- The layout is responsive and works across mobile, tablet, and desktop devices.

**Tasks**
- Update ClubInfo model to include contact_name, contact_email, and contact_phone
- Modify the clubs template and view to display contact details in the club summary.
- Ensure the contact_email is displayed as a clickable mailto: link.
- Ensure the contact_phone is displayed as a clickable tel: link for mobile devices.
- Test that the email and phone links open the correct client/app when clicked.
- Ensure no contact details are shown for clubs that have missing data.
- Test visibility of contact details for unauthenticated users.
- Style contact details in a clear and consistent manner.
- Ensure the contact details layout adapts responsively across mobile, tablet, and desktop devices.

### View Club Website  (MUST) 1SP
As a **prospective player**, I can **click on a link to the club webpage** so that **I can find out more information about the club**.

**Acceptance Criteria**
- If a club has a website, a visible link is shown as part of the club's summary.
- The link opens the club website in a new browser tab or window.
- If a club does not have a website, no link is displayed (no placeholder or broken link).
- The website link is styled consistently with other links with similar hover effects.
- Club website links are accessible without requiring login.

**Tasks**
- Update club template to include a website link in the club summary.
- Ensure the website link opens in a new tab/window using the target="_blank" attribute.
- Style the website link to match other links in the page (e.g., consistent color, hover effect).
- Test that clicking the link opens the website correctly in a new tab.
- Ensure the website link is visible and accessible without requiring login.


## NOT COMPLETED

### View Club Venues  (MUST) 3SP
As a **league player**, I can **view information about club venues** so that **I know where to go when playing a team at their venue**.

**Acceptance Criteria**
- Each club listing includes a list of one or more associated venues.
- For each venue, the following details are shown: Venue name, Street address, Address line 2 (optional - only shown if present), City, County, Postcode, Parking information, Number of tables available
- Venue information is grouped under the relevant club and may appear multiple times on the page (if shared by more than one club).
- The venue address is copyable (in case users want to copy into a document or third party map app).
- All venue details are visible without requiring login.
- If a club has no associated venues, a message such as "No venues listed" is displayed.
- The layout is fully responsive across mobile, tablet, and desktop devices.

**Tasks**
- Update clubs view to include related Venue info from ClubInfo.venues.
- Update template to iterate over venues and display venue fields.
- Conditionally display Address Line 2 only if it's populated.
- Ensure all venues display under each club they are linked to.
- Add fallback message for clubs with no associated venues.
- Style venue blocks for responsive layout and copy-friendly formatting.
- Test clubs with 0, 1, and multiple venues across devices.

### Access Club Admin Page (MUST) 2SP
As a **club admin**, I can **see a "Club Admin" item in my profile dropdown menu that links to my club admin dashboard** so that **I can easily manage my club's details and admin tasks**.

**Acceptance Criteria**
- The "Club Admin" link appears in the user dropdown menu only if the logged-in user has club admin privileges.
- The link is styled consistently with other dropdown items (e.g. Account Settings, Logout).
- Clicking the link takes the user to the club admin dashboard page.
- The club admin dashboard is only accessible to users with club admin status (access is restricted server-side).
- If a non-club admin attempts to access the page directly, they are redirected or shown an appropriate "Access Denied" message.

**Tasks**
- Add a is_club_admin flag or permission check to the User model or related Club role.
- Update the user dropdown template to conditionally render the "Club Admin" item.
- Create or link the "Club Admin" page route and view.
- Protect the club admin view using a permission decorator or role check.
- Style the dropdown link to match other profile actions.
- Write tests to confirm visibility of the link for admins and absence for non-admins.
- Test direct access protection and expected redirection or messaging for unauthorized users.

### Create Club Info (MUST) 3SP
As a **club admin**, I can **submit information about my club** so that **it appears on the website once approved**.

**Acceptance Criteria**
- Only logged-in club admins can access the form.
- Admins can only submit info for their assigned club.
- The form includes all fields from the ClubInfo model, with required fields validated.
- On success:
    - A confirmation message is shown.
    - The user is redirected to the admin dashboard.
    - A preview displays with a status:
        - “Awaiting approval…” if not yet approved
        - “Approved and visible…” if approved
- Validation errors appear next to the relevant fields.
- Submitted info is hidden from public view until approved.

**Tasks**
- Build ClubInfo model and ModelForm.
- Create view, template, and route.
- Restrict form access to assigned admins only.
- Display required/optional fields correctly.
- Handle success and error messages.
- Write tests for access, validation, and submission logic.

### Update Club Info (MUST) – 2SP
As a **club administrator**, I can **update my club's details** so that **the information stays current**.

**Acceptance Criteria**
- Only authenticated club admins can access the edit form.
- Admins can only edit the club they are assigned to.
- Pre-populated form shows current club info.
- Same field validation rules as "Create Club Information".
- On successful update:
    - Show: “Club info successfully updated.”
    - Redirect to admin dashboard.
    - Show preview with approval status message.
- Inline error messages if validation fails.
- Club remains hidden from Clubs page unless approved = True.

**Tasks**
- Create view and ModelForm to handle editing.
- Pre-fill form with existing club info.
- Restrict update permissions to assigned admins.
- Add success, error, and redirect handling.
- Write tests:
    - Edit access control.
    - Field updates and validation.
    - Preview and post-update visibility.

### Delete Club Info (MUST) – 2SP
As a **club administrator**, I can **delete my club's information** so that **it's removed from the Clubs page**.

**Acceptance Criteria**
- “Delete Club Info” button is shown in admin dashboard (if info exists).
- Clicking it leads to a confirmation screen warning this action is irreversible.
- Upon confirmation:
    - The club info is deleted.
    - The user is redirected to the admin dashboard.
    - Show a message prompting them to re-add club info.
- Only authenticated admins can delete the info for the club they are assigned to.
- Deleted info is no longer shown on the Clubs page.
- The Club is not deleted from the Clubs model, only the ClubInfo model

**Tasks**
- Add delete route and confirmation view.
- Restrict deletion to authenticated, assigned admins.
- Implement confirmation screen with irreversible warning.
- On delete, redirect and show re-add message.
- Write tests:
    - Deletion logic and access control.
    - Post-deletion visibility on Clubs page.


### Assign Venues (SHOULD) – 3SP
As a **club administrator**, I can **assign an existing venue to my club** so that **it appears on the Clubs page**.

**Acceptance Criteria**
- The Club Admin dashboard displays an Assign Venue section.
- A dropdown lists only venues not already linked to the club.
- If no unlinked venues exist, the section is hidden.
- Selecting a venue and clicking "Assign" links it to the club.
- The assigned venue is shown immediately in the club's venue list.
- Only authenticated club admins can assign venues to their own club.

**Tasks**
- Implement dropdown logic to list only unlinked venues.
- Create view and form to handle assignment logic.
- Restrict access to assigned admins.
- Update the UI to reflect new assignment instantly.
- Write tests for:
    - Admin access control
    - Validation and successful submission
    - Venue relationship logic

### Unassign Venues (SHOULD) – 3SP
As a **club administrator**, I can **unassign a venue** so that **it is no longer linked to my club**.

**Acceptance Criteria**
- "Unassign" button appears below each assigned venue.
- Clicking prompts confirmation (via modal or confirmation page).
- Upon confirmation:
    - Venue is unlinked from club.
    - UI updates immediately.
    - Show message: “Venue has been unassigned.”
    - Venue no longer appears on Clubs page.
- Only club admins can unassign venues from their own club.

**Tasks**
- Create unassignment view and confirmation flow.
- Restrict action to valid admins.
- Update frontend to reflect venue removal immediately.
- Write tests for:
    - Access control
    - UI and post-action behavior

### Create Venue (SHOULD) – 3SP
As a **club administrator**, I can **delete a venue (if unlinked from other clubs or history)** so that **it is permanently removed**.

**Acceptance Criteria**
- "Delete Venue" button leads to a confirmation page.
- Users can choose to delete unapproved venue info or the venue itself
- Unapproved venue information can be deleted even if venue is shared with other clubs
- Venue can only be deleted if not linked to other clubs (or historic data if added later).
- A confirmation checkbox must be ticked before submitting the form
- Upon successful deletion:
    - Show: “Venue has been deleted.” or "Unapproved venue info has been deleted." as appropriate
    - Venue is removed from all dropdowns and dashboards.
- Only authenticated admins can access this feature.

**Tasks**
- Create route, view, and form to delete venue.
- Implement irreversible confirmation step.
- Ensure deletable condition (no club/historic linkage) is enforced.
- Update UI after deletion.
- Write tests for:
    - Deletion logic
    - Access control
    - Post-deletion database state


### Edit Venue Details (COULD) – 2SP
As a **club administrator**, I can **edit venue details (if only linked to my club)** so that **the venue information remains accurate**.

**Acceptance Criteria**
- "Edit Details" button appears under venue previews.
- Only visible if the venue is assigned exclusively to that club.
- Pre-filled form displays current venue info.
- Same validation as venue creation.
- On success:
    - Show: "Venue info updated."
    - Redirect to dashboard with updated preview.
    - Venue still hidden from Clubs page unless approved.

**Tasks**
- Create view/form with prefilled data.
- Restrict edit access to clubs with sole venue ownership.
- Add success and error messages.
- Write tests for:
    - Access control
    - Validation and updates
    - Post-update rendering

### Delete Venue (COULD) – 5SP
As a **club administrator**, I can **delete a venue (if unlinked from other clubs or history)** so that **it is permanently removed**.

**Acceptance Criteria**
- "Delete Venue" button leads to a confirmation page.
- Users can choose to delete unapproved venue info or the venue itself
- Unapproved venue information can be deleted even if venue is shared with other clubs
- Venue can only be deleted if not linked to other clubs (or historic data if added later).
- A confirmation checkbox must be ticked before submitting the form
- Upon successful deletion:
    - Show: “Venue has been deleted.”
    - Venue is removed from all dropdowns and dashboards.
- Only authenticated admins can access this feature.

**Tasks**
- Create route, view, and form to delete venue.
- Implement irreversible confirmation step.
- Ensure deletable condition (no club/historic linkage) is enforced.
- Update UI after deletion.
- Write tests for:
    - Deletion logic
    - Access control
    - Post-deletion database state

### View Club Locations on a Map  (COULD) 5SP
As a **prospective player**, I can **view the locations of club venues on a map** so that **I can easily find which clubs are closest to me**.

**Acceptance Criteria**
- A map is displayed at the top of the Clubs page showing markers for each approved club venue.
- Each marker represents a venue and includes the venue name in a tooltip or info window.
- If there are no venues to show, a message such as “No club locations available” is displayed.
- The map adjusts its zoom level and center to include all visible venues.
- The map is responsive and works correctly on mobile, tablet, and desktop devices.
- Map and markers load without requiring the user to be logged in.

**Tasks**
- Use JavaScript (Google Maps API) to render map on the Clubs page.
- In the Django view, serialize venue data with coordinates for the frontend.
- Add logic to exclude venues with missing or null lat/lng.
- Add map markers with tooltip/info window for each venue.
- Center and zoom map to fit all markers dynamically.
- Display fallback message if no coordinates exist.
- Test map rendering and responsiveness across devices.


# SPRINT 5 - CLUBS PAGE & CLUB ADMIN PAGE (PART 2)

Total Story Points: 22

| Priority | Story Points | Percentage |
|----------|--------------|------------|
| MUST | 18 | 55 % |
| SHOULD | 10 | 30 % |
| COULD | 5 | 15 % |

## COMPLETED

### View Club Venues  (MUST) 3SP
As a **league player**, I can **view information about club venues** so that **I know where to go when playing a team at their venue**.

**Acceptance Criteria**
- Each club listing includes a list of one or more associated venues.
- For each venue, the following details are shown: Venue name, Street address, Address line 2 (optional - only shown if present), City, County, Postcode, Parking information, Number of tables available
- Venue information is grouped under the relevant club and may appear multiple times on the page (if shared by more than one club).
- The venue address is copyable (in case users want to copy into a document or third party map app).
- All venue details are visible without requiring login.
- If a club has no associated venues, a message such as "No venues listed" is displayed.
- The layout is fully responsive across mobile, tablet, and desktop devices.

**Tasks**
- Update clubs view to include related Venue info from ClubInfo.venues.
- Update template to iterate over venues and display venue fields.
- Conditionally display Address Line 2 only if it's populated.
- Ensure all venues display under each club they are linked to.
- Add fallback message for clubs with no associated venues.
- Style venue blocks for responsive layout and copy-friendly formatting.
- Test clubs with 0, 1, and multiple venues across devices.

### Access Club Admin Page (MUST) 2SP
As a **club admin**, I can **see a "Club Admin" item in my profile dropdown menu that links to my club admin dashboard** so that **I can easily manage my club's details and admin tasks**.

**Acceptance Criteria**
- The "Club Admin" link appears in the user dropdown menu only if the logged-in user has club admin privileges.
- The link is styled consistently with other dropdown items (e.g. Account Settings, Logout).
- Clicking the link takes the user to the club admin dashboard page.
- The club admin dashboard is only accessible to users with club admin status (access is restricted server-side).
- If a non-club admin attempts to access the page directly, they are redirected or shown an appropriate "Access Denied" message.

**Tasks**
- Add a is_club_admin flag or permission check to the User model or related Club role.
- Update the user dropdown template to conditionally render the "Club Admin" item.
- Create or link the "Club Admin" page route and view.
- Protect the club admin view using a permission decorator or role check.
- Style the dropdown link to match other profile actions.
- Write tests to confirm visibility of the link for admins and absence for non-admins.
- Test direct access protection and expected redirection or messaging for unauthorized users.

### Create Club Info (MUST) 3SP
As a **club admin**, I can **submit information about my club** so that **it appears on the website once approved**.

**Acceptance Criteria**
- Only logged-in club admins can access the form.
- Admins can only submit info for their assigned club.
- The form includes all fields from the ClubInfo model (excluding autopopulated fields: club, created_on, approved)
- Required fields are validated and specialist fields (email, phone) are also validated.
- Validation errors appear next to the relevant fields.
- On success:
    - A success message is shown.
    - The user is redirected to the admin dashboard.
    - The status panel shows "PENDING APPROVAL" next to Club Info until it has been approved
    - New club info shows immediately in the admin panel (on page refresh) and on the Club Admin dashboard

**Tasks**
- Build ClubInfo model and ModelForm.
- Create view, template, and route.
- Restrict form access to assigned admins only.
- Display required/optional fields correctly.
- Handle success and error messages.
- Write tests for access, validation, and submission logic.

### Update Club Info (MUST) – 2SP
As a **club administrator**, I can **update my club's details** so that **the information stays current**.

**Acceptance Criteria**
- Only authenticated club admins can access the edit form.
- Admins can only edit the club they are assigned to.
- Pre-populated form shows most recent club info.
- Same field validation rules as "Create Club Information".
- Inline error messages if validation fails.
- On successful update:
    - A success message is shown.
    - The user is redirected to the admin dashboard.
    - The status panel shows "PENDING APPROVAL" next to Club Info until it has been approved
    - New club info shows immediately in the admin panel (on page refresh) and on the Club Admin dashboard
    - Outdated ClubInfo records are deleted (only the most recently approved info and the newly submitted info should remain)

**Tasks**
- Create view and ModelForm to handle editing.
- Pre-fill form with existing club info.
- Restrict update permissions to assigned admins.
- Add success, error, and redirect handling.
- Write tests:
    - Edit access control.
    - Field updates and validation.
    - Preview and post-update visibility.

### Delete Club Info (MUST) – 2SP
As a **club administrator**, I can **delete some or all of my club's information** so that **outdated or unwanted info is removed from the Clubs page**.

**Acceptance Criteria**
- “Delete Club Info” button is shown on the admin dashboard only if club info exists.
- Clicking it leads to a confirmation page with:
    - A warning that deletion is irreversible.
    - Radio buttons to choose deleting only unapproved info or all info.
- A confirmation checkbox appears if deleting all info, enabling the Delete button only when checked.
- Upon confirming deletion:
    - The selected info is deleted.
    - The user is redirected to the admin dashboard.
    - A success message prompts re-adding or updating club info.
- If deleting unapproved info when none exists, show a warning and do not delete anything.
- Only authenticated club admins assigned to the club can delete its info.
- Deleted info is immediately removed from the Clubs page and Django admin.

**Tasks**
- Add delete route, view, and confirmation page.
- Enforce access control for assigned, authenticated admins.
- Implement form with radio buttons and confirmation checkbox logic.
- Handle deletion logic and appropriate messaging.
- Update admin dashboard to show/hide delete button based on club info existence.
- Write tests for access control, deletion scenarios, and UI behavior.


### Unassign Venues (MUST) – 3SP
As a **club administrator**, I can **unassign a venue** so that **it is no longer linked to my club**.

**Acceptance Criteria**
- "Unassign" button appears next to each assigned venue.
- Clicking prompts confirmation (via modal)
- Upon confirmation:
    - Venue is unlinked from club.
    - UI updates immediately without requiring a full page refresh.
    - Venue no longer appears under club on Clubs page.
- Only club admins can unassign venues from their own club.

**Tasks**
- Add HTMX to allow for AJAX POST requests and dynamic page updates
- Restrict action to valid admins.
- Update frontend to reflect venue removal immediately.
- Write tests for:
    - Access control
    - UI and post-action behavior

## NOT COMPLETED

### Assign Venues (MUST) – 3SP
As a **club administrator**, I can **assign an existing venue to my club** so that **it appears on the Clubs page**.

**Acceptance Criteria**
- The Club Admin dashboard displays an Assign Venue button which leads to a form on a separate page.
- A dropdown lists only venues not already linked to the club.
- If no unlinked venues exist, the form is hidden and a "No other venues exist!" message displays instead
- Selecting a venue and clicking "Assign" links it to the club.
- The assigned venue is shown immediately in the club's venue list.
- Only authenticated club admins can assign venues to their own club.

**Tasks**
- Implement dropdown logic to list only unlinked venues.
- Create view and form to handle assignment logic.
- Restrict access to assigned admins.
- Update the UI to reflect new assignment instantly.
- Write tests for:
    - Admin access control
    - Validation and successful submission
    - Venue relationship logic

### Create Venue (MUST) – 3SP
As a **club administrator**, I can **delete a venue (if unlinked from other clubs or history)** so that **it is permanently removed**.

**Acceptance Criteria**
- "Delete Venue" button leads to a confirmation page.
- Users can choose to delete unapproved venue info or the venue itself
- Unapproved venue information can be deleted even if venue is shared with other clubs
- Venue can only be deleted if not linked to other clubs (or historic data if added later).
- A confirmation checkbox must be ticked before submitting the form
- Upon successful deletion:
    - Show: “Venue has been deleted.” or "Unapproved venue info has been deleted." as appropriate
    - Venue is removed from all dropdowns and dashboards.
- Only authenticated admins can access this feature.

**Tasks**
- Create route, view, and form to delete venue.
- Implement irreversible confirmation step.
- Ensure deletable condition (no club/historic linkage) is enforced.
- Update UI after deletion.
- Write tests for:
    - Deletion logic
    - Access control
    - Post-deletion database state


### Edit Venue Details (SHOULD) – 2SP
As a **club administrator**, I can **edit venue details (if only linked to my club)** so that **the venue information remains accurate**.

**Acceptance Criteria**
- "Edit Details" button appears under venue previews.
- Only visible if the venue is assigned exclusively to that club.
- Pre-filled form displays current venue info.
- Same validation as venue creation.
- On success:
    - Show: "Venue info updated."
    - Redirect to dashboard with updated preview.
    - Venue still hidden from Clubs page unless approved.

**Tasks**
- Create view/form with prefilled data.
- Restrict edit access to clubs with sole venue ownership.
- Add success and error messages.
- Write tests for:
    - Access control
    - Validation and updates
    - Post-update rendering

### Delete Venue (SHOULD) – 5SP
As a **club administrator**, I can **delete a venue (if unlinked from other clubs or history)** so that **it is permanently removed**.

**Acceptance Criteria**
- "Delete Venue" button leads to a confirmation page.
- Users can choose to delete unapproved venue info or the venue itself
- Unapproved venue information can be deleted even if venue is shared with other clubs
- Venue can only be deleted if not linked to other clubs (or historic data if added later).
- A confirmation checkbox must be ticked before submitting the form
- Upon successful deletion:
    - Show: “Venue has been deleted.”
    - Venue is removed from all dropdowns and dashboards.
- Only authenticated admins can access this feature.

**Tasks**
- Create route, view, and form to delete venue.
- Implement irreversible confirmation step.
- Ensure deletable condition (no club/historic linkage) is enforced.
- Update UI after deletion.
- Write tests for:
    - Deletion logic
    - Access control
    - Post-deletion database state

### Filter Clubs by Checklist Criteria (COULD) 5SP
As a **prospective player**, I can **filter the list of clubs based on specific criteria** so that **I can narrow down my options to clubs that meet my needs**.

**Acceptance Criteria**
- Clubs page includes a filter panel with checklist options (e.g., “Beginners”, “Kids”, etc.).
- Users can select one or more filter criteria.
- The club list updates based on selected filters.
- If no clubs match the selected criteria, a message like "No clubs were found." is shown.
- Filters persist during navigation (e.g., page refresh or back/forward navigation).
- The filter interface is responsive and usable on mobile, tablet, and desktop.

**Tasks**
- Add checklist filter UI to Clubs page.
- Implement filtering logic in the view to return clubs matching selected criteria.
- Update club list when filters are submitted.
- Ensure fallback message for zero results.
- Ensure filter state is preserved across navigation.
- Test filtering on multiple device types and browsers.





# SPRINT 6 - CLUBS PAGE & CLUB ADMIN PAGE (PART 3)

Total Story Points: 22

| Priority | Story Points | Percentage |
|----------|--------------|------------|
| MUST | 16 | 55 % |
| SHOULD | 5 | 17 % |
| COULD | 8 | 28 % |

## COMPLETED

### Assign Venues (MUST) – 3SP
As a **club administrator**, I can **assign an existing venue to my club** so that **it appears on the Clubs page**.

**Acceptance Criteria**
- The Club Admin dashboard displays an Assign Venue button which leads to a form on a separate page.
- A dropdown lists only venues not already linked to the club.
- If no unlinked venues exist, the form is hidden and a "There are no available venues to assign" message displays instead
- Selecting a venue and clicking "Assign" links it to the club.
- The assigned venue is shown immediately in the club's venue list.
- Only authenticated club admins can assign venues to their own club.

**Tasks**
- Implement dropdown logic to list only unlinked venues.
- Create view and form to handle assignment logic.
- Restrict access to assigned admins.
- Update the UI to reflect new assignment instantly.
- Write tests for:
    - Admin access control
    - Validation and successful submission
    - Venue relationship logic

### Create Venue (MUST) – 5SP
As a **club administrator**, I can **delete a venue (if unlinked from other clubs or history)** so that **it is permanently removed**.

**Acceptance Criteria**
- "Delete Venue" button leads to a confirmation page.
- Users can choose to delete unapproved venue info or the venue itself
- Unapproved venue information can be deleted even if venue is shared with other clubs
- Venue can only be deleted if not linked to other clubs (or historic data if added later).
- A confirmation checkbox must be ticked before submitting the form
- Upon successful deletion:
    - Show: “Venue has been deleted.” or "Unapproved venue info has been deleted." as appropriate
    - Venue is removed from all dropdowns and dashboards.
- Only authenticated admins can access this feature.

**Tasks**
- Create route, view, and form to delete venue.
- Implement irreversible confirmation step.
- Ensure deletable condition (no club/historic linkage) is enforced.
- Update UI after deletion.
- Write tests for:
    - Deletion logic
    - Access control
    - Post-deletion database state


### Edit Venue Details (MUST) – 3SP
As a **club administrator**, I can **edit venue details** so that **the venue information remains accurate**.

**Acceptance Criteria**
- "Edit Details" button appears next to venue in status panel.
- Clicking button takes user to Edit Venue Details page.
- If the venue is shared with another club, the page informs the user that this is a shared venue and that details will be updated for other clubs as well (if approved by league administrator)
- Pre-filled form displays current venue info.
- Same validation as venue creation.
- On success:
    - Show: "Venue info updated."
    - Redirect to dashboard with updated preview.
    - Venue still hidden from Clubs page unless approved.

**Tasks**
- Create view/form with prefilled data.
- Restrict edit access to clubs with sole venue ownership.
- Add success and error messages.
- Write tests for:
    - Access control
    - Validation and updates
    - Post-update rendering

### Delete Venue (MUST) – 5SP
As a **club administrator**, I can **delete a venue (if unlinked from other clubs or history)** so that **it is permanently removed**.

**Acceptance Criteria**
- "Delete Venue" button leads to a confirmation page.
- Users can choose to delete unapproved venue info or the venue itself
- Unapproved venue information can be deleted even if venue is shared with other clubs
- Venue can only be deleted if not linked to other clubs (or historic data if added later).
- A confirmation checkbox must be ticked before submitting the form
- Upon successful deletion:
    - Show: “Venue has been deleted.”
    - Venue is removed from all dropdowns and dashboards.
- Only authenticated admins can access this feature.

**Tasks**
- Create route, view, and form to delete venue.
- Implement irreversible confirmation step.
- Ensure deletable condition (no club/historic linkage) is enforced.
- Update UI after deletion.
- Write tests for:
    - Deletion logic
    - Access control
    - Post-deletion database state

### Filter Clubs by Checklist Criteria (SHOULD) 5SP
As a **prospective player**, I can **filter the list of clubs based on specific criteria** so that **I can narrow down my options to clubs that meet my needs**.

**Acceptance Criteria**
- Clubs page includes a filter panel with checklist options (e.g., “Beginners”, “Kids”, etc.).
- Users can select one or more filter criteria.
- The club list updates based on selected filters.
- If no clubs match the selected criteria, a message like "No clubs were found." is shown.
- Filters persist during navigation (e.g., page refresh or back/forward navigation).
- The filter interface is responsive and usable on mobile, tablet, and desktop.

**Tasks**
- Add checklist filter UI to Clubs page.
- Implement filtering logic in the view to return clubs matching selected criteria.
- Update club list when filters are submitted.
- Ensure fallback message for zero results.
- Ensure filter state is preserved across navigation.
- Test filtering on multiple device types and browsers.

## NOT COMPLETED

### View Club Locations on a Map  (COULD) 8SP
As a **prospective player**, I can **view the locations of club venues on a map** so that **I can easily find which clubs are closest to me**.

**Acceptance Criteria**
- A map is displayed at the top of the Clubs page showing markers for each approved club venue.
- Each marker represents a venue and includes the venue name in a tooltip or info window.
- If there are no venues to show, a message such as “No club locations available” is displayed.
- The map adjusts its zoom level and center to include all visible venues.
- The map is responsive and works correctly on mobile, tablet, and desktop devices.
- Map and markers load without requiring the user to be logged in.

**Tasks**
- Use JavaScript (Google Maps API) to render map on the Clubs page.
- In the Django view, serialize venue data with coordinates for the frontend.
- Add logic to exclude venues with missing or null lat/lng.
- Add map markers with tooltip/info window for each venue.
- Center and zoom map to fit all markers dynamically.
- Display fallback message if no coordinates exist.
- Test map rendering and responsiveness across devices.












# SPRINT 7 - CLUB ADMIN DASHBOARD AND ACCOUNT SETTINGS PAGE

Total Story Points: 

| Priority | Story Points | Percentage |
|----------|--------------|------------|
| MUST | 14 | 50 % |
| SHOULD | 6 | 21 % |
| COULD | 8 | 29 % |

### Styling and UI Consistency  (MUST) 3SP
As a **user**, I can **experience consistent fonts, spacing, and colours across the site** so that **the interface feels professional and easy to navigate**.

**Acceptance Criteria:**
- Fonts are legible and consistent across pages.
- Headings have consistent font sizes across pages.
- Elements are well spaced (not cramped) and position is responsive on different screen sizes.
- Consistent colour theme across the website which matches colour scheme of league logo.

**Tasks:**
- Audit current styling for inconsistencies.
- Refactor shared components or CSS/SCSS variables.
- Test styling across screen sizes and pages.

### Navbar Menu Reordering & Change Password Relocation  (MUST) 3SP
As an **authenticated user**, I can **see a simplified and logically ordered dropdown menu** so that **I can easily access account-related options without confusion**.

**Acceptance Criteria:**
- Dropdown shows 'Club Admin', 'Account Settings' and 'Logout' in that order.
- “Change Password” is removed from the dropdown and placed in Account Settings.
- Account Settings page matches updated wireframe.

**Tasks:**
- Update dropdown menu logic.
- Move password functionality into Account Settings component/view.
- Test layout and mobile responsiveness.


### Add Section for Dropping Club Admin Status  (MUST) 3SP
As a **club admin**, I can **remove my admin status from the Account Settings page** so that **I have control over my administrative role**.

**Acceptance Criteria:**
- A section appears in Account Settings if the user is a club admin.
- “Drop Admin Status” button is present and functional.
- Confirmation prompt before removal.
- Role update reflects in backend and UI.

**Tasks:**
- Add conditional section in Account Settings.
- Create confirmation page and functionality for removing admin status.
- Test functionality to good UX and ensure admin status is removed.


### Code Documentation and Formatting  (MUST) 5SP
As a **developer**, I can **view clear documentation and formatted code** so that **I can understand and maintain the project efficiently**.

**Acceptance Criteria:**
- All custom functions, methods and classes include docstrings.
- Python code follows PEP8
- Code is indented consistently
- Comments are used to organise and explain code (when appropriate)

**Tasks:**
- Add docstrings and comments
- Run code formatters (e.g. Prettier)


### Code Validation  (SHOULD) 3SP
As a **QA**, I can **validate the codebase using code validation tools** so that **I can catch errors early and ensure code quality**.

**Acceptance Criteria:**
- No major errors shown when passed through a validator
- Warnings are documented.

**Tasks:**
- Run code validators.
- Fix any identified problems.
- Document issues that need further discussion.


### Manual Testing Phase 1  (SHOULD) 3SP
As a **tester**, I can **manually test website features** so that **I can ensure a smooth and bug-free experience for users**.

**Acceptance Criteria:**
- Key user flows are manually tested on various devices/browsers.
- Pass/fail results documented.

**Tasks:**
- Run through test checklist to ensure features are still working
- Fix any issues found


### View Club Locations on a Map  (COULD) 8SP
As a **prospective player**, I can **view the locations of club venues on a map** so that **I can easily find which clubs are closest to me**.

**Acceptance Criteria**
- A map is displayed at the top of the Clubs page showing markers for each approved club venue.
- Each marker represents a venue and includes the venue name in a tooltip or info window.
- If there are no venues to show, a message such as “No locations to display.” is displayed.
- The map adjusts its zoom level and center to include all visible venues.
- The map is responsive and works correctly on mobile, tablet, and desktop devices.
- Map and markers load without requiring the user to be logged in.

**Tasks**
- Use JavaScript (Google Maps API) to render map on the Clubs page.
- In the Django view, serialize venue data with coordinates for the frontend.
- Add logic to exclude venues with missing or null lat/lng.
- Add map markers with tooltip/info window for each venue.
- Center and zoom map to fit all markers dynamically.
- Display fallback message if no coordinates exist.
- Test map rendering and responsiveness across devices.

# SPRINT 8

