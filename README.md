## What is Twitterlytics?
Twitterlytics is a full-stack web application that collects, analyzes, and displays realtime Twitter data, as seen in this quick demonstration below. Click the gif below to open the actual Vimeo video.

<a href="https://player.vimeo.com/video/283262887" target="_blank"><img src="https://thumbs.gfycat.com/ElementarySilverLadybug-size_restricted.gif" width="100%" height="100%"/></a>

The current iteration of this application analyzes 2000 tweets (because of Twitter API constraints) for their most used langauges, love vs. hate words, and countries mentioned. It also categorizes tweets as "top" if the tweet exceeded 10,000 retweets. Some of these top tweets are printed below, and the languages from these top tweets are also analyzed.


## How does Twitterlytics work?
Twitterlytics utilizes Python 3 and the Tweepy library to grab tweets from the live Twitter API stream. The data is then written to a SQLite database, then presented using Flask and Google Charts.

The flowchart below illustrates the process.
![alt text](https://christiantimbol.com/live-Twitterlytics/static/img/tlytics.png "tlytics flowchart")


## How was Twitterlytics developed?
#### Design
I first began designing my solution after determining the technologies to use, exemplified by the flowchart diagram in the previous section. Doing this helped me ensure I had the big picture in mind as I proceeded to move onto actually coding. Through my design, I was able to think about the code blocks I'll have, their relationships to each other, as well as the overall data flow through Twitterlytics. Determining all technologies I planned on using in the beginning during the design phase allowed me to compile resources to help me accomplish the overall task as well.

#### [messy_twitter.py](https://github.com/christiantimbol/live-Twitterlytics/blob/master/messy_twitter.py) + [twitter.py](https://github.com/christiantimbol/live-Twitterlytics/blob/master/twitter.py)
Then, I began messy_twitter.py, which was my initial iteration of the final twitter.py file. The (messy_)twitter.py file is the main script which talks to the Twitter API. I first ensured this script may actually stream tweets, which would verify my credentials.py file (renamed to [YOUR-CREDENTIALS.py](https://github.com/christiantimbol/live-Twitterlytics/blob/master/YOUR-CREDENTIALS.py) to keep my credentials secret) as well as confirm that I can actually retrieve tweets using Tweepy. I then added a counter to the script to have it continuously stream tweets. Next, I added more details to the tweets being pulled by having the script categorize tweets by language and retweet count. At this point, messy_twitter.py began getting really *messy* (hence its name), so I added classes (Twitter class and Statistics class) to encompass the functions spread throughout the code. In order to preserve my evolving development process, I just left messy_twitter.py and created a new file (twitter.py) that wasn’t as messy.

#### [create_database.py](https://github.com/christiantimbol/live-Twitterlytics/blob/master/create_database.py)
After ensuring twitter.py retrieves and analyzes the tweets from the Twitter stream, I worked on the database script (create_database.py) to have the data inserted into a SQLite database according to the tables I created. Whenever twitter.py is run, [twitterlytics_data.db](https://github.com/christiantimbol/live-Twitterlytics/blob/master/twitterlytics_data.db) is updated.

#### [test_backend.py](https://github.com/christiantimbol/live-Twitterlytics/blob/master/test_backend.py)
Most of the backend code was finished at this point, so I wrote test scripts for the aforementioned files, test_backend.py. This script tests the development database code (not production data!), tests if the Twitter class may retrieve a small amount of tweets (compared to the 2000 actually grabbed), tests the analytical features (calls the functions to retrieve the categorized tweets and if they’ve been written to the database), and tests the stats class.

#### [test_frontend.py](https://github.com/christiantimbol/live-Twitterlytics/blob/master/test_frontend.py)
Onto the frontend! I wrote the tests for the upcoming Flask web server preemptively to help with actually developing the frontend because these tests contained the bulk of what I designed the frontend to be comprised of. These tests may be seen in test_frontend.py. Basically, it firsts checks if Flask is running on the development server (localhost:5000), then tests each frontend feature individually, starting with tweet languages.

#### [FlaskApp.py](https://github.com/christiantimbol/live-Twitterlytics/blob/master/FlaskApp.py)
Next, the actual Flask code, that may be seen in FlaskApp.py. This was my first time working with Flask, but it was generally straightforward thanks to their excellent documentation. Basically, FlaskApp.py reads the SQLite database and sends this data to the HTML pages in the Templates folder. In Twitterlytics’ case, the majority of the data is graphed through Google Charts. After getting the date displayed on my local environment, I touched up the frontend using [my website](https://ctimbol.com) as a guideline for Twitterlytics’ frontend codebase.


## Why was Twitterlytics made?
Ultimately, I decided to develop this to 1) practice full-stack Python applications and 2) because I use Twitter a lot (follow me at: [@christianlobmit](https://twitter.com/christianlobmit)) and found it intriguing to dive into Twitter data.


<!--

ToDo:
- fix nav bar mobile
- fix the inability to vertically scroll the embedded gists
- fix nav bar highlighting

-->

<!--

below is template for rest of readme

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

-->
