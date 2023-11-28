# Running the "med adherence app" Django Project Locally

These instructions will guide you through setting up and running the "med adherence app" Django project on your local machine. Make sure you have Python and a code editor installed.

## Prerequisites

- [Python](https://www.python.org/downloads/)
- Code Editor (e.g., Visual Studio Code, PyCharm)

## Step 1:

1. Open your terminal.
2. Navigate to the directory of the project
` cd med_adherence_app`

## Step 2: Set Up a Virtual Environment

1. Create a virtual environment in the project directory:
` python -m venv myenv`
2. Activate the virtual environment:
- On Windows:

 ```
  myenv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source myenv/bin/activate
  ```

## Step 3: Install Dependencies

`pip install -r requirements.txt`

##  Step 4: Navigate to med adherence app directory

This is the directory that has the manage.py file

`cd med_adherence_app`


## Step 5: Run the Development Server

Start the Django development server:

`python manage.py runserver`

You should now be able to access the project by opening a web browser and navigating to `http://127.0.0.1:8000/`.

Now that the project is up and running, here are some instructions for using the "med_adherence_app" project:

### Login as an existing user

login as an existing user with these: 
- password : 
- email: 

### Registering New Users

1. Click on the "Register" button to register a new user.

2. Enter a unique username, a strong password, and a valid email address.

3. Click "Register" to create the new user account.


### Creating a New prescription 

1. Click on the "+" button to create a new prescription
2. add the name of the medication
3. form of the medication
4. what the medication is for
5. number of doses
6. how you want to take the med

### User Authentication

1. Click on the "Login" button to log in.

2. After logging in, you'll have access to create,update and delete your posts.

3. Click on the "Logout" button to log out.


### Editing Your med

1. To edit your med, click on the med you want to edit. You must be a logged in doctor/health worker to edit a patient's med.


That's it! You should now have a clear understanding of how to use the "med adherence" Django project and its key features.
