# Data Management

This document outlines the limitations of using the Django Admin panel to manage project data and explains how to load sample data using fixtures.

# Notes on Django Admin Panel

It is assumed that only the League Administrator (i.e. the website administrator) would have access to the Django Admin panel.

The long-term goal for this project is to build a front-end dashboard that the League Administrator interacts with. This dashboard would summarise any actions that are needed across all the models, for example:
- managing news items for displaying on the homepage
- responding to enquiries
- creating new club records
- approving user-submitted information (e.g. club information, reviews and venue information)
- assigning club admin status to some users
- setting up season data (including a round-robin style fixture generator)
- registering players and teams to the league
- inputting match results

Therefore, the ultimate aim is to remove the need for the Django Admin panel completely and streamline the tasks that the League Administrator would want to do.

To enable the website administrator to manage the website in the meantime, the Django Admin panel is configured to display useful information from the list view (e.g. ClubInfo Approval status), record filtering and so on. However, the models were designed with data organisation and scalability in mind, not for streamlining data input through the Django Admin interface.

Using the Django Admin panel for some actions is quite time consuming and error prone. For example, when submitting one fixture result, the following models need populating
- `FixtureResult`: 1 record
- `SinglesMatch`: 9 records
- `DoublesMatch`: 1 record
- `SinglesGame`: between 3 and 5 records per `SinglesMatch`
- `DoublesGame`: between 3 and 5 records per `DoublesMatch`

Clearly this is quite labour intensive and it highlights the need for a front-end interface on the website to streamline this process. Stage 3 of the project development is largely focused around streamlining these actions.


## Django Admin Workflows

For some of the common tasks that a League Administrator would need to perform, it is perhaps unclear how these would be achieved using the Django Admin panel.Therefore, the following sections state how some of these tasks can be achieved.

### Approving User-Submitted Information

Numerous models have an `approved` field that needs updating from `False` to `True` before the information is displayed on the public facing webpages. This approach ensures that the league administrator has complete control over the content of the website.

The following models have an `approved` field:
- `ClubInfo`
- `VenueInfo`
- `ClubReview`
- `Team`

The approval status is displayed in the list view for all of these models and the records can also be filtered by approval status. To update the approval status, simply click on a record to view the form and update the status of the 'Approved' checkbox.

### Responding to User Enquiries

The Enquiry model has an `is_actioned` field to enable the League Administrator to see which enquiries have been dealt with. There is currently no way of communicating with other website users through the website itself so it is expected that the League Administrator would follow up any further communications through the email address provided.

*NOTE: the `email` field is a required field in the enquiry form.*

### Creating a Club and Assigning Club Admin Status

The Homepage (FAQs section) and Contact page (above the form) describe the process for registering a new club.

The workflow for the League Administrator is currently as follows:
1. After receiving communication from the person registering a new club (e.g. through the enquiry form), the League Admin would visit the club (to check it is legitimate).
2. Following the visit, they would create a new `Club` record (containing the name of the Club) and then a new `ClubAdmin` record (linking the website user to the new Club record).
    - *NOTE: The user will then see 'Club Admin' as an item in the User dropdown menu in the top navigation bar. Using the Club Admin Dashboard, the user can submit club and venue information*
3. Once club information and venue information has been provided by the user, the League Administrator can approve this information (as discussed above) to allow the new information to appear on the Clubs page

### Creating Season Data

To achieve this using the Django Admin panel, the following models should be populated in this order:
1. `Division`: only if all the required divisions do not already exist from previous seasons
2. `Season`: to include information about the season
3. `Week`: records need creating for each week that will contain a Fixture
4. `Team`: each `Team` record is specific to a particular season so new `Team` records will need creating for each season
5. `Player` and `TeamPlayer`: a `TeamPlayer` record is specific to a `Team` within a `Season` whereas a `Player` record represents a club player and allows a player to be linked to data from multiple seasons.
6. `Fixture`: Each team will play each other team in their division twice (once at home and once away)

### Recording Match Scores

To achieve this using the Django Admin panel, the following models should be populated in this order:
1. `FixtureResult`: gives the overall match score
2. `SinglesMatch`: if each team has 3 players and each player plays all the opposing players then 9 `SinglesMatch` records would need creating
3. `DoublesMatch`: there would be one doubles match per fixture
4. `SinglesGame`: if each singles match is best of 5, between 3 and 5 `SinglesGame` records would be needed for each `SinglesMatch`
5. `DoublesGame`: if the doubles match was also best of 5, between 3 and 5 `DoublesGame` records would be needed for the `DoublesMatch`


# Populating the Database with Sample Data

During development, ChatGPT was used to assist in generating sample JSON fixture data. These JSON files are included in the [**Fixtures folder**](fixtures/) to assist those who wish to experiment.

## Summary of Fixture Data

### 1_users.json

