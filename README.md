# MedRecords
## Sebastian Presno Alvarado
### Video Demo:  <https://youtu.be/jTa_rNhH0cA>
### General idea: Web Application created for the medical area (specifically the Pathology field), designed to make it easier for staff to register patients plus search and save valuable information easily with a relational database (SQL). Created using Python, Flask, Jinja Templating, HTML, JavaScript, and CSS.
### Context:
I created this web application having in mind my parent's business. Both of them are doctors and own a private laboratory focused on **Oncological Pathology**. Pathology is the area focused on diagnosis, they make the necessary studies to determine if a patient has diseases such as cancer.

 Throughout the years I've seen them register their patients in an old-fashioned way (just recently they started using Excel). Therefore, with what I learned through the CS50 course, I decided to focus my final project on improving **Patient Recording**  in the pathology laboratory.

 Having medical records' data easily accessible can make any medical business' life easier. In case of clarification, a patient can easily be found as well as the date of study or doctor who attended the patient originally. Also, during any legal process, a record can be easily accessed and avoid further problems for the company. ***NAME*** solves both of these situations in a user-friendly way. It's important to mention that this idea can be implemented into ANY medical business with minor changes/adaptations. I decided to focus on pathology since it is the area I feel more acquainted. Having this in mind, I decided to start working on my project.
