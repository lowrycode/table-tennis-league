# Personal Project Goals

In this fourth portfolio project I aim to develop a full-stack web application using Django which showcases my abilities to potential employers whilst meeting the assessment criteria for the project.

Through this project, I intend to showcase:

- a solid understanding of the MVC design pattern as implemented in Django
- the ability to build a secure user authentication system
- proficiency in designing and implementing relational databases using an ORM
- the ability to manipulate data into a well-presented format that is easily analysed by a target user
- familiarity with Test-Driven Development (TDD) practices
- a strong grasp of agile principles and methodologies
- an understanding of the concept and practical application of a Minimum Viable Product (MVP)

With its large and highly extensible scope, this project offers an ideal opportunity to demonstrate the principle of *Minimum Viable Product*. It will be essential to prioritise features according to those which deliver the most value to users because it will not be possible to finish all of the possible features within the allotted time.

I will use this project as an opportunity to practise using the features in GitHub Projects to implement an Agile approach to development. This will include:
- Using a Product Backlog to prioritise User Stories.
- Assigning User Stories to sprints using MoSCoW prioritisation.
- Monitoring progress through the use of Kanban boards.

I also intend to learn more about using TDD in the context of a Django project and to practice using this approach throughout development.

# Website Purpose

The home of City and District Table Tennis League - a fictional table tennis league based in York. The website will include information about
- local clubs
- league fixtures and results
- league tables
- results analysis (team stats, player stats)
- other useful league information

# Target Audience and User Personas

The website will have the following types of users:
- **Visitors:** who seek to learn about table tennis clubs and competitions available in the area 
- **League Players:** who want to view information about fixtures, results, tables, stats and submit match results
- **Club Admins:** who want to manage club information, players and teams
- **League Admin:** the overall website administrator who wants to assign fixtures, approve results, approve club information and manage user permissions 

# Intended Features and Stages of Development

Planning has been organised into 3 distinct stages. Each stage includes features based around a common theme.

**STAGE 1: Information and Contact**
- Website displays key information about the league.
- Users can submit an enquiry to the league secretary via a contact form.
- Users can view information about table tennis clubs in the region.
- Authenticated users can be assigned club admin status to manage club information (which is approved by the league secretary).

*This stage ensures that all of the key assessment criteria are met, including user authentication and CRUD functionality.*

**STAGE 2: Displaying League Data**
- Users can view fixtures, results, league tables, team stats and player stats.
- Authenticated users can link their account to a player to more quickly view information that relates directly to them (upcoming fixtures, recent results, etc.).

*This stage provides an opportunity for planning and implementing a relational database and also data analysis features.*

**STAGE 3: League Management**
- Authenticated users can be assigned permissions to submit match scores.
- Club Admins can manage club players and register teams in the league.
- League Administrator can set up league seasons through the website, rather than the Django admin panel, for a more streamlined experience (e.g. generating fixtures rather than relying on manual data entry).

*This stage provides an opportunity for demonstrating proficiency in problem solving and efficient, scalable design systems.*


# Planned Technologies

The main technologies I intend to use are:
- HTML
- CSS (Bootstrap)
- JS (possibly JQuery and DataTables)
- Python + Django
- Relational database (PostgreSQL)

I may use HTMX for updating page content using AJAX requests.

Python Libraries that I am likely to use (beyond the default Django packages) include:
- **django-allauth:** for simplifying user validation
- **django-phonenumber-field:** to provide phone number field support in Django models
- **phonenumbers:** for validating phone numbers in different regions
- **django-localflavor:** for validating postcodes in different regions
- **requests:** for making HTTP requests to Google GeoCode API on the server side
- **crispy-bootstrap5:** for adding Bootstrap styles to forms
- **cloudinary:** to integrate with Cloudinary's image storage system
- **gunicorn:** for running a web server in production
- **whitenoise:** for serving static files in production 

Other Technologies
- Google Maps API
- Google GeoCode API

# Project structure

The project will include the following apps:

- `home`: For things relating to the Homepage.
- `contact`: For things relating to the Contact page.
- `clubs`: For things relating to information about table tennis clubs.
- `useraccounts`: For functionality related to user authentication and account settings.
- `league`: For league specific information such as seasons, divisions, teams, fixtures, results, tables, stats etc.

# Entity Relationship Diagram

The database design is summarised in the diagram below, which includes Django ORM-specific details to support precise model planning.

![ERD diagram](images/erd-detailed.jpg)


# User Stories and the Agile Approach

User stories for each of the planned features have been written at this initial planning stage. The [**User Stories**](user_stories.md) document lists the user stories under their relevant **themes** and **epics**.

The [**Sprints Log**](sprint_log.md) document contains the implementation details of each user story, such as the story point estimations, acceptance criteria and development tasks. It also shows the MoSCoW prioritisation labels that were assigned to each user story in each particular sprint.

The user stories can also be viewed in the [**GitHub Project**](https://github.com/users/lowrycode/projects/10/views/1) linked to this repository.