# USER STORIES

This document shows the user stories that were written during the initial planning stages. They have been categorised under **themes** and **epics**.

Some of these user stories, especially those relating to Phase 3 of development, were not added to the Product Backlog, and others were classed as "WON'T HAVE".

Some additional user stories were added later (e.g. for Bug Fixes).

The [**Sprints Log**](sprint_log.md) document contains more details about each user story, such as
- the **estimated story points**
- the **MoSCoW prioritisation** label assigned for particular sprints
- the **acceptance criteria**
- the **development tasks**


# THEME 0: PROJECT SETUP

## EPIC 0.1: Project Setup

- As a **user**, I can **experience consistent fonts, spacing, and colours across the site** so that **the interface feels professional and easy to navigate**.
- As a **developer**, I can **set up the Django project structure and initial database** so that **I can build and run the app locally**.
- As a **developer**, I can **create a shared base template with reusable layout components** so that **the site remains DRY, maintainable, and visually consistent across all pages**.
- As a **developer**, I can **deploy the Django application to Heroku** so that **the app is accessible online and can be tested in a live environment**.
- As a **developer**, I can **configure Cloudinary and use CloudinaryField for image storage** so that **the application can serve media files reliably in production**.
- As a **site visitor**, I can **see a custom 403 error page if I try to access something I'm not allowed to** so that **I understand the issue and can navigate to another part of the site**.
- As a **site visitor**, I can **see a friendly custom 404 error page when I visit a broken or non-existent link** so that **I know the page doesn't exist and can easily find my way back to the homepage**.
- As a **site visitor**, I can **see a friendly custom 500 error page if something goes wrong on the server** so that **I'm not shown a generic or confusing error and can easily navigate elsewhere**.

# THEME 1: Display of Public Information

## EPIC 1.1: Homepage and League Overview

- As a **site visitor**, I can **immediately recognise the purpose of the website through viewing an engaging hero image** so that **I can decide whether to keep browsing the website**.
- As a **site visitor**, I can **view general information about the league** so that **I understand what the league is about and how to join the league**.
- As a **site visitor**, I can **see news about the league** so that **I can keep up-to-date with any matters relating to the league**.
- As a **site visitor**, I can **see a section with useful links on the home page** so that **I can easily navigate to important areas of the site**.
- As a **site visitor**, I can **view a section for frequently asked questions** so that **I can find answers to the most common questions quickly**.
- As a **league sponsor**, I can **see our brand logo as a clickable link on the homepage** so that **my brand gains exposure to visitors and league participants**.

## EPIC 1.2: Contact Information Display

- As a **site visitor**, I can **navigate to the Contact page using the top navigation bar** so that **I can easily find contact information without needing to scroll to the footer**.
- As a **site visitor**, I can **easily find contact information for the league administrator** so that **I can contact them if I have any queries or requests**.

## EPIC 1.3: Clubs Directory

- As a **prospective player**, I can **view summary information about clubs near me** so that **I can decide which club to join**.
- As a **prospective player**, I can **click on a link to the club webpage** so that **I can find out more information about the club**.
- As a **prospective player**, I can **view club contact details** so that **I can contact the club to ask any questions**.
- As a **league player**, I can **view information about club venues** so that **I know where to go when playing a team at their venue**.
- As a **prospective player**, I can **filter the list of clubs based on specific criteria** so that **I can narrow down my options to clubs that meet my needs**.
- As a **prospective player**, I can **view the locations of club venues on a map** so that **I can easily find which clubs are closest to me**.

(ADDED LATER)

- As a **prospective player**, I can **view all reviews and ratings for a club** so that **I can make an informed decision about the club**.
- As a **logged-in user**, I can **submit a review with a star rating and comment for a club** so that **I can share my experience with others**.
- As a **logged-in user**, I can **update or delete my own club review** so that **I can update or remove my feedback if needed**.

## EPIC 1.4: League Fixtures

- As a **league player**, I can **view upcoming fixtures** so that **I know who, where, and when I'm playing**.
- As a **league player**, I can **view venue details from a fixture** so that **I know where it's being held**.
- As a **league player**, I can **filter fixtures by season** so that **I can view matches from a specific season**.
- As a **league player**, I can **filter fixtures by division** so that **I can easily find relevant matches**.
- As a **league player**, I can **filter fixtures by club** so that **I can quickly find matches involving a specific club**.
- As a **league player**, I can **filter fixtures by team** so that **I can easily see matches involving a specific team**.
- As a **fixtures page user**, I can **quickly jump to the current week's fixtures** so that **I don't have to scroll through past weeks manually**.

