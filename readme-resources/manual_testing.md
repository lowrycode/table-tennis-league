# Manual Tests

These tests cover all of the implemented User Stories and were carried out at various stages of development and before submitting the final project. They were all conducted on different browsers and devices (as specified in the README).

## Django Admin Panel

### NewsItem Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel displays correct fields (Title, Active From, Active To) in correct order (descending on Active From field) |
| ✓ | Admin Panel allows filtering by Active From and Active To |
| ✓ | Error message displayed when missing required fields |
| ✓ | Error message displayed when active_to is before active_from |
| ✓ | Error message displayed when active_to is not in the future |

### Enquiry Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows Enquiry model under Contact app with the plural name "Enquiries" |
| ✓ | Admin Panel displays correct fields (Subject, Name, Submitted At, Is Actioned) in correct order (descending on Submitted At field) |
| ✓ | Admin Panel allows filtering by Is Actioned field |
| ✓ | Error message displayed when missing required fields |
| ✓ | Error message displayed when invalid email |
| ✓ | Error message displayed when invalid UK phone number |
| ✓ | Form data submitted by POST request immediately visible in Admin Panel on page reload |
| ✓ | Default fields (User, Is Actioned) correctly populated |

### Club Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows Club model under Clubs app |
| ✓ | Club model contains a required field called name |
| ✓ | Error message displayed when missing the required field |
| ✓ | Error message displayed when non-unique name provided |

### ClubInfo Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows ClubInfo model under Clubs app |
| ✓ | ClubInfo model contains all expected fields |
| ✓ | Fields are correctly assigned as whether they are required or not |
| ✓ | Error message displayed when missing required fields |
| ✓ | One-to-one relationship with Club is enforced with appropriate error message displayed |
| ✓ | Helper text displayed for image field to recommend image format, resolution and orientation |
| ✓ | Boolean fields are unchecked by default |

### ClubReview Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows ClubReview model under Clubs app |
| ✓ | ClubReviews are listed by updated_on field (most recent first) |
| ✓ | ClubReviews can be filtered by is_approved status |
| ✓ | ClubReview model contains all expected fields |
| ✓ | Fields are all required and score must be in range 1 to 5 |
| ✓ | Error message displayed when missing required fields |
| ✓ | Constraint for Club and User together is enforced (a user cannot write more than one review per club) |
| ✓ | Approved field is unchecked by default |

### VenueInfo Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows VenueInfo model under Clubs app |
| ✓ | VenueInfo model contains all expected fields |
| ✓ | Fields are correctly assigned as whether they are required or not |
| ✓ | Error message displayed when missing required fields |
| ✓ | One-to-one relationship with Venue is enforced with appropriate error message displayed |
| ✓ | Boolean fields are unchecked by default |
| ✓ | Latitude and Longitude fields are autopopulated from valid postcode if left blank |
| ✓ | Invalid postcode does not autopopulate latitude and longitude fields - record is still saved without errors or crashes but no location is added to the map |

### Division Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows Division model under League app |
| ✓ | Divisions are listed with name and rank and ordered by rank (low to high) |
| ✓ | Division model contains all expected fields |
| ✓ | Fields are correctly assigned as whether they are required or not |
| ✓ | Error message displayed when missing required fields |
| ✓ | Error message displayed when non-unique value entered for either field |
| ✓ | Delete button is missing from detail view if division is linked to a season but shows for unlinked divisions |
| ✓ | List view shows custom bulk action 'Delete unlinked divisions' |
| ✓ | 'Delete unlinked divisions' action deletes unlinked divisions (with success message) but shows warning for linked divisions and does not delete these |


### Season Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows Season model under League app |
| ✓ | Seasons are listed with name and is_current status |
| ✓ | Seasons are listed in order of season start_date (desc) |
| ✓ | Season model contains all expected fields |
| ✓ | Fields are correctly assigned as whether they are required or not |
| ✓ | Error message displayed when missing required fields |
| ✓ | Error message displayed when non-unique value entered for name, short_name and slug fields |
| ✓ | Error message shows when start date is after end date |
| ✓ | Error message shows when registration opens is after registration closes |
| ✓ | Error message shows when registration closes is after start date |
| ✓ | When 'is current' status is set to true for a season and the record is saved, all other seasons have 'is current' status set to false |


### Week Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows Week model under League app |
| ✓ | Weeks are listed with name, start_date, details and season |
| ✓ | Weeks are listed in order of start_date (desc in admin, asc in model) |
| ✓ | Week model contains all expected fields |
| ✓ | Unique constraint is enforced (season and name together) |
| ✓ | Fields are correctly assigned as whether they are required or not and missing fields display error messages |

### Player Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows Player model under League app |
| ✓ | Players are listed with surname, forename, DOB, current_club and club_status |
| ✓ | Players are listed in order of surname then forename (asc) |
| ✓ | Player model contains all expected fields |
| ✓ | Unique constraint is enforced (surname, forename and DOB together) |
| ✓ | Fields are correctly assigned as whether they are required or not and missing fields display error messages |
| ✓ | Default club_status is 'pending' |
| ✓ | Deletion restricted if player is linked to a PlayerSeason record |

### TeamPlayer Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows TeamPlayer model under League app |
| ✓ | TeamPlayers are listed with player, team and paid fees status |
| ✓ | TeamPlayers are listed in order of player (asc by surname) then team |
| ✓ | TeamPlayer model contains all expected fields |
| ✓ | Unique constraint is enforced (players cannot register with more than one team in the same season but can be registered in multiple seasons) |
| ✓ | Cannot add record if club on player profile does not have 'confirmed' status and related error message shows |
| ✓ | Cannot add record if club on player profile does not match club stated in the form and related error message shows |
| ✓ | All fields are required and missing fields display error messages |
| ✓ | Default paid_fees is False |

