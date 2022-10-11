# ECSE428 Master Chef (Group 1)

## Project for ECSE 428 - Software Engineering Practice

Forum website to share recipes and other cooking related things

| Name | ID |
|---|---|
| Ruoli Wang | 260833864 |
| Sia Ham | 260924883 |
| Tyler Syme | 260929186 |
| Zheyan Tu | 260828963 |
| Ben Mwaniki | 260772709 |
| Sandy Lao | 260925318 |
| Theodore Peters | 260919785 |
| Paul Teng | 260862906 |
| Niilo Vuokila | 260926706 |
| Jasmine Cheung | 260985168 |
| Filip Piekarek | 260805461 |

## Setting up the environment

### Prerequisites

Python 3
Postgres 14 (can be remote, but access is necessary)

### Steps

1.  Clone the repo and navigate into the repo directory
2.  Create a Python virtual environment (***optional, but good idea***)

```sh
python3 -m venv venv
```

3.  Activate the venv

```sh
source venv/bin/activate    # for linux or mac
venv\Scripts\activate.bat   # for cmd.exe
venv\Scripts\Activate.ps1   # for powershell
```

4.  Install the dependencies

```sh
pip3 install -r requirements.txt
```

At this point, you are ready to [run the app](#running-the-app).

As a side note,
to exit / deactivate the venv, do

```sh
deactivate
```

## Running the app

Once the environment is setup, you can start the app:

```sh
python3 app.py
```

### Configuration

Parts of the app's behavior must / can be configured via environment variables

| Variable setup | Purpose |
|--------------|---------|
| `DEBUG=true`   | Run in debug mode (which, among other things, means the app will automatically load changes to the code without needing to be rerun) |
| `POSTGRES_USER=...` | Credentials for postgres server, replace `...` with the actual username, defaults to `postgres` |
| `POSTGRES_PASSWORD=...` | Credentials for postgres server, replace `...` with the actual password, ***you need to supply it*** |
| `POSTGRES_DB=...` | Database name for the postgres server, replace `...` with the actual name, defaults to the username before |
| `POSTGRES_HOST=...` | Host of the postgres server, replace `...` with the actual host, defaults to `localhost` |
| `POSTGRES_PORT=...` | Port of the postgres server, replace `...` with the actual port, defaults to `5432` |

