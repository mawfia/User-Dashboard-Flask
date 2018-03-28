Coding Dojo (Python/Flask) - User Dashboard/Wall Assignment created 26 March 2018 and still under development

INTRODUCTION:
--------------------
This is a Flask/Python project being designed, built, and deployed to cloud services.

INTRO:
--------------------

-This application is an amalgamation between assignments User Dashboard and The Wall (mockups below) built as preparation for the Coding Dojo Belt exam, culminating 2 months of material including HTML, CSS, JavaScript, 
jQuery, Ajax, Python, Flask, Django and the various ways of using these technologies to develop a modern day application.  As the 
practice for a belt exam we spend no more than 48 hours from start and finsh for an application including testing and deployment with the following requirements:

1. Login and Registration that is displayed when the user navigates to the main URL. Validation errors should appear on each page with a form. Logout as well. Password should be at least 8 characters and not stored in plain text.
2. Display the logged users account information; also displays other users' accounts. Display should be specific per user.
3. Ability to view other users pages. Once the logged user joins they shoudl have access according to their permissions to update, delete or view messages on other users pages.
4. Display of a particular travel plan which also indicates the list of users who joined that plan.
5. You must be able to deploy your work to Amazon EC2 and provide the IP address or subdomain/domain name to where your work has been deployed.

![Image of Dashboard](http://mawfia.com/documents/user_dashboard.jpg)
![Image of Dashboard](http://mawfia.com/documents/flask_wall.png)


HOW TO USE:
---------------------
Choose login or register, to login in use username: "test@test.com" password: "1qazZAQ!", or register to create an account.  After logging in or registering you will see all trips from eveyone with an account.  You can choose to join a trip or create your own.


TECHNOLOGY USED:
-----------------
1.  Python 2.7 (upgraded to Python3.6.4) and MySQL were used for all back-end and data storage logic.

2.  A Virtual Environment was used to manage all module and library dependencies.

3.  CSS3 and HTML5 were used for initial form validation.

4.  MD5 (soon to be updated to SHA256) was used as a salt/hash algorithm to obsfuscate each user's password stored in MySQL.

5.  Flask, Blueperint, Nginx, and uWSGI were used for server deployment, routing, and execution with data and template client-side service requests handled with Jinja2 and JavaScript.

6.  The application is deployed on a AWS account for cloud services including Ubuntu configuration and management.

Current Maintainer:
 * M. Andrew Williams

This project has been sponsored by:
Coding Dojo

