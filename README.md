# solid-learnination

## Roster: Jiayang Chen, Jabir Chowdhury, Puneet Johal, Mai Rachlevsky

P02: The End

## Description
Always Be A Good Sport is a website to check your favorite team's statistics and schedule. By using the MySportsFeeds API, we are able to provide stats from the NBA, NFL, NHL, and MLB for the user. Users can save their favorite teams and see their schedules from the homepage. In the individual stat-sheets for specific games, we allow user interactivity, like organizing the table by a certain header, by using JavaScript. 

## How To Run

**Note:** These instructions need to be followed 1-2 days before actually using the website because you need to wait for the MySportsFeeds developers to NON-commercialize your key for free usage.
1. Clone this repository:
```
$ git clone https://github.com/jiayang/solid-learnination.git
```

2. Go into the repository's directory:
```
$ cd solid-learnination
```

3. Activate your virtual environment. 
```
$ source path/to/virtual/env/bin/activate #For Linux/OS
$ source path\to\virtual\env\Scripts\activate #For Windows
```

4. In your virtual environment, install the dependencies:
```
$ pip install -r requirements.txt
```

5. Procure API keys for the APIs listed by following the instructions [below](https://github.com/jiayang/solid-learnination#apis).

6. Change the `keys.json` file in the /data by adding your API keys as shown below:
```
{
  "mysportsfeeds" : "<INSERT_YOUR_API_KEY>",
  "msf_password" : "<YOUR_MYSPORTSFEEDS_ACCOUNT_PASSWORD>"
}
```

7. Now, run the python file to start the Flask server:
```
$ python app.py
```

8. Open your favorite web browser enter `localhost:5000` into the URL.

9. To terminate the server, press CTRL + C.

## APIs
- MySportsFeeds API
     - Procure an API key [here](https://www.mysportsfeeds.com/). 
     	* Create your account and click new API key. 
       		* **IMPORTANT** Your MySportsFeeds account password will be used to make API calls (because free keys only have access to v1.0) so use a password different from your other private passwords.
      	* Go to [Contact US](https://www.mysportsfeeds.com/contact-us) and state that the API key will be used only for a project and will be NON-commercial
     		* **IMPORTANT**: Now, you will have to wait 1-2 days for a response in your email, that your key has been NON-commercialized
      	* In your profile page on the website, open the dropdown for your key.
     	* Add **Limited POST-game access** subscriptions to the NBA, NFL, NHL, MLB to your key.
     - Use API key to request information from API.
     - The API retrieves postgame statistics from the four different leagues and returns it as a JSON.
     - We used this API as the backbone of our website, to provide every stat.

## Dependencies
- urllib
     - The `urllib` library was used to get the JSON files. This library is a standard Python library, so no action needed.
- json
     - The `json` library was used to parse the JSON files requested from the API. This library is a standard Python library, so no action needed.
- wheel
     - The `wheel` library is needed for the `flask` library. This is not a standard Python library.
- flask
     - The `flask` library allows the website to run on `localhost`. This is not a standard Python library.
- passlib
     - The `passlib` library was used to securely hash user passwords. This is not a standard Python library.
