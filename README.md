# CS50-Web-Projects
This repository contains my code for all of my projects for CS50 Web, along with videos demonstrating them.

### About CS50 Web
CS50’s Web Programming with Python and JavaScript is a free, online web development course offered by Harvard.  According to their [welcome page](https://cs50.harvard.edu/web/2020/),
> This course picks up where [CS50x](https://cs50.harvard.edu/x/2022/) leaves off, diving more deeply into the design and implementation of web apps with Python, JavaScript, and SQL using frameworks like Django, React, and Bootstrap. Topics include database design, scalability, security, and user experience. Through hands-on projects, students learn to write and use APIs, create interactive UIs, and leverage cloud services like GitHub and Heroku. By semester’s end, students emerge with knowledge and experience in principles, languages, and tools that empower them to design and deploy applications on the Internet.

### Repository Structure
I am currently independetly working through this course.  The following are the projects in the course:
- [Project 0: Search](https://cs50.harvard.edu/web/2020/projects/0/search/) - A replica of Google's regular, iamge, and advanced searches using pure HTML and CSS.
- [Project 1: Wiki](https://cs50.harvard.edu/web/2020/projects/1/wiki/) - A django web app simulating a wiki where people can search for pages, edit wiki pages, or create new ones.
- [Project 2: Commerce](https://cs50.harvard.edu/web/2020/projects/2/commerce/) - A django web app meant to model eBay on which users can post listings, bid, comment on listings, and close/win active listings.
- [Project 3: Mail](https://cs50.harvard.edu/web/2020/projects/3/mail/) - A single page application for an email service implemented with a given API and pure JavaScript where users can send, reply to, and archive emails.
- [Project 4: Network](https://cs50.harvard.edu/web/2020/projects/4/network/) - A web app for a sample social media platform on which users can view, make, and like posts in a paginated view along with following other users and viewing their posts.
- [Final Project](https://cs50.harvard.edu/web/2020/projects/final/capstone/) - A flexible final project combining all of the aspects taught in this course.

As I work through the course, I will be adding my files for each project in this repository.  Each folder contains a README file with information about the project, a link to the assignment page, a description of what I contributed from the initial distribution code, and a link to a video demonstrating the app in action.

**Current Status:**  Working on Project 4

### Running the Projects
If you wish to download and run the projects yourself, you must have Python and Django installed for all projects except Project 0.  Note that Django is simply a Python library and can be downloaded with pip as with any other Python library.  Once you have these installed and have navigated to the directory with the files for the given project, execute the following commands:
```
python manage.py makemigrations [INSERT NAME OF FOLDER WITH templates FOLDER]
python manage.py migrate
python manage.py runserver
```
Note: for Project 1, you **do not** have to run the first two commands, only the third one.