## EPIC 1.5: League Results

- As a **league player**, I can **view completed or forfeited match results** so that **I know the outcomes of recent matches**.
- As a **league player**, I can **click on a match score to view detailed drilldown scores** so that **I can see how the overall match result was achieved**.
- As a **league player**, I can **filter results by season** so that **I can view outcomes from a specific season**.
- As a **league player**, I can **filter results by division** so that **I can find relevant match outcomes more easily**.
- As a **league player**, I can **filter results by club** so that **I can quickly find outcomes involving a particular club**.
- As a **league player**, I can **filter results by team** so that **I can easily view matches for my team**.

## EPIC 1.6: League Tables

- As a **league player**, I can **view league tables** so that **I can see how teams are performing in the league**.
- As a **league player**, I can **filter league tables by season** so that **I can view standings from past or current seasons**.
- As a **league player**, I can **filter league tables by division** so that **I can quickly find a specific division's table**.

## EPIC 1.7: Team Stats

- As a **league player**, I can **view a team's summary page** so that **I can see details about their players, recent results, and upcoming fixtures**.

## EPIC 1.8: Player Stats

- As a **league player**, I can **view a player's summary page** so that **I can see their key stats and match history**.
- As a **league player**, I can **view player-level analysis** so that **I can analyse the past performance of myself or future opponents in the league and view player rankings**.

# Theme 2: User Communication

## EPIC 2.1: Contact Form

- As a **site visitor**, I can **submit an enquiry using a contact form** so that **I can ask questions or request help without needing to email directly**.
- As a **league admin**, I can **receive contact form submissions via the dashboard** so that **I can respond to users' enquiries promptly**.

## EPIC 2.2: Notification System

- As a **league admin**, I can **send custom notifications to specific users** so that **I can inform them of important updates or actions they need to take**.
- As a **logged-in user**, I can **view notifications sent to me** so that **I stay informed about league-related news or actions**.
- As a **logged-in user**, I can **mark notifications as read** so that **I can keep track of what I've already seen**.
- As a **logged-in user**, I can **view a history of past notifications** so that **I can refer back to old messages when needed**.

# Theme 3: User Authentication and Account Management

## EPIC 3.1: User Authentication

- As a **new user**, I can **register for an account using a username and password** so that **I can access member-only features and content**.
- As a **new user**, I can **receive a confirmation email after registering** so that **I can verify my email address and activate my account**.
- As a **registered user**, I can **log in using my username and password** so that **I can access secure and personalised content**.
- As a **logged-in user**, I can **log out of my account** so that **I can end my session securely**.
- As a **logged-in user**, I can **change my password** so that **I can keep my account secure**.
- As a **user**, I can **reset my password via a "forgot password" link** so that **I can regain access if I forget my login details**.

## EPIC 3.2: Manage Account Settings

- As a **registered user**, I can **visit my Account Settings page** so that **I can view / edit account details**.
- As a **registered user**, I can **view and update my email address from the Account Settings page** so that **I can keep my account information up to date**.
- As a **registered user**, I can **delete my account from the Account Settings page** so that **I can remove my login account when no longer needed**.
- As a **registered user**, I can **link my account to an existing player profile** so that **I can quickly view fixtures and results that are related to me**.
- As a **registered user**, I can **unlink my account from a player profile** so that **I can link to a different player profile if I accidentally linked to the wrong player**.
- As a **registered user**, I can **create a player profile if I don't have one** so that **I can participate in league activities as a player**.
- As a **player**, I can **edit my player profile** so that **I can keep my information up to date**.
- As a **registered user**, I can **request to be linked to a club** so that **I can participate as a player in a team for that club in the league**.
- As a **player**, I can **delete my player profile (if not linked to archived results)** so that **I can remove my profile if I don't end up playing in the league**.
- As a **registered player**, I can **request the removal or anonymisation of my personal data** so that **I can exercise my GDPR right to be forgotten**.
- As a **league administrator**, I can **anonymize or rename players who have left the league** so that **their historical data complies with GDPR regulations**.

# Theme 4: League Management

## EPIC 4.1: Manage Seasons and Divisions

- As a **league administrator**, I can **create, update, or delete divisions (if not linked to archived data)** so that **teams can be grouped appropriately based on skill level**.
- As a **league administrator**, I can **create and manage a season** so that **fixtures, divisions, and results can be organized independently from previous seasons**.
- As a **league administrator**, I can **create, update, or delete weeks (if not linked to archived data)** so that **each week in a season can be defined and referenced for fixtures and display**.

