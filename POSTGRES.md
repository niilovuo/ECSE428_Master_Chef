# Setting up PostgreSQL

## Linux

First install postgresql:

On Ubuntu, ```sudo apt install postgresql```, Arch, ```sudo pacman -S postgresql```, etc..

On Linux, postgres runs as a service under its own user. Start the service with ```sudo service postgresql start```, then access the service with ```sudo -u postgres psql```. This will open an interactive command prompt where you can modify the postgres instance you are running locally. First, set the password to access this database with ```\password postgres```, and enter a password (for example, postgres will be used here).

## Windows

You may wish to use [WSL](https://docs.microsoft.com/en-us/windows/wsl/install), as windows command line is pretty gross in general.

If not, download PSQL through [the installer](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads); this will prompt you to enter a password (for example, postgres will be used here), and then a port (5432 is the default).

You should then be able to access SQL Shell (psql) from the start menu; open this app, it will prompt you to enter info such as server, database, etc.. Just press enter to accept the default values (in square brackets, will be the values you set in app setup). Then you will be prompted to enter your password, and you will find yourself in an interactive command prompt. You can change the password with ```\password postgres```, if you desire.

## Mac

Using [homebrew](https://brew.sh/), install with ```brew install postgresql@14```

# Creating the PostgreSQL database

In the psql shell, create a database for our grocery system: ```CREATE DATABASE my_database_name;```. You can verify this database has been created with ```\l```. Use ```\q``` to exit psql. my_database_name will need to be specified in the corresponding enviornment value as well.

# Configuring the app to run with PostgreSQL

See README.md