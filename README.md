# Advanced Call Forwarding with Python, Flask, and Twilio

Learn how to use [Twilio](https://www.twilio.com) to forward a series of phone calls to your state senators.

## Local Development
This project is built using the [Flask](http://flask.pocoo.org/) web framework, and runs on Python 2.7+ and Python 3.4+

To run the app locally, follow these steps:
1. Clone this repository and `cd` into it.
2. Create a new virtual environment with [virtualenv](https://virtualenv.pypa.io/en/latest/):
    ```
    $ virtualenv venv
    $ source venv/bin/activate
    ```
3. Install the requirements:
```
$ pip install -r requirements.txt
```
4. Copy the .env_example file to .env, and edit it to match your configuration.
5. Run `source .env` to apply environment variables. Even better, use [autoenv](https://github.com/kennethreitz/autoenv).
6. Run the migrations:
```
$ python manage.py db upgrade
```
7. Seed the database with data:
```
$ python manage.py dbseed
```
```
$ python manage.py dbseed_zips
```
This will load senators.json into your SQLit database.
8. Expose your application to the internet using [ngrok](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html).
```
$ ngrok http 5000
```
Once you have started ngrok, update your TwiML application's voice URL setting to use your ngrok hostname. It will look something like this in your Twilio [console](https://www.twilio.com/console/phone-numbers/):
```
https://d06f533b.ngrok.io/callcongress/welcome
```
9. Start your development server:
```
$ python manage.py runserver
```
Once ngrok is running, open up your browser and go to your ngrok URL.


## Run the Tests
Run the tests locally with [coverage](http://coverage.readthedocs.org/):
```
coverage run manage.py test
```
You can then view the coverage results with `coverage report` or build an HTML report with `coverage html`.

*Note: If coverage seems to run way too many files, you can omit directories by adjusting your coverage command to something like `coverage run --omit=venv/* manage.py test`. See the [coverage docs](http://coverage.readthedocs.org/) for more information.*

## Meta
* No warranty expressed or implied. Software is as is. Diggity.
* [MIT License](https://opensource.org/licenses/mit-license.html)
* Lovingly crafted by Twilio Developer Education.
