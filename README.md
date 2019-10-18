# gbbo parsing and basic analytics
Parsing thegreatbritishbakeoff.co.uk for recipes and building database to be used for analytics

## Usage

raw look

    sqlitebrowser database.db

### Dependencies
This is built for Python3 on a Debian environment. Please make sure you have the following installed:

    python3
    pip3

To install required Python packages:

    make depends


### Generate database
To start crawling over the website and building the database, run:

    make

or

    python3 spiders.py

During the crawling metadata about each recipe will be printed to the console.


## TODO

- Add verbosity flag to control console output
