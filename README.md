# FSND Capstone README

## Overview

This project is based on Udacity's Full Stack Web Developer Nanodegree (FSND) capstone project. The app is designed to demonstrate how to set up a local development environment and deploy the app to Heroku.

## Prerequisites

1. **Clone the Repository**  
   Begin by cloning the FSND repo, which contains the starter code.

   ```bash
   git clone "https://github.com/udacity/FSND.git"
   ```

2. **Install PostgreSQL**  
   To run the app locally, ensure that PostgreSQL is installed on your system, and the PostgreSQL server is up and running. Use the following commands to install and start PostgreSQL on Mac/Linux:

   ```bash
   # Install Postgres using Homebrew (for Mac)
   brew install postgresql
   
   # Verify the installation
   postgres --version
   
   # Start the Postgres server
   pg_ctl -D /usr/local/var/postgres start
   
   # Stop the Postgres server
   pg_ctl -D /usr/local/var/postgres stop
   ```

3. **Verify the PostgreSQL Database Setup**  
   After installation, you can verify your PostgreSQL setup by opening the `psql` prompt to view available roles and databases:

   ```bash
   psql [your_username]
   \du      # List available roles
   \list    # List available databases
   ```

   You can use the default PostgreSQL database (`postgres`) and a superuser role to create necessary tables later on.

## Running the App Locally

### 1. Set up the project directory
   In your terminal, create a new project directory, clone the repo, and copy the necessary files for the Heroku sample app:

   ```bash
   mkdir heroku_sample
   git clone https://github.com/udacity/FSND.git
   cp FSND/projects/capstone/heroku_sample/starter/Procfile heroku_sample/
   cp FSND/projects/capstone/heroku_sample/starter/*.py heroku_sample/
   cp FSND/projects/capstone/heroku_sample/starter/*.txt heroku_sample/
   cp FSND/projects/capstone/heroku_sample/starter/*.sh heroku_sample/
   ```

### 2. Create a Virtual Environment
   To keep your Python dependencies isolated, create a virtual environment:

   ```bash
   cd heroku_sample
   python3 -m venv myvenv
   source myvenv/bin/activate
   ```

### 3. Check Starter Files
   Your project directory should now contain the following key files to run the app:

   ```
   ├── app.py
   ├── models.py
   ├── requirements.txt
   └── setup.sh
   ```

   Additionally, for optional Heroku deployment, you may find:

   ```
   ├── Procfile
   ├── manage.py
   └── runtime.txt
   ```

### 4. Set Up Environment Variables
   Set up the environment variables by making `setup.sh` executable and running it:

   ```bash
   chmod +x setup.sh
   source setup.sh
   ```

   This script will set two environment variables:
   - `DATABASE_URL`: Points to your PostgreSQL database.
   - `EXCITED`: A sample variable used by the app.

   Verify the environment variables:

   ```bash
   echo $DATABASE_URL   # Should output something like postgresql://postgres@localhost:5432/postgres
   echo $EXCITED        # Should output "true"
   ```

   Adjust `DATABASE_URL` to match your local PostgreSQL configuration.

### 5. Install Dependencies
   Install the required Python dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

### 6. Run the Application
   Finally, start the application locally by running:

   ```bash
   python3 app.py
   ```

   Once the app starts, visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. If successful, you should see the message:

   ```
   Hello!!!!! You are doing great in this Udacity project.
   ```

## Troubleshooting (Mac Only)

If you encounter a "FATAL: role 'postgres' does not exist" error when trying to connect to PostgreSQL, it is likely due to Homebrew setting up the local PostgreSQL installation with a database superuser whose role name matches your login name. To resolve this, create the `postgres` role with superuser privileges:

```bash
/usr/local/Cellar/postgresql/14.1_1/bin/createuser -s postgres
```

## Additional Notes

- **Heroku Deployment**: This README focuses on setting up the app locally. For Heroku deployment, refer to the `Procfile`, `manage.py`, and `runtime.txt` files included in the project directory.
  
