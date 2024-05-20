# xplor-movies-at-mariana
This is repository for task given by xplor technology
Task Application:

# Below is summary for application:

Mariana Tek is hosting a series of events calledThe Movies@Mariana Tek this summer for camaraderie purposes. We want to be as democratic as possible, so each night we will have 3 choices that we can vote on. We need to create a small application where everyone can view the movies on the schedule, separated by date. These movies should be in a list with the following information:

Title
Poster
Genre(s)
Rating
Year Release
Metacritic Rating
Runtime
There should be one filter and one search. The filter should be by Genre. It should be a dropdown list, populated with all genres of movies currently in our list and it should hide all movies that do not match the selected genre when clicked. Bonus points if it allows for multiple selections.

The search should be by Title. It's should be a text input that, with each character, shows each movie that matches the current string and hides each movie that doesn't.


Database Updated with given Json file
movies/index.json



# Backend:

Using Django frontend, backend and API's are created, with given requirements


How to Run Backend Application


create directory
    
cmd    virtualenv venv


activate directory
    
cmd    .\venv\Script\activate

change directory
    
cmd    cd back-end


Install pip dependencies
    
cmd    pip install -r requirements.txt



To run backend application
    
cmd    python manage.py runsever 8000


Return all movies list which has high meta score for each date

access using browser http://127.0.0.1:8000/movies/



Result:

1) Login required
2) list all movies with high meta score
3) search bar to search movie
4) genre wise filter
5) each user can vote for single movie on each day



# Fronend with react js

cmd cd xplor-movies-at-mariana/front-end/frontend-app

cmd npm install

cmd npm start


access using browser http://127.0.0.1:3000/


Result:

1) Login required
2) list all movies with high meta score
3) search bar to search movie
4) genre wise filter
5) vote for movie 


# API's

http://127.0.0.1:8000/api/home/

    

http://127.0.0.1:8000/api/movies_by_date/<str:date>/

    parameter:

        date format YYYY-MM-DD


http://127.0.0.1:8000/api/vote/ 
    
    parameter:
        
        movie_id

