# E-Learning Platform 📚

## Project Overview ✨

The **E-Learning Platform** is a comprehensive, interactive, and accessible environment for online education. The application is designed to be a one-stop solution for learners and instructors, offering a seamless and engaging educational experience. It supports a wide range of features, from secure user authentication and course management to real-time communication tools and AI-driven assistance. 🧑‍🎓

---

## Features 🚀

* **User Authentication:** A robust and secure system for user registration and login. 🔐
* **Personalized Dashboards:** Each user has a personalized dashboard to track their enrolled courses, monitor their learning progress, and manage their profile. 📈
* **Course Management:** Users can easily browse, search, and view detailed information on a wide variety of courses. 🎓
* **Interactive Lessons:** Engage with structured lessons and track progress to ensure a clear learning path.
* **Virtual Classrooms:** The platform facilitates live video streaming for real-time interaction between instructors and learners. This feature includes a real-time chat and file-sharing capabilities to enhance the collaborative learning environment. 👩‍🏫
* **AI-Driven Chatbot:** An integrated AI chatbot provides 24/7 support. It offers personalized learning assistance, answers frequently asked questions, and helps students navigate the platform efficiently. 🤖
* **Social Learning:** A real-time messaging feature allows students to connect, communicate with classmates, and form course-specific chat groups to foster a sense of community. 💬

---

## Technologies Used 💻

This project is built using a modern and efficient technology stack.

* **Backend:**
    * **Python:** The primary programming language for the application logic. 🐍
    * **Flask:** A lightweight and flexible micro-framework used to build the web application's backend. 🌐
* **Frontend:**
    * **HTML, CSS, JavaScript:** The standard trio for creating an interactive and responsive user interface. 🎨
* **Database:**
    * **SQLite:** Used as the default database for development and local testing. 💾
* **Libraries & Extensions:**
    * `Flask`, `Flask-SQLAlchemy`, `google-generativeai`, `Flask-SocketIO`, `requests`, `python-dotenv`

---

## Getting Started 🚀

Follow these steps to set up and run the E-Learning Platform on your local machine.

### Prerequisites ✅
* **Python 3.x:** Ensure you have Python 3 installed.
* **pip:** The Python package installer.

### Installation 🛠️

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/pmanikyalarao/E-Learning-Project.git
    cd E-Learning-Project
    ```
2.  **Set up your Google API Key:**
    * Create an `apikeys.py` file in the root directory of the project.
    * Inside the file, define a variable named `googleAPIKey` and assign your Google API key to it. Replace `YOUR_GOOGLE_API_KEY` with your actual key.
    ```python
    # apikeys.py
    googleAPIKey = "YOUR_GOOGLE_API_KEY"
    ```
    * **Note:** This key is essential for the AI-driven chatbot functionality. Without it, the chatbot will not work.
3.  **Configure email settings:**
    * Open the `myBlueprints/__init__.py` file.
    * Locate the `def createApp():` function.
    * In the email configuration section, replace `'YOUR MAIL ID TO SEND OTPS'` with your Gmail address and `'YOUR MAIL PASSWORD'` with your app-specific password.
    ```python
    # myBlueprints/__init__.py
    # ... other configurations
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'YOUR MAIL ID TO SEND OTPS'
    app.config['MAIL_PASSWORD'] = 'YOUR MAIL PASSWORD'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'YOUR MAIL ID TO SEND OTPS'
    # ... rest of the code
    ```
    * **Note:** You must use a **Gmail App Password** instead of your regular Gmail password. For security reasons, Google requires this for third-party applications. To generate an App Password, you need to have **2-Step Verification** enabled on your Google account. You can create one from your [Google Account security settings](https://myaccount.google.com/security).


4.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
    A **virtual environment** is a self-contained directory containing a specific Python interpreter and a set of libraries, allowing you to manage project dependencies independently. 

5.  **Activate the virtual environment:**
    * **On Windows:**
        ```bash
        venv\Scripts\activate
        ```
    * **On macOS and Linux:**
        ```bash
        source venv/bin/activate
        ```
6.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This command reads the `requirements.txt` file and installs all the necessary Python libraries.

---

### Running the Application ▶️

1.  **Initialize the database:**
    * The project uses Flask-SQLAlchemy. You need to create the database and tables before running the application.
    * With your virtual environment activated, open a Python shell in your terminal by typing `python`.
    * Then, run the following commands to create the database:
    ```python
    >>> from myBlueprints import db
    >>> from main import app
    >>> with app.app_context():
    ...     db.create_all()
    ...
    >>> exit()
    ```

2.  **Run the Flask application:**
    * First, you need to set the `FLASK_APP` environment variable to point to your main application file, which is `main.py`.

    * **On Windows:**
        ```bash
        set FLASK_APP=main.py
        flask run
        ```
    * **On macOS and Linux:**
        ```bash
        export FLASK_APP=main.py
        flask run
        ```
3.  **Access the application:**
    * Open your web browser and navigate to `http://127.0.0.1:5000`. You should see the application's homepage. 🎉

---

## Contribution 🤝

Contributions are welcome! If you have suggestions for new features, bug fixes, or improvements, please feel free to open an issue or submit a pull request.