### Implementation Details
#### Database
The first thing I did was create my database called `pathology.db`. This works as a Relational database with 3 tables: `users, doctors, AND pathology`. The pathology table **references** the "doctors" table and the "users" table is used to register the users who have access to the system as well as their *hashed* passwords (created with a Python function from the library *werkzeug.security*).
Here is the diagram that explains how the tables are related as well as the attributes of each table:
![relational_model](https://github.com/presno2112/MedRecords/blob/main/screenshots/database.png)

#### Templates
Afterwards, I created my `/templates` folder inside my project. Which was composed of all of the HTML files that were going to be accessed in each of my routes. `/templates` has 9 HTML files in total, each of which will be explained in the following segment:

- `layout.html`: The skeleton of the whole web application. It contains a ***navbar*** with some *jinja* logic which displays different elements in which the user can navigate. The *jinja* logic helps display **LogIn** and **Register** if the user is not logged in, and in case the user is logged in, it displays 4 options: **Patients, Doctors, Search**(which is a dropdown menu divided into Search By Name, Search by Doctor and Search By Date) and finally the **Log Out** option. This layout will be *extended* onto every other HTML file with *jinja* so that only the body can be modified and every option can be accessed at all times. At the bottom, there's a small footer that contains developer information.
![layout](https://github.com/presno2112/MedRecords/blob/main/screenshots/layout_screenshot.png)
- `login.html`: The login page consists of a form with 2 inputs, a text input where the username needs to be the input, and a password input where the user types its password. If the input is correct, it queries the database and gets the user and password, and if they match, logs the user in automatically and allows them to use the app's functions. It looks like this:
![login](https://github.com/presno2112/MedRecords/blob/main/screenshots/login_screenshot.png)
- `register.html`: The template is almost identical to `login.html`, only that it contains a form with 3 inputs: a username input, and two password inputs which means the input will be censored with "*" (one of them sets the password and the second one is used to confirm the password). If the passwords don't match **or** the username is already in existence, a *flash alert* is displayed. If the input is correct, it inserts the data into the database and immediately logs the user in. Here's how it looks:
![register](https://github.com/presno2112/MedRecords/blob/main/screenshots/register_screenshot.png)
- `index.html`: This template is the first thing the user sees when they log in or register. It's quite simple, it only displays a *welcome* message and a table of the most recent studies that have been registered. This table is created with Jinja Templating, using a loop that iterates through every element of a **SQL** query containing every study made throughout time. The table shows the doctor's name, the patient's name, their email, the study type with its price, and the date it was registered.
![index](https://github.com/presno2112/MedRecords/blob/main/screenshots/index_screenshot.png)
- `doctors.html`: "Doctors.html" is the file used to POST a new doctor into the database. In the pathological field, other medical specialties are extremely important as every surgical procedure made by any doctor **MUST** be studied by a pathologist to verify everything's in order, which is why the database is designed to consider every patient but also, which doctor gave them treatment originally. The template consists of a form with two inputs, the doctor's name and their medical specialty, which to avoid user misinput, are already pre-defined and displayed to the user as a SELECT type of input. This function allows the database to have more standardized insertions. And finally, a Submit Button that triggers the insertion into the database as long as the input data is correct.
![doctors](https://github.com/presno2112/MedRecords/blob/main/screenshots/doctors_screenshot.png)
- `patients.html`: This is used to register a new medical study into the database. It takes, in a form the input for the doctor's name(Already listed in a select input, which accesses the "doctors" table in the database so it keeps updating), the patient's name and email, and the type of study. All of this with a submit button at the bottom that triggers the insertion of data into the database, registering the new study.
- `search_date.html`: The search files all work quite in the same way. In this case, the template has a **date** input which dynamically displays a table just like in `index.html` without the need of refreshing the page. With some ***JavaScript*** and a *** JSON *** format of data, the *innerHTML* of the table's body is modified so that its value is updated depending on the user's input.
![search_date](https://github.com/presno2112/MedRecords/blob/main/screenshots/search_nameScreenshot.png)
- `search_doctor.html`: Similar to the last template, *`search_doctor.html`* has a text input which, again, using ***JavaScript*** and a *** JSON *** format of data, updates the contents of the table (modifying the innerHTML) according to what the user types in. It looks like this initially:
![search_doctor1](https://github.com/presno2112/MedRecords/blob/main/screenshots/search_doctor1SS.png) Now if the user types **ANY letter**, as long as it is inside the name of any of the doctors, the data will change dynamically: ![search_doctor2](https://github.com/presno2112/MedRecords/blob/main/screenshots/search_doctor2SS.png)
- `search_name.html`: This works exactly like `search_doctor.html`, only instead of making a query based on the doctor's name, it takes the **patient's name** and updates the innerHTML of the table. ***JavaScript*** and ***JSON*** are both used just as in the other search templates. It looks like this:
![search_name1](https://github.com/presno2112/MedRecords/blob/main/screenshots/search_name1SS.png) As the user types any letter, the table gets updated like this: ![search_name2](https://github.com/presno2112/MedRecords/blob/main/screenshots/search_name2SS.png)

#### Design decisions
Taking into account that my project is focused on the medical area, I decided to style it with blue tonalities so it resembles the area it belongs to. I created a `/static` folder which contains my `styles.css` file and a `favicon.ico` icon of a **microscope** which I used as the app's icon so it looks like this:

![microscope](https://github.com/presno2112/MedRecords/blob/main/screenshots/tab_view.png)

#### BackEnd functionality
The backend functionality is made using Flask in Python. The Python code is divided into two files:
- `app.py`: Establishes the necessary routes for the application to work properly. **ALMOST** every route works with both a **POST** and a **GET** method (with the exception of `/index`,`/search_name`,`/search_date` and `/search_doctor` which only *display* data exclusively through the **GET** method). The **POST** method is mainly used to insert data into the database, obtaining data from the form using the function `request.form.get()`. I made completely sure that every single input is filled in before *posting*. In fact, if the user were to misinput, *flash* error messages appear on the screen. Finally, with the **GET** method we can render our template and connect variables between python and the HTML file. This file contains the **whole functionality** of the application.
- `functions.py`: Simply contains the function `login_required()` which is imported into `app.py` and helps us ensure that certain routes are only available to the user if they're logged in.
#### Final thoughts
**MedRecords** is meant to have a positive impact in the medical area. While it was made having in mind the *pathological field*, it can certainly be applied to any field with adequate modifications. Keeping patients' information safe and easily accessible is necessary and if done properly, can prevent potential lawsuits and provide easier access to information, which is exactly what **MedRecords** is designed to achieve.

#### ---------------created by Sebastián Presno Alvarado----------------