Loads 5 test users which are later used for linking to club reviews.

### 2_clubs_and_venues.json

Loads the following:
- 11 `Club` records with related `ClubInfo` records.
- 13 `Venue` records with related `VenueInfo` records.
- 20 `ClubVenue` records where Venue 6 and venue 12 are shared by 2 clubs each.

### 3_club_reviews.json

Loads 12 ClubReview records across 7 clubs (9 approved, 3 not approved).

*NOTE: The reviews are made by users 2 to 6 so these users must exist in the database before attempting to load this data.*

### 4_league_divisions_seasons_weeks.json

Loads 3 `Division` records and 3 `Season` records.
- 2 divisions are used across all seasons; 1 is unused (for testing).
- Seasons: 2022–23, 2023–24, 2024–25 (latest is marked as current).
- Each season includes 10 Week records (total 30 weeks), with every 5th and 10th week designated as catchup weeks (but still with matches).

### 5_players.json

Loads `Player` records, each assigned to a club.

### 6_teams.json

Loads 30 `Team` records.
- 10 teams per season, 5 teams in each division.

### 7_team_players.json

Loads `TeamPlayer` records for teams across the 3 seasons. Most teams have 3 players.

### 8_fixtures_seasonX.json

Loads `Fixture` records where each team plays each other team in their division twice (once at home, once away).
- 10 teams per season, 5 teams per division.

### 9_fixture_results_seasonX.json

Loads `FixtureResult` records for each fixture which summarise the overall match score
- The current season does not have FixtureResults for all matches to simulate a season that is still in progress.

### 10_singles_doubles_matches_season3.json

Loads `SinglesMatch` and `DoublesMatch` records for `FixtureResult` records in the current season.

### 11_singles_doubles_games_season3.json

Loads `SinglesGame` and `DoublesGame` records for `SinglesMatch` and `DoublesMatch` records in the current season.

## Deleting Existing Database Data

The quickest way to delete existing data from the database is from the command line using the Django shell utility. 

In a terminal window:
1. Navigate to the project root directory and type `python manage.py shell`.
2. Copy the following python code to delete the data from the specified models.

```python
## LEAGUE DATA
from league.models import Division, Season, Week, Team, Player, TeamPlayer, Fixture
Fixture.objects.all().delete()
TeamPlayer.objects.all().delete()
Team.objects.all().delete()
Week.objects.all().delete()
Season.objects.all().delete()
Player.objects.all().delete()
Division.objects.all().delete()

## CLUBS AND VENUES
from clubs.models import ClubAdmin, ClubVenue, VenueInfo, Venue, ClubReview, ClubInfo, Club 
ClubAdmin.objects.all().delete()
ClubVenue.objects.all().delete()
VenueInfo.objects.all().delete()
Venue.objects.all().delete()
ClubReview.objects.all().delete()
ClubInfo.objects.all().delete()
Club.objects.all().delete()

## ALL USERS (including super user)
from django.contrib.auth.models import User
User.objects.exclude(username='superuser').delete()
```

3. Exit the shell utility by typing `exit()`.

*NOTE: The order in which data is deleted is important due to protected field constraints within the models.*

*NOTE: The superuser is not deleted in the above code. It is assumed that the superuser is the first user in the database with a primary key of 1. The superuser MUST NOT have a primary key value between 2 and 6.*

*NOTE: The `NewsItem` and `Enquiry` models are not deleted in the above code.*

## Loading Fixture Data

To load the fixture data from the terminal
1. Navigate to the project root directory.
2. Copy the relevant lines from the code below.

```bash
python manage.py loaddata readme-resources/fixtures/1_users.json
python manage.py loaddata readme-resources/fixtures/2_clubs_and_venues.json
python manage.py loaddata readme-resources/fixtures/3_club_reviews.json
python manage.py loaddata readme-resources/fixtures/4_league_divisions_seasons_weeks.json
python manage.py loaddata readme-resources/fixtures/5_players.json
python manage.py loaddata readme-resources/fixtures/6_teams.json
python manage.py loaddata readme-resources/fixtures/7_team_players.json
python manage.py loaddata readme-resources/fixtures/8_fixtures_season1.json
python manage.py loaddata readme-resources/fixtures/8_fixtures_season2.json
python manage.py loaddata readme-resources/fixtures/8_fixtures_season3.json
python manage.py loaddata readme-resources/fixtures/9_fixture_results_season1.json
python manage.py loaddata readme-resources/fixtures/9_fixture_results_season2.json
python manage.py loaddata readme-resources/fixtures/9_fixture_results_season3.json
python manage.py loaddata readme-resources/fixtures/10_singles_doubles_matches_season3.json
python manage.py loaddata readme-resources/fixtures/11_singles_doubles_games_season3.json

```

*NOTE: Later fixtures rely on earlier ones so load the data in the order specified above.*