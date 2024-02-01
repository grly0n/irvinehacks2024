This app was created in 42 hours for UC Irvine's IrvineHacks 2024 Hackathon competition by [Gavin](https://github.com/gavindg), [George](https://github.com/grly0n), and [Alex](https://github.com/tenor-ow).

## Inspiration

Necessity. Have you ever been to the Brandywine or Anteatery websites? We don't like them. It takes a lot of menuing and scrolling to check what food will be served at each location. Compound that with some sluggish load times and you're in for a bad time.

## What it does

Brandeatery makes the upcoming menu for UCI's two most popular eateries accessible and user-friendly. Once you're on the site, you can see the menu for the next two weeks at either location with a single click.

## How we built it

Our backend is constructed in Python using the FastAPI framework. Our web scraping app is also written in Python using the libraries BeautifulSoup (HTML parser) and Selenium (for its web driver). The front end is written in HTML and Javascript using React and is hosted on Vercel.

## Challenges we ran into

- Creating the web scraper was quite time-consuming, as the Brandywine and Anteatery websites are heavily reliant on JavaScript. To get the menus for the next two weeks (or any arbitrary number of days ahead), we had to utilize a web driver to simulate a person going through all the menus that a human would have to. Doing so proved to be more complicated than expected, especially when accounting for things like loading screens, which the site has plenty of.

- Learning a new language or framework is a significant challenge, and FastAPI was no exception. In our final implementation we did not implementing many of its features, opting instead to read directly from .json files stored in the working directory instead of a dedicated and hosted backend, a problem for another time. Additionally, we found that it was far more straightforward for the frontend to access the raw JSON data instead of fetching SQL or the like from a database, contributing towards unique challenges involving JSON and Python dictionaries. Moreover, learning React, Javascript and webdev as whole while actively developing the project was challenging, as concepts such as arrow functions and syntax is completely foreign from languages that the team was used to.

## Accomplishments that we're proud of

- We're proud that we were able to put together a full-stack application. None of us had any web development experience coming into this project, but we created a pretty cohesive (and quite useful) app.

- After making some optimizations, our web-scraper runs more than twice as fast as it did after the initial implementation!

## What we learned

- [Gavin](https://github.com/gavindg) wrote the browser automation and web scraping portion. He ran into a few roadblocks along the way but is happy with how everything turned out. He's also currently working on a project that heavily involves web scraping, so this was great practice!

- Our front-end guy, [Alex](https://github.com/tenor-ow), essentially learned JavaScript and React as he was going through the project (and did a good job of it)! He was looking to learn the ins and outs of React before the hackathon, and finally got the chance to during the event.

- [George](https://github.com/grly0n) worked on the backend and database implementation, and he learned that web development as a whole is a tough, but rewarding experience. He is grateful to have had this valuable learning experience, and he hopes to continue learning in his classes and personal projects (for which he now has a few good ideas!)

## What's next for Brandeatery

Currently, our backend is only hosted locally at the moment and is used to periodically update our frontend hosted on Vercel. We plan to host the backend on a dedicated server. Our meatloaf timer also does not work, and we need to find a way to search for meatloaf in the next two weeks and countdown to that date. 