### Team Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows Team model under League app |
| ✓ | Teams are listed with team name, club, division and season |
| ✓ | Teams are listed in order of team name (asc) then season (most recent first) |
| ✓ | Team model contains all expected fields |
| ✓ | All fields are required and missing fields display error messages |
| ✓ | Unique constraint is enforced (team name and season together) |
| ✓ | Home day defaults to Monday and home time defaults to 7pm |
| ✓ | Home time can only be within range 6pm to 8pm and field error message shows correctly |
| ✓ | Division cannot be changed after season start_date but can before |

### Fixture Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows Fixture model under League app |
| ✓ | Fixtures are listed with expected str representation (Season Week - Home vs Away) |
| ✓ | Fixtures are listed by date (desc) |
| ✓ | Fixture model contains all expected fields |
| ✓ | All fields are required and missing fields display error messages |
| ✓ | Unique constraint is enforced (same season/home/away together) but home/away can be swapped |
| ✓ | Time constraint enforced (must be between 6pm and 8pm) |
| ✓ | Date constraint enforced (must be within same week) |
| ✓ | Duplicate team constraint enforced (can't have same home and away team) |
| ✓ | Division constraint enforced (both teams must be in stated division) |
| ✓ | Season constraint enforced (both teams must be assigned to stated season) |
| ✓ | Venue auto-populated from home team default venue if left blank |

### FixtureResult Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows FixtureResult model under League app |
| ✓ | Fixture results are listed with expected str representation (<home_team> <home_score> vs <away_score> <away_team>) |
| ✓ | Fixture results are listed by fixture date (desc) |
| ✓ | FixtureResult model contains all expected fields |
| ✓ | Required fields display error messages when missing |
| ✓ | Unique constraint is enforced (can't have more than one fixture result per fixture) |
| ✓ | Total score (home + away) must add up to 10 |
| ✓ | Winner field is auto-populated and read-only |
| ✓ | A FixtureResult record can be updated and deleted in Django Admin |

### SinglesMatch Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows SinglesMatch model under League app |
| ✓ | Singles matches are listed with expected str representation (<home_player> <home_sets> vs <away_sets> <away_player>) |
| ✓ | Singles matches are listed alphabetically by home player surname, then away player surname |
| ✓ | SinglesMatch model contains all expected fields |
| ✓ | Required fields display error messages when missing |
| ✓ | Unique constraint is enforced (can't have duplicate home/away players for fixture) |
| ✓ | Winner field is auto-populated correctly and is read-only |
| ✓ | Scores cannot be equal (draws not allowed) |
| ✓ | Scores must be consistent with best of 5 (at least one player must have 3 sets and more than 3 sets is not allowed) |
| ✓ | Players cannot play against themselves |
| ✓ | Players must be Team Players registered for that season |
| ✓ | Players must be Team Players from the same club (not just same team to allow for reserves) |
| ✓ | A SinglesMatch record can be updated and deleted in Django Admin |

### DoublesMatch Model

*Note: M2M field validation enforced through form clean() rather than model clean()*

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows DoublesMatch model under League app |
| ✓ | Doubles matches are listed with expected str representation (<home_player1> + <home_player2> <home_sets> vs <away_sets> <away_player1> + <away_player2> ) |
| ✓ | Doubles matches are listed according to order defined in FixtureResult model |
| ✓ | DoublesMatch model contains all expected fields |
| ✓ | Required fields display error messages when missing |
| ✓ | Winner field is auto-populated correctly and is read-only |
| ✓ | Unique constraint enforced (only one doubles match allowed per fixture result) |
| ✓ | Scores cannot be equal (draws not allowed) |
| ✓ | Scores must be consistent with best of 5 (at least one player must have 3 sets and more than 3 sets is not allowed) |
| ✓ | A player cannot play for both teams |
| ✓ | Each doubles team must have exactly 2 players |
| ✓ | All players must be Team Players registered for that season |
| ✓ | All players must be Team Players from the same club as the home/away team (not just same team to allow for reserves) |
| ✓ | A DoublesMatch record can be updated and deleted in Django Admin |

### SinglesGame Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows SinglesGame model under League app |
| ✓ | Singles games are listed with expected str representation (<home_player> vs <away_player>: Set <set_num>: <home_points>-<away_points>) |
| ✓ | Singles games are ordered by singles match then set number (ascending) |
| ✓ | SinglesGame model contains all expected fields |
| ✓ | Required fields display error messages when missing |
| ✓ | Unique constraint is enforced (can't have duplicate set number for singles match) |
| ✓ | Set number must be between 1 and 5 inclusive |
| ✓ | Winner field is auto-populated correctly and is read-only |
| ✓ | Scores cannot be equal (draws not allowed) |
| ✓ | At least one score must be greater than 10 points  |
| ✓ | Winning score must be at least 2 points higher and exactly 2 points higher if both scores greater than or equal to 10 points |
| ✓ | A SinglesGame record can be updated and deleted in Django Admin |

### DoublesGame Model

| Status  | Test Description |
| ---     | ---              |
| ✓ | Admin Panel shows DoublesGame model under League app |
| ✓ | Doubles games are listed with expected str representation (<home_team> vs <away_team>: Set <set_num>: <home_points>-<away_points>) |
| ✓ | Doubles games are ordered by doubles match then set number (ascending) |
| ✓ | DoublesGame model contains all expected fields |
| ✓ | Required fields display error messages when missing |
| ✓ | Unique constraint is enforced (can't have duplicate set number for doubles match) |
| ✓ | Set number must be between 1 and 5 inclusive |
| ✓ | Winner field is auto-populated correctly and is read-only |
| ✓ | Scores cannot be equal (draws not allowed) |
| ✓ | At least one score must be greater than 10 points  |
| ✓ | Winning score must be at least 2 points higher and exactly 2 points higher if both scores greater than or equal to 10 points |
| ✓ | A DoublesGame record can be updated and deleted in Django Admin |

## Common Page Elements

### Navbar

| Status  | Test Description |
| ---     | ---              |
| ✓ | No broken links |
| ✓ | Home nav item active on home page with aria-current correctly assigned |
| ✓ | Clubs nav item active on clubs page with aria-current correctly assigned |
| ✓ | Contact nav item active on contact page with aria-current correctly assigned |
| ✓ | For unauthenticated users, the User Profile dropdown menu shows "Login" and "Signup" items only which correctly navigate to their respective pages |
| ✓ | For authenticated users, the User Profile dropdown menu shows "Logout" and "Change Password" and "Account Settings" items only which correctly navigate to their respective pages |
| ✓ | The User Profile icon indicates that a user is logged in by changing colour |
| ✓ | If an authenticated user is also assigned as a club admin, they see a "Club Admin" link in the user dropdown menu |
| ✓ | The "Club Admin" link does not display for unauthenticated users or users that do not have club admin status |
| ✓ | The "Club Admin" link is styled consistently with other items in the nav dropdown menu |
| ✓ | Clicking the "Club Admin" link correctly takes the user to the club admin dashboard page |

### User Banner

| Status  | Test Description |
| ---     | ---              |
| ✓ | When a user is logged in, the user banner displays underneath the navbar to show which user is logged in |
| ✓ | When a user is not logged in, the user banner does not display |


### Footer

| Status  | Test Description |
| ---     | ---              |
| ✓ | Footer is responsive on different devices |
| ✓ | Hover effects are consistently themed and present when hovering mouse over all links |
| ✓ | Clicking social media icon navigates to external page and opens in a new tab |
| ✓ | Clicking Contact Us navigates to contact page |
| ✓ | No console errors or warnings were caused by interacting with footer elements |


## Website Pages

### Custom Error Pages

| Status  | Test Description |
| ---     | ---              |
| ✓ | When navigate to invalid url path, custom 404 page seen and HTTP 404 status returned |
| ✓ | When visit page without relevant permission (simulated using "raise PermissionDenied" in view), custom 403 page seen and HTTP 403 status returned |
| ✓ | When simulate server error (by requesting static resource without load static tag in template), custom 500 page seen and HTTP 500 status returned |

### Homepage

| Status  | Test Description |
| ---     | ---              |
| ✓ | Hero image and overlay display well on different screen sizes |
| ✓ | Hero image and overlay display for unauthenticated users |
| ✓ | About section shows correct content and displays well on different screen sizes |
| ✓ | About section displays for unauthenticated users |
| ✓ | News section shows all active news items rotating in a carousel |
| ✓ | Inactive news items do not display (expired, future) |
| ✓ | When no active news items, a placeholder message is shown instead of the carousel |
| ✓ | When only one active news item, carousel navigation buttons are hidden |
| ✓ | New news items immediately show on the homepage upon manual page refresh |
| ✓ | News items are visible without requiring login |
| ✓ | News section is responsive on different screen sizes |
| ✓ | Useful Links section contains cards which correctly link to Clubs, League Tables, Fixtures and Results pages |
| ✓ | FAQ section shows correct content and functionality |
| ✓ | FAQ section displays well on different screen sizes |
| ✓ | FAQ section displays for unauthenticated users |
| ✓ | Sponsors section shows logos for league sponsors in a flexible and responsive layout |
| ✓ | Clicking on sponsor logo navigates to the correct website |
| ✓ | Clicking on sponsor logo opens external website in a new browser tab |
| ✓ | Hovering over sponsor logo with a mouse shows the correct tooltip |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Contact Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | Contact Details section is responsive on different devices |
| ✓ | Clicking on email address opens default email client |
| ✓ | Clicking on phone number opens phone dialler (on mobile devices) |
| ✓ | Contact information is visible without requiring a login |
| ✓ | Enquiry form auto-populates email for authenticated users |
| ✓ | Enquiry form shows error message when required fields are not filled in |
| ✓ | Enquiry form shows error message when invalid phone number is given (not a UK region phone number) alongside a warning alert |
| ✓ | Enquiry form submits message successfully and can be viewed in the admin panel immediately upon page refresh |
| ✓ | A success alert message displays at the top of the page when the Enquiry form is submitted successfully |
| ✓ | On successful form submission, the Enquiry form is reset to empty (with auto populated email for authenticated users) |
| ✓ | On simulated server error upon form submission, user is directed to custom 500 error page |
| ✓ | Enquiry form is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Signup Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | Signup form only accessible to unauthenticated users (authenticated users are redirected to homepage) |
| ✓ | Signup form includes email, username, password and confirm password as required fields |
| ✓ | Signup form shows error message when required fields are not filled in |
| ✓ | Signup form shows error message when invalid email is given |
| ✓ | Signup form shows error message when email is not unique |
| ✓ | Signup form shows error message when username is not unique |
| ✓ | Signup form shows error message when password and confirm password fields are different |
| ✓ | Signup form creates a user in the database and can be viewed immediately in admin panel on page refresh |
| ✓ | Passwords are stored securely (hashed) and not visible as plain text in Django Admin Panel |
| ✓ | On successful form submission, a success alert message displays at the top of the page and the user is redirected to the homepage |
| ✓ | "Already have an account?" message present and link to login page works correctly |
| ✓ | Signup form is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Login Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | Login form only accessible to unauthenticated users (authenticated users are redirected to homepage) |
| ✓ | Login form includes username and password as required fields |
| ✓ | Login form shows error message when required fields are not filled in |
| ✓ | Login form shows error message when invalid username or password is given |
| ✓ | Password field is case sensitive |
| ✓ | On successful form submission, a success alert message displays at the top of the page, user is logged in and the user is redirected to the homepage |
| ✓ | If "Remember Me" checkbox not ticked, authenticated user is logged out when browser closes |
| ✓ | If "Remember Me" checkbox is ticked, authenticated user remains logged in for a time, even if browser is closed |
| ✓ | Forgotten password message present and Link to contact page works correctly |
| ✓ | Link to signup page is present and works correctly |
| ✓ | Login form is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Logout Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | Logout page contains correct message, Log Out button and Go Back button |
| ✓ | Clicking the logout button correctly logs out the user, shows success message and redirects user to the home page |
| ✓ | Clicking the Go Back button correctly takes user back to the previous page in browser history |
| ✓ | If there is no previous page (e.g. when browser is opened using logout link) the website does not crash when the Go Back button is clicked |
| ✓ | Unauthenticated users are redirected to the homepage |
| ✓ | Logout form is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Change Password Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | Change Password page contains form with correct fields (Current Password, New Password, New Password Again), Change Password button, Go Back button and "Forgot Password?" message with link |
| ✓ | Error messages show if any of the required fields are left blank |
| ✓ | Error message shows if current password is incorrect |
| ✓ | Error message shows if new passwords don't match |
| ✓ | Passwords are case sensitive |
| ✓ | For valid fields, clicking the Change Password button correctly changes the password, shows success message and redirects user to previous page |
| ✓ | Clicking the Go Back button correctly takes user back to the previous page in browser history |
| ✓ | If there is no previous page (e.g. when browser is opened using change password link) the website does not crash when the Go Back button or Change Password button is clicked (the user remains on the Change Password page) |
| ✓ | Clicking the link ("contact the league administrator") correctly takes the user to the contact page |
| ✓ | Unauthenticated users are redirected to the login page and return to the change password page after logging in |
| ✓ | Form is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Account Settings Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | When an unauthenticated user tries to access the Account Settings page, they are redirected to the login page and returned after successful login |
| ✓ | Account Settings page shows current email address and a link to a page for changing it (which correctly navigates the user) |
| ✓ | Account Settings page shows a Club Admin section for users which have club admin status but does not show otherwise |
| ✓ | Clicking the Drop Club Admin Status button correctly links to the Confirm Drop Club Admin Status page |
| ✓ | Account Settings page shows a section for deleting the user account and correctly links to the Confirm Account Deletion page |
| ✓ | Account Settings page is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Change Email Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | Change Email page contains title, form field labelled "New Email", Change Email button and Go Back button |
| ✓ | When an unauthenticated user tries to access the Change Email page, they are redirected to the login page and returned after successful login |
| ✓ | Clicking the Go Back button takes the user back to the Account Settings page |
| ✓ | Email Settings page shows current email address in the textbox by default |
| ✓ | Invalid email formats and blank entries show relevant error messages |
| ✓ | If email is not unique, a clear error message displays and the form will not update the email |
| ✓ | When users submit the same email address as the current one, they are directed back to the Account Settings page without errors |
| ✓ | When a valid email is submitted, the user's email is updated, a success message is displayed and the user is redirected to the Account Settings page |
| ✓ | The new email displays immediately on returning to the Account Settings page |
| ✓ | Emails are converted to lowercase by the form before saving to the database |
| ✓ | Change Email page is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Confirm Drop Club Admin Status Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | Confirm Drop Club Admin Status page contains title, explanatory comments and warnings, a confirmation checkbox, a Drop Club Admin Status button and a Cancel button |
| ✓ | When an unauthenticated user tries to access the page, they are redirected to the login page and returned after successful login |
| ✓ | Clicking the Cancel button takes the user back to the Account Settings page |
| ✓ | Drop Club Admin Status button is disabled by default and only becomes active when the confirm checkbox is ticked |
| ✓ | Clicking the Drop Club Admin Status button (when active) successfully removes club admin status from the user, redirects to the Account Settings page and shows a success message |
| ✓ | The ClubAdmin object no longer exists for the user after Dropping Club Admin Status and the Club Admin section no longer displays on the Account Settings page |
| ✓ | The club and venue information is unaffected by dropping club admin status and still displays on the clubs page |
| ✓ | The Confirm Drop Club Admin Status page is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |


### Confirm Account Deletion Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | Confirm Account Deletion page contains title, explanatory comments and warnings, a confirmation checkbox, a Delete Account button and a Cancel button |
| ✓ | When an unauthenticated user tries to access the Confirm Account Deletion page, they are redirected to the login page and returned after successful login |
| ✓ | Clicking the Cancel button takes the user back to the Account Settings page |
| ✓ | Delete Account button is disabled by default and only becomes active when the confirm checkbox is ticked |
| ✓ | Clicking the Delete Account button (when active) successfully deletes the user account, redirects to the homepage and shows a success message |
| ✓ | The user no longer shows in the database after account deletion and the user can no longer log into the account using their username and password (confirming the user has been deleted) |
| ✓ | If the user was assigned club admin status, the Club Admin object no longer exists for that user after the account has been deleted (as shown in Django Admin Panel) |
| ✓ | Only the account for the logged in user is deleted in the database |
| ✓ | Confirm Account Deletion page is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |


### Clubs Page - Club Listings

| Status  | Test Description |
| ---     | ---              |
| ✓ | The Clubs nav item is highlighted to indicate that it is the active page  |
| ✓ | A list of clubs is seen including Name, Review Data, Website Link (if given), Contact Name, Phone (if given), Email, Description, User Image (or placeholder image), Session information, Checkboxes for various features |
| ✓ | Clubs are listed in alphabetical order by name |
| ✓ | Only approved club information is shown on the page |
| ✓ | Clubs with no club information submitted do not show on the Clubs page |
| ✓ | Where there are multiple versions of the Club Information, only the most recently approved version is displayed |
| ✓ | If there are no approved clubs, a placeholder ("No clubs found.") is shown instead |
| ✓ | If the club does not have any approved reviews, a placeholder shows |
| ✓ | If the club does have approved reviews, the average star rating score and review count is shown, based on approved reviews only |
| ✓ | Clicking on the review information links to the club's dedicated reviews page |
| ✓ | If no website for the club is provided, no link to the website shows |
| ✓ | Clicking on a website link correctly navigates to the external webpage (if it exists) and it opens in a new browser tab |
| ✓ | Website links are styled consistently with other links on the website |
| ✓ | Clicking on email address opens default email client |
| ✓ | Clicking on phone number opens phone dialler (on mobile devices) |
| ✓ | Login not required to view the club information |
| ✓ | Page is responsive on different screen sizes |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Clubs Page - Venue Listings

| Status  | Test Description |
| ---     | ---              |
| ✓ | The venues for each club are displayed alongside other club information |
| ✓ | Venue information includes: Venue name, Street address, Address line 2 (optional - only shown if present), City, County, Postcode, Parking information, Number of tables |
| ✓ | The venue address is copyable |
| ✓ | Venues are listed in alphabetical order by name |
| ✓ | Only approved venue information is shown on the page |
| ✓ | Venues with no venue information attached do not show on the Clubs page |
| ✓ | Where there are multiple versions of the Venue Information, only the most recently approved version is displayed |
| ✓ | If a venue is shared by multiple clubs, it is shown multiple times (once for each club) |
| ✓ | If a club has multiple venues, all approved venues are displayed |
| ✓ | If there are no approved venues, a placeholder ("No venues are currently listed.") is shown instead |
| ✓ | Login not required to view the venue information |
| ✓ | Venues section is responsive on different screen sizes |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Clubs Page - Map

| Status  | Test Description |
| ---     | ---              |
| ✓ | The positions of approved venues are displayed as markers on the map but unapproved venues are not shown |
| ✓ | Hovering over markers shows the venue name and a prompt to click for more details |
| ✓ | When marker is clicked, an info window displays the venue name, address and clubs that use it |
| ✓ | If a venue is shared by multiple clubs, all relevant clubs are written |
| ✓ | Only venues attached to a club with at least one approved club info record are shown |
| ✓ | If there are no venue locations to display, a placeholder prompt ("No locations to display.") is displayed instead of the map |
| ✓ | The map dynamically centers and zooms so that all locations are shown |
| ✓ | Login not required to view the map |
| ✓ | Map is responsive on different screen sizes |
| ✓ | No console errors or warnings were caused by interacting with the map |

### Club Reviews Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | The Reviews page shows the name of the club, the average review score and number of reviews in the page header and data is based on approved reviews only |
| ✓ | The Reviews page lists all approved reviews for that club, showing star rating, headline, review text, the date it was last modified and the username for the user who posted it. |
| ✓ | Reviews are sorted by most recent first. |
| ✓ | Authenticated users who have not made a review see a button for creating a review which links to the Create Review Page |
| ✓ | Clicking the 'Write a review' button takes the user to the Create Club Review page |
| ✓ | Authenticated users who have made a review see their review above the others with buttons for updating or deleting their review |
| ✓ | Clicking the Update button takes the user to the Update Club Review page |
| ✓ | Clicking the Delete button takes the user to the Confirm Delete Club Review page |
| ✓ | If the authenticated user's review has not yet been approved, a message states this |
| ✓ | Unauthenticated users do not see buttons for creating, updating or deleting reviews |
| ✓ | No console errors or warnings were caused by interacting with the page |

### Create Club Review Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | The Create Club Review page redirects unauthenticated users to the login page and returns them to the page following successful login |
| ✓ | If an authenticated user who has already written a review for the specified club tries to access the page (by direct url), they are redirected to the Club Reviews page for that club with a warning message |
| ✓ | The Create Club Review page includes a form with required fields for a star rating (1 to 5), a headline and review text |
| ✓ | Form errors display for invalid forms |
| ✓ | On successful form submission, the user is redirected to the Club Reviews page, a success message is shown and the new review shows as awaiting approval. |
| ✓ | Once approved, the average club rating score and review count updates |
| ✓ | No console errors or warnings were caused by interacting with the page |

### Update Club Review Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | The Update Club Review page redirects unauthenticated users to the login page and returns them to the page following successful login |
| ✓ | If an authenticated user who has not yet written a review for the specified club tries to access the page (by direct url), they are redirected to the Club Reviews page for that club with a warning message |
| ✓ | The Update Club Review page includes a form with required fields for a star rating (1 to 5), a headline and review text and is pre-populated |
| ✓ | Form errors display for invalid forms |
| ✓ | On successful form submission, the user is redirected to the Club Reviews page, a success message is shown and the updated review shows as awaiting approval. |
| ✓ | If the previous review had been approved, the average club rating score and review count updates |
| ✓ | Once approved, the average club rating score and review count updates on the Clubs page and Club Reviews page |
| ✓ | No console errors or warnings were caused by interacting with the page |

### Confirm Delete Club Review Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | The Delete Club Review page redirects unauthenticated users to the login page and returns them to the page following successful login |
| ✓ | If an authenticated user who has not yet written a review for the specified club tries to access the page (by direct url), they are redirected to the Club Reviews page for that club with a warning message |
| ✓ | Clicking the cancel button takes users back to the Club Reviews page |
| ✓ | Clicking the delete button deletes the ClubReview record (verified in Django Admin), redirects the user to the Club Reviews page and shows a success message |
| ✓ | On successful deletion, the review does not show on the Club Reviews page and the average review score and review count is also updated |
| ✓ | If the review had been approved, the average club rating score and review count updates on the Clubs page and Club Reviews page |
| ✓ | No console errors or warnings were caused by interacting with the page |

### Club Admin Page - Managing Club and Venue Info

| Status  | Test Description |
| ---     | ---              |
| ✓ | If an unauthenticated user tries to access the Club Admin Dashboard (via direct url) they are redirected to the login page before another request to the dashboard page is made |
| ✓ | If an authenticated user without Club Admin status tries to access the Club Admin Dashboard (via direct url) they are directed to a custom 403 (Forbidden) page |
| ✓ | The Club Admin page includes a section for managing club and venue information |
| ✓ | The Club Admin page includes a section displaying the current status of information (missing, pending approval or approved) |
| ✓ | The Toggle Preview button correctly allows the user to toggle a view of the most recent data as it appears on the clubs page (or as it will appear when approved) |
| ✓ | If not all data is approved, a message is displayed above the preview to clarify that this is how the data will appear on the clubs page once approved |
| ✓ | The preview shows review summary data as a disabled link with muted text and hover effects to show it is disabled (also works after unassigning a venue) |
| ✓ | If no club information exists (even if venues have been assigned), the Toggle Preview button is not displayed and a status message displays "(Club Information REQUIRED)" with the red label |
| ✓ | If no venue has been assigned, a status message displays "(Venue REQUIRED)" with the red label |
| ✓ | If no venue information exists, a status message displays "(INFO REQUIRED)" with the red label |
| ✓ | If club information is not yet approved, the status message displays "(PENDING APPROVAL)" with the amber label |
| ✓ | If venue information is not yet approved, this is indicated with the amber label |
| ✓ | Hovering over the status labels shows an appropriate tooltip ("Missing club info", "Pending approval", "Missing venue info", "Approved" ) |
| ✓ | Clicking the Add Club Info or Edit Club Info buttons takes the user to the "Update Club Info" page |
| ✓ | Clicking the Assign Venue button takes the user to the "Assign Venue" page |
| ✓ | Clicking the Edit Venue Details button takes the user to the "Update Venue Info" page |
| ✓ | Clicking the Create New Venue button takes the user to the "Create Venue" page |
| ✓ | Clicking the Delete button next to a venue takes the user to the "Delete Venue" page |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Update Club Info Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | If an unauthenticated user tries to access the Update Club Info page (via direct url) they are redirected to the login page before another request to the page is made |
| ✓ | If an authenticated user without Club Admin status tries to access the Update Club Info page (via direct url) they are directed to a custom 403 (Forbidden) page |
| ✓ | The Update Club Info page includes a form and two buttons ("Update Club Info" and "Go Back") |
| ✓ | The form auto-populates with most recent ClubInfo record (if found) |
| ✓ | The form shows error message when required fields are not filled in |
| ✓ | The form shows error message when invalid email address is provided |
| ✓ | The form shows error message when invalid phone number is given (not a UK region phone number) alongside a warning alert |
| ✓ | The form submits Club Info successfully (including image upload) and can be viewed in the Django Admin Panel (upon page refresh) and Club Admin dashboard immediately |
| ✓ | Any outdated records are deleted from the ClubInfo database (as verified in the Django Admin Panel) |
| ✓ | A success alert message displays at the top of the page when the form is submitted successfully |
| ✓ | Club Admins can only update club information for the club they are assigned to |
| ✓ | Other links on the page work correctly (the "Cancel" button) |
| ✓ | The page is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Delete Club Info Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | If an unauthenticated user tries to access the Delete Club Info page (via direct url) they are redirected to the login page before another request to the page is made |
| ✓ | If an authenticated user without Club Admin status tries to access the Delete Club Info page (via direct url) they are directed to a custom 403 (Forbidden) page |
| ✓ | The Delete Club Info page includes a message warning that the action cannot be undone and a link to the Update Club Info page which correctly takes the user to that page when clicked |
| ✓ | The Delete Club Info page includes radio buttons to allow the user to choose whether to delete unapproved information only or delete approved information as well |
| ✓ | If the user chooses the option to delete all club info data (including approved version), a confirmation checkbox is displayed and the Delete Club Info button is disabled until they tick it |
| ✓ | Clicking the Delete Club Info button (when enabled) successfully deletes the requested info, displays a success message and returns the user to the Club Admin dashboard |
| ✓ | Deleted ClubInfo records no longer show in Django Admin panel (on page refresh) or in the Club Admin dashboard immediately |
| ✓ | If a user chooses to delete unapproved information only and no unapproved information exists, the user is returned to the Delete Club Info page and a warning message is displayed to alert the user that no action was taken |
| ✓ | Club Admins can only delete club information for the club they are assigned to |
| ✓ | Other links on the page work correctly including the "Cancel" button and the link to the Update Club Info page |
| ✓ | The page is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Assign Venue Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | If an unauthenticated user tries to access the Assign Venue page (via direct url) they are redirected to the login page before another request to the page is made |
| ✓ | If an authenticated user without Club Admin status tries to access the Assign Venue page (via direct url) they are directed to a custom 403 (Forbidden) page |
| ✓ | If there are no possible venues to assign (because they don't exist or are already assigned), the page shows a "There are no available venues to assign." message, a link to the Create Venue page and a button to return to the Club Admin page |
| ✓ | If there are possible venues to assign they are shown in a dropdown (venues which are already assigned are not shown) |
| ✓ | Choosing a venue and clicking the Assign Venue button correctly assigns the venue to the club (a new ClubVenue object is seen in Django Admin panel and it displays on Club Admin dashboard), the user is redirected back to the Club Admin dashboard and a confirmation message is seen |
| ✓ | The latitude and longitude fields are autopopulated correctly for valid postcodes |
| ✓ | Club Admins can only Assign Venues for the club they are assigned to |
| ✓ | Other links on the page work correctly including the "Cancel" button and the link to the "Create New Venue" page |
| ✓ | The page is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Update Venue Info Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | If an unauthenticated user tries to access the Update Venue page (via direct url) they are redirected to the login page before another request to the page is made |
| ✓ | If an authenticated user without Club Admin status tries to access the Update Venue page (via direct url) they are directed to a custom 403 (Forbidden) page |
| ✓ | If a user tries to edit venue information for a venue not assigned to their club, they are redirected to the Club Admin dashboard and a message "Unable to edit venue information." is displayed |
| ✓ | If venue is shared with another club, a message is displayed to inform the user that changes will also affect the information displayed for the other clubs as well |
| ✓ | If venue information exists, the most recent data is used to pre-fill the form |
| ✓ | When required fields are missing, appropriate validation errors are seen |
| ✓ | On successful form submission, the updated venue info appears in the admin panel (on page refresh) and the club admin dashboard, outdated records are deleted, the user is redirected to the Club Admin dashboard and a confirmation message displays |
| ✓ | The latitude and longitude fields are autopopulated correctly |
| ✓ | Updated venue information only displays on the Clubs page once approved by the league administrator |
| ✓ | Other links on the page work correctly including the "Cancel" button, the "Assign Venue" link and the "Create New Venue" link |
| ✓ | The page is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Create Venue Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | If an unauthenticated user tries to access the Create Venue page (via direct url) they are redirected to the login page before another request to the page is made |
| ✓ | If an authenticated user without Club Admin status tries to access the Create Venue page (via direct url) they are directed to a custom 403 (Forbidden) page |
| ✓ | The form includes fields for name, street_address, address_line2 (optional), city, county, postcode, num_tables, parking_info. |
| ✓ | Form validation errors show when missing required fields and duplicate venue name |
| ✓ | On successful form submission, the new venue and venue_info appears in the admin panel (on page refresh) and the club admin dashboard, the user is redirected to the Club Admin dashboard and a confirmation message displays |
| ✓ | Other links on the page work correctly (the "Cancel" button) |
| ✓ | The page is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Delete Venue Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | If an unauthenticated user tries to access the Delete Venue page (via direct url) they are redirected to the login page before another request to the page is made |
| ✓ | If an authenticated user without Club Admin status tries to access the Delete Venue page (via direct url) they are directed to a custom 403 (Forbidden) page |
| ✓ | A user can choose between deleting unapproved venue info or deleting the venue entirely |
| ✓ | If the venue is shared with another club, the second option is disabled and the page informs the user that the venue is shared |
| ✓ | If the user chooses to delete unapproved venue info and there is no unapproved venue info to delete, a message informs the user of this when the delete button is pressed |
| ✓ | If the user chooses to delete unapproved venue info and unapproved venue info exists, the unapproved venue info is deleted (as seen in Django Admin panel), the user is redirected to the club admin dashboard, a confirmation message displays and the new venue info status is reflected (either INFO REQUIRED or showing previously approved info) |
| ✓ | If the user chooses to delete the venue entirely, a confirmation checkbox appears and the Delete button is disabled until it is checked |
| ✓ | After ticking the confirmation checkbox and pressing the delete button, the venue is deleted (if not shared by other clubs) as verified by Django Admin panel, the user is redirected to the Club Admin page, a success message shows and the venue no longer appears in dropdowns for assigning a venue |
| ✓ | If the venue is protected (as a team's home venue), the second option (for deleting venue entirely) is disabled and an information box states that it is linked to a team's home venue |
| ✓ | Other links on the page work correctly including the "Cancel" button and the link to the Update Venue Information page |
| ✓ | The page is responsive across devices and themed consistently with the rest of the website |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Fixtures Page - Fixture Listings

| Status  | Test Description |
| ---     | ---              |
| ✓ | The League nav item is highlighted when the fixtures page is active  |
| ✓ | A list of Fixtures (grouped by week) is seen |
| ✓ | Weeks are listed in chronological order (earliest first) with week name, start date and details (if provided) |
| ✓ | Fixtures are listed within each week in chronological order (earliest first), by date and time |
| ✓ | Each fixture includes required information (home team, away team, date and time of fixture, a button for showing venue information) |
| ✓ | Fixtures are colour coded according to status and a key displays what the colours mean (when fixtures are present) |
| ✓ | If a week has no fixtures, a placeholder "No fixtures this week." is shown |
| ✓ | If no weeks are found, a placeholder "No weeks to display." is shown |
| ✓ | If season not found, a placeholder "Season not found." is shown |
| ✓ | If today's date is within one of the fixture weeks, a 'Jump to Current Week' link displays near the top of the page which navigates to fixtures for that week |
| ✓ | If today's date is not within one of the fixture weeks (e.g. out of season), the 'Jump to Current Week' link does not display |
| ✓ | Venue buttons are styled to look like links used elsewhere on the website and show tooltip when hovered |
| ✓ | Login not required to view the fixtures page |
| ✓ | Page is responsive on different screen sizes |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Fixtures Page - Venue Modal

| Status  | Test Description |
| ---     | ---              |
| ✓ | Clicking on venue opens the venue modal with venue information |
| ✓ | A loading spinner shows when retrieving venue information |
| ✓ | If venue not found, a placeholder "Venue not found" is shown |
| ✓ | If no approved venue information, a placeholder "No venue info available" is shown |
| ✓ | If venue info is available it displays correctly alongside the fixture description (Home vs Away) |
| ✓ | Login not required to view the venue-modal |
| ✓ | Modal is responsive on different screen sizes |
| ✓ | No console errors or warnings were caused by interacting with the modal |


### Fixtures Page - Filters Panel

| Status  | Test Description |
| ---     | ---              |
| ✓ | Clicking on filter button opens a filter panel |
| ✓ | Filter panel includes select boxes for season and division |
| ✓ | Filter panel includes buttons "Clear Filters" and "Apply Filters"  |
| ✓ | Only seasons with is_visible display in seasons dropdown |
| ✓ | Seasons are listed in reverse chronological order |
| ✓ | Current season is chosen as the default option |
| ✓ | The divisions dropdown shows divisions in rank order |
| ✓ | The divisions dropdown has a default value of "All Divisions" |
| ✓ | The Club dropdown shows clubs in alphabetical order and each club only appears once |
| ✓ | The Club dropdown has a default value of "All Clubs" |
| ✓ | The fixtures list updates correctly according to the selected filters when the "Apply Filters" button is pressed |
| ✓ | The fixtures list updates correctly when the "Clear Filters" button is pressed |
| ✓ | Changing the season updates the divisions dropdown options but changing the division does not reset the season |
| ✓ | Changing the season and/or division updates the clubs dropdown options but changing the club does not reset the season or division |
| ✓ | All filters work across devices and the layout is fully responsive |
| ✓ | No console errors or warnings were caused by interacting with the modal |

### Results Page - Result Listings

| Status  | Test Description |
| ---     | ---              |
| ✓ | The League nav item is highlighted when the Results page is active  |
| ✓ | A list of Results (grouped by week) is seen |
| ✓ | Weeks are listed in chronological order (latest first) with week name, start date and details (if provided) |
| ✓ | Results are listed within each week in chronological order (earliest first), by date and time |
| ✓ | Each Result includes required information (home team, away team, fixture date, score and a link ("score") to view match breakdown) |
| ✓ | Clicking the link navigates to the Result Breakdown page |
| ✓ | If a match was forfeited, the fixture result is coloured red and the text "FORFEITED" is displayed |
| ✓ | If no weeks are found with results, a placeholder "No results to display." is shown |
| ✓ | If season not found, a placeholder "Season not found." is shown |
| ✓ | Login not required to view the Results page |
| ✓ | Page is responsive on different screen sizes |
| ✓ | No console errors or warnings were caused by interacting with page elements |

### Results Page - Filters Panel

| Status  | Test Description |
| ---     | ---              |
| ✓ | Clicking on filter button opens a filter panel |
| ✓ | Filter panel includes select boxes for season, division and club |
| ✓ | Filter panel includes buttons "Clear Filters" and "Apply Filters"  |
| ✓ | Only seasons with is_visible display in seasons dropdown |
| ✓ | Seasons are listed in reverse chronological order |
| ✓ | Current season is chosen as the default option |
| ✓ | The divisions dropdown shows divisions in rank order |
| ✓ | The divisions dropdown has a default value of "All Divisions" |
| ✓ | The Club dropdown shows clubs in alphabetical order and each club only appears once |
| ✓ | The Club dropdown has a default value of "All Clubs" |
| ✓ | The fixtures list updates correctly according to the selected filters when the "Apply Filters" button is pressed |
| ✓ | The fixtures list updates correctly when the "Clear Filters" button is pressed |
| ✓ | Changing the season updates the divisions dropdown options but changing the division does not reset the season |
| ✓ | Changing the season and/or division updates the clubs dropdown options but changing the club does not reset the season or division |
| ✓ | All filters work across devices and the layout is fully responsive |
| ✓ | No console errors or warnings were caused by interacting with the modal |

### Result Breakdown Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | Match scores for singles and doubles matches are displayed |
| ✓ | Game scores for singles and doubles matches are displayed |
| ✓ | If there are no records for any singles matches and/or the doubles match (e.g. if forfeited), suitable placeholders are shown |
| ✓ | If there are no game score records for a singles and/or doubles match, suitable placeholders are shown |
| ✓ | A button to return to results page displays and works correctly |
| ✓ | The fixture date, time and venue are displayed |
| ✓ | A summary showing how many singles matches were won by each player is displayed |
| ✓ | Trying to access the page by direct URL for a fixture with no result redirects the user to the results page |
| ✓ | Page is responsive on different screen sizes |
| ✓ | No console errors or warnings were caused by interacting with the page |

### League Tables Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | Navbar includes Tables in League menu dropdown |
| ✓ | The page shows a table for each division in the current season (by default) |
| ✓ | Each table includes team name, matches played (P), Wins (W), Losses (L), Draws (D), Points (Pts) and Position (Rank) |
| ✓ | Teams are sorted by points (highest first); ties are broken using number of team match wins, then team sets, then individual sets |
| ✓ | If no data is available, suitable placeholders are displayed |
| ✓ | Tables are visible to all users without requiring login |
| ✓ | Page is responsive on different screen sizes |
| ✓ | No console errors or warnings were caused by interacting with the page |

### League Tables Page - Filter Panel

| Status  | Test Description |
| ---     | ---              |
| ✓ | A season filter is displayed and defaults to the current season |
| ✓ | Season filter is a dropdown listing all visible seasons and is sorted by start date (most recent first) |
| ✓ | Season data updates correctly when filter is applied |
| ✓ | Suitable placeholders show if no season data is available |
| ✓ | Filtering updates dynamically without requiring a full page reload |
| ✓ | Filter is responsive on different screen sizes |
| ✓ | No console errors or warnings were caused by interacting with the page |

### Team Summary Page

| Status  | Test Description |
| ---     | ---              |
| ✓ | Clicking on a team name in Fixtures, Results and League Tables pages navigates to the Team Summary page |
| ✓ | The Team Summary page includes summary details about the team including team name, club, season, division, and performance stats. |
| ✓ | The Team Summary page includes a list of players and reserves who have played for the team in the season with stats (matches played, wins and win percentage) |
| ✓ | Reserves are marked with "(RESERVE)". |
| ✓ | Players are sorted by percentage wins then win count.  |
| ✓ | If a player hasn't played matches yet, a zero value show for matches played but dashes are displayed for wins and percentage wins |
| ✓ | Team result are listed by week in chronological order  |
| ✓ | Details of team results include the opponent team (linked), venue (home/away, opens modal), result (win/loss/draw) and score |
| ✓ | If the team has not yet played any matches, the placeholder “No results to display” is shown  |
| ✓ | Upcoming fixtures are listed by week in chronological order |
| ✓ | Fixture details include week, date, opponent team (linked) and venue (opens modal with details) |
| ✓ | If the team has no upcoming fixtures, the placeholder “No upcoming fixtures” is shown |
| ✓ | Pressing the Go Back button navigates the user to the previous page |
| ✓ | Attempting to access the page by direct url for a non-existent team id redirects the user to the 404 page |
| ✓ | The page correctly shows data for teams within their particular season, not just current season teams |
| ✓ | Page is responsive on different screen sizes |
| ✓ | No login is required to view the page |
| ✓ | No console errors or warnings were caused by interacting with the page |

