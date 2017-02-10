# watbooks

The only way to tell which textbooks are useful is to ask upper-years who have already taken the course. But there's no centralized platform to get that information in a summarized way... until now. Enter WatBooks, a very simple site that solves a BIG and EXPENSIVE problem.

Try it out at: http://watbooks.xin-xin.me


## Project Setup

```
git clone <url>
cd watbooks

# Create and enter a new virtual environment (requires virtualenv)
virtualenv venv
source venv/bin/activate

# Install Django and other Python dependencies
pip install -r requirements.txt

# Migrate DB and start Django server
python manage.py migrate
python manage.py runserver

# In a new terminal window:
cd ngApp

# Install NPM dependencies
npm install

# Start NPM, incl. TypeScript compiler
npm start

```