## EPIC 4.2: Manage Players and Teams

- As a **league administrator**, I can **create, update, or delete base player profiles** so that **player information is maintained centrally and stays consistent across seasons**.
- As a **league administrator**, I can **create, update, or delete TeamPlayer records** so that **season-specific details are tracked independently of general player information**.
- As a **league administrator**, I can **create, update, or delete Team records** so that **each team is correctly assigned to a division within a season**.
- As a **club administrator**, I can **view which players are eligible to act as reserves for a team** so that **I can select substitutes for upcoming fixtures while ensuring compliance with league rules**.

## EPIC 4.3: Manage Fixtures and Results

- As a **league administrator**, I can **create and update fixtures** so that **I can manage when and where matches take place and track their current status**.
- As a **league administrator**, I can **record and update fixture results** so that **match outcomes are accurately captured and reflected in the system**.
- As a **league administrator**, I can **record individual singles match scores for a fixture** so that **each fixture result is backed by detailed match data**.
- As a **league administrator**, I can **record doubles match scores for a fixture** so that **fixture results include complete information about doubles matches played**.
- As a **league administrator**, I can **record individual game scores for a singles match** so that **I can maintain detailed records of how each match was played**.
- As a **league administrator**, I can **record individual game scores for a doubles match** so that **I can track detailed performance of doubles teams across each set**.

# Theme 5: Club Management

## EPIC 5.1: Manage Club Information

- As a **club admin**, I can **see a "Club Admin" item in my profile dropdown menu that links to my club admin dashboard** so that **I can easily manage my club's details and admin tasks**.
- As a **club administrator**, I can **add information about my club** so that **it appears on the website once approved**.
- As a **club administrator**, I can **update my club's details** so that **the information stays current**.
- As a **club administrator**, I can **delete my club's information** so that **it's removed from the Clubs page**.
- As a **club administrator**, I can **assign an existing venue to my club** so that **it appears on the Clubs page**.
- As a **club administrator**, I can **unassign a venue** so that **it is no longer linked to my club**.
- As a **club administrator**, I can **create a new venue** so that **I can assign it to my club**.
- As a **club administrator**, I can **edit venue details (if only linked to my club)** so that **the venue information remains accurate**.
- As a **club administrator**, I can **delete a venue (if unlinked from clubs or history)** so that **it is permanently removed**.

## EPIC 5.2: Add/Remove/Approve Players in Club

- As a **club administrator**, I can **view a list of players who are currently registered with the club** so that **I can update the list if necessary**.
- As a **club administrator**, I can **add players to the club** so that **they can be assigned to teams and participate in league matches**.
- As a **club administrator**, I can **remove players from the club** so that **the list of club members stays current and accurate**.
- As a **club administrator**, I can **approve or reject requests from users to join the club members list** so that **only verified players are eligible to play for the club in the league**.
- As a **club administrator**, I can **view a list of players who have requested to join the club** so that **I can review and respond to their requests in a timely manner**.

## EPIC 5.3: Assign Players to Teams

- As a **club administrator**, I can **register players with specific teams in the club** so that **they are eligible to compete in team matches**.
- As a **club administrator**, I can **view a list of players assigned to each team in a particular season** so that **I can quickly check who is registered to play for each team**.

# Theme 6: Website Administration

## EPIC 6.1: Manage User Permissions

- As a **league administrator**, I can **assign or unassign club-admin permissions to individual users** so that **I can control who has permission to edit club information, manage team registrations and submit results for teams in their club**.
- As a **league administrator**, I can **assign or unassign permissions for entering match scores to individual users** so that **I can control who is able to submit match results for their team**.

## EPIC 6.2: Manage Dynamic Content (e.g. News Items)

- As a **league administrator**, I can **create and publish news posts on the homepage** so that **site visitors stay informed about league updates and announcements**.
- As a **league administrator**, I can **edit or delete existing news posts** so that **information stays relevant and outdated content can be removed**.
- As a **league administrator**, I can **schedule news items to be published at a future date** so that **announcements can be planned and timed in advance**.

# Theme 7: TECHNICAL QUALITY

## EPIC 7.1: Technical Quality

- As a **developer**, I can **view clear documentation and formatted code** so that **I can understand and maintain the project efficiently**.
- As a **QA**, I can **validate the codebase using code validation tools** so that **I can catch errors early and ensure code quality**.
- As a **tester**, I can **manually test website features** so that **I can ensure a smooth and bug-free experience for users**.




