import json, re
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, Genre, Rating, MovieSchedule, UserMovieVote
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Max, Count, Case, When, Value, IntegerField, OuterRef, Subquery


data=[
    {
        "date": "2019-06-21T11:10:04.781Z",
        "movies": [
            {
                "title": "In the Mood for Love",
                "year": "2000",
                "rated": "PG",
                "released": "09 Mar 2001",
                "runtime": "98 min",
                "genre": [
                    "Drama",
                    "Romance"
                ],
                "director": "Kar-Wai Wong",
                "writer": "Kar-Wai Wong",
                "actors": "Maggie Cheung, Tony Chiu-Wai Leung, Ping Lam Siu, Tung Cho 'Joe' Cheung",
                "plot": "Two neighbors, a woman and a man, form a strong bond after both suspect extramarital activities of their spouses. However, they agree to keep their bond platonic so as not to commit similar wrongs.",
                "language": "Cantonese, Shanghainese, French, Spanish",
                "country": "Hong Kong, China",
                "awards": "Nominated for 1 BAFTA Film Award. Another 44 wins & 47 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BYjZjODRlMjQtMjJlYy00ZDBjLTkyYTQtZGQxZTk5NzJhYmNmXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "8.1/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "90%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "85/100"
                    }
                ],
                "meta_score": "85",
                "imdb_rating": "8.1",
                "imdb_votes": "105,461",
                "imdb_id": "tt0118694",
                "type": "movie",
                "dvd": "05 Mar 2002",
                "box_office": "N/A",
                "production": "USA Films",
                "website": "http://www.wkw-inthemoodforlove.com"
            },
            {
                "title": "Fantastic Planet",
                "year": "1973",
                "rated": "PG",
                "released": "01 Dec 1973",
                "runtime": "72 min",
                "genre": [
                    "Animation",
                    "Sci-Fi"
                ],
                "director": "René Laloux",
                "writer": "Stefan Wul (novel), Roland Topor (adaptation), René Laloux (adaptation)",
                "actors": "Jennifer Drake, Eric Baugin, Jean Topart, Jean Valmont",
                "plot": "On a faraway planet where blue giants rule, oppressed humanoids rebel against their machine-like leaders.",
                "language": "French, Czech",
                "country": "France, Czechoslovakia",
                "awards": "1 win & 2 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BYjhhMDFlZDctYzg1Mi00ZmZiLTgyNTgtM2NkMjRkNzYwZmQ0XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.8/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "89%"
                    }
                ],
                "meta_score": "N/A",
                "imdb_rating": "7.8",
                "imdb_votes": "20,216",
                "imdb_id": "tt0070544",
                "type": "movie",
                "dvd": "23 Oct 2007",
                "box_office": "N/A",
                "production": "New World Pictures",
                "website": "N/A"
            },
            {
                "title": "Oh, Sun",
                "year": "1967",
                "rated": "N/A",
                "released": "04 Jan 1973",
                "runtime": "98 min",
                "genre": [
                    "Drama"
                ],
                "director": "Med Hondo",
                "writer": "Med Hondo",
                "actors": "Yane Barry, Bernard Bresson, Greg Germain, Robert Liensol",
                "plot": "A native of Mauritania is delighted when he is chosen to work in Paris. Hoping to parlay the experience into a better life for himself, he eagerly prepares for his departure from his native...",
                "language": "French, Arabic",
                "country": "France, Mauritania",
                "awards": "1 win.",
                "poster": "N/A",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.4/10"
                    }
                ],
                "meta_score": "N/A",
                "imdb_rating": "7.4",
                "imdb_votes": "67",
                "imdb_id": "tt0062285",
                "type": "movie",
                "dvd": "N/A",
                "box_office": "N/A",
                "production": "N/A",
                "website": "N/A"
            }
        ]
    },
    {
        "date": "2019-06-28T11:10:04.781Z",
        "movies": [
            {
                "title": "The Love Witch",
                "year": "2016",
                "rated": "Unrated",
                "released": "10 Mar 2017",
                "runtime": "120 min",
                "genre": [
                    "Romance",
                    "Thriller"
                ],
                "director": "Anna Biller",
                "writer": "Anna Biller",
                "actors": "Samantha Robinson, Gian Keys, Laura Waddell, Jeffrey Vincent Parise",
                "plot": "A modern-day witch uses spells and magic to get men to fall in love with her.",
                "language": "English",
                "country": "USA",
                "awards": "3 wins & 3 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMjA5NDEyMjQwNV5BMl5BanBnXkFtZTgwNDQ1MjMwMDI@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "6.2/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "95%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "82/100"
                    }
                ],
                "meta_score": "82",
                "imdb_rating": "6.2",
                "imdb_votes": "9,153",
                "imdb_id": "tt3908142",
                "type": "movie",
                "dvd": "14 Mar 2017",
                "box_office": "$226,223",
                "production": "Oscilloscope Laboratories",
                "website": "N/A"
            },
            {
                "title": "The Craft",
                "year": "1996",
                "rated": "R",
                "released": "03 May 1996",
                "runtime": "101 min",
                "genre": [
                    "Drama",
                    "Fantasy",
                    "Horror",
                    "Thriller"
                ],
                "director": "Andrew Fleming",
                "writer": "Peter Filardi (story), Peter Filardi (screenplay), Andrew Fleming (screenplay)",
                "actors": "Robin Tunney, Fairuza Balk, Neve Campbell, Rachel True",
                "plot": "A newcomer to a Catholic prep high school falls in with a trio of outcast teenage girls who practice witchcraft, and they all soon conjure up various spells and curses against those who anger them.",
                "language": "English, French",
                "country": "USA",
                "awards": "1 win & 2 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BZTBkMWE1NGItZTgxMi00ZTE0LWIzZjAtNzQ5ZGZlZTQxN2EwXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "6.3/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "57%"
                    }
                ],
                "meta_score": "N/A",
                "imdb_rating": "6.3",
                "imdb_votes": "68,363",
                "imdb_id": "tt0115963",
                "type": "movie",
                "dvd": "02 Jul 1997",
                "box_office": "N/A",
                "production": "Sony Pictures Home Entertainment",
                "website": "N/A"
            },
            {
                "title": "Ganja & Hess",
                "year": "1973",
                "rated": "R",
                "released": "20 Apr 1973",
                "runtime": "110 min",
                "genre": [
                    "Drama",
                    "Fantasy",
                    "Horror"
                ],
                "director": "Bill Gunn",
                "writer": "Bill Gunn",
                "actors": "Duane Jones, Marlene Clark, Bill Gunn, Sam L. Waymon",
                "plot": "After being stabbed with an ancient, germ-infested knife, a doctor's assistant finds himself with an insatiable desire for blood.",
                "language": "English",
                "country": "USA",
                "awards": "N/A",
                "poster": "https://m.media-amazon.com/images/M/MV5BMTgxNjI5OTI1NF5BMl5BanBnXkFtZTgwNTI2OTY0NTM@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "6.2/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "86%"
                    }
                ],
                "meta_score": "N/A",
                "imdb_rating": "6.2",
                "imdb_votes": "999",
                "imdb_id": "tt0068619",
                "type": "movie",
                "dvd": "14 Jul 1998",
                "box_office": "N/A",
                "production": "Kelly/Jordan Enterprises",
                "website": "N/A"
            }
        ]
    },
    {
        "date": "2019-07-05T11:10:04.781Z",
        "movies": [
            {
                "title": "Persepolis",
                "year": "2007",
                "rated": "PG-13",
                "released": "22 Feb 2008",
                "runtime": "96 min",
                "genre": [
                    "Animation",
                    "Biography",
                    "Drama",
                    "History",
                    "War"
                ],
                "director": "Vincent Paronnaud, Marjane Satrapi",
                "writer": "Marjane Satrapi (comic), Vincent Paronnaud (scenario)",
                "actors": "Chiara Mastroianni, Danielle Darrieux, Catherine Deneuve, Simon Abkarian",
                "plot": "A precocious and outspoken Iranian girl grows up during the Islamic Revolution.",
                "language": "French, English, Persian, German",
                "country": "France, USA",
                "awards": "Nominated for 1 Oscar. Another 28 wins & 54 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMGRkZThmYzEtYjQxZC00OWEzLThjYjAtYzFkMjY0NGZkZWI4XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "8.1/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "96%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "90/100"
                    }
                ],
                "meta_score": "90",
                "imdb_rating": "8.1",
                "imdb_votes": "81,930",
                "imdb_id": "tt0808417",
                "type": "movie",
                "dvd": "24 Jun 2008",
                "box_office": "$4,400,000",
                "production": "Sony Pictures Classics",
                "website": "http://www.sonyclassics.com/persepolis/"
            },
            {
                "title": "Waltz with Bashir",
                "year": "2008",
                "rated": "R",
                "released": "12 Jun 2008",
                "runtime": "90 min",
                "genre": [
                    "Animation",
                    "Biography",
                    "Drama",
                    "History",
                    "Mystery",
                    "War"
                ],
                "director": "Ari Folman",
                "writer": "Ari Folman",
                "actors": "Ari Folman, Ori Sivan, Ronny Dayag, Shmuel Frenkel",
                "plot": "An Israeli film director interviews fellow veterans of the 1982 invasion of Lebanon to reconstruct his own memories of his term of service in that conflict.",
                "language": "Hebrew, Arabic, German, English",
                "country": "Israel, France, Germany, USA, Finland, Switzerland, Belgium, Australia",
                "awards": "Nominated for 1 Oscar. Another 44 wins & 58 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BNjM2OTI3NzQyNl5BMl5BanBnXkFtZTcwNjkzNzQ5MQ@@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "8.0/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "96%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "91/100"
                    }
                ],
                "meta_score": "91",
                "imdb_rating": "8.0",
                "imdb_votes": "52,295",
                "imdb_id": "tt1185616",
                "type": "movie",
                "dvd": "23 Jun 2009",
                "box_office": "$2,300,000",
                "production": "Sony Pictures Classics",
                "website": "http://www.sonyclassics.com/waltzwithbashir"
            },
            {
                "title": "Shark Tale",
                "year": "2004",
                "rated": "PG",
                "released": "01 Oct 2004",
                "runtime": "90 min",
                "genre": [
                    "Animation",
                    "Adventure",
                    "Comedy",
                    "Family",
                    "Fantasy"
                ],
                "director": "Bibo Bergeron, Vicky Jenson, Rob Letterman",
                "writer": "Michael J. Wilson (screenplay), Rob Letterman (screenplay), Scott Aukerman (additional dialogue), Alec Berg (additional dialogue), Sean Bishop (additional dialogue), BJ Porter (additional dialogue), Jeff Schaffer (additional dialogue), Lona Williams (additional dialogue), David P. Smith (additional dialogue), David Soren (additional dialogue)",
                "actors": "Will Smith, Robert De Niro, Renée Zellweger, Jack Black",
                "plot": "When a son of a gangster shark boss is accidentally killed while on the hunt, his would-be prey and his vegetarian brother decide to use the incident to their own advantage.",
                "language": "English",
                "country": "USA",
                "awards": "Nominated for 1 Oscar. Another 3 wins & 15 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMTMxMjY0NzE2M15BMl5BanBnXkFtZTcwNTc3ODcyMw@@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "6.0/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "36%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "48/100"
                    }
                ],
                "meta_score": "48",
                "imdb_rating": "6.0",
                "imdb_votes": "154,594",
                "imdb_id": "tt0307453",
                "type": "movie",
                "dvd": "08 Feb 2005",
                "box_office": "$160,762,022",
                "production": "DreamWorks SKG",
                "website": "http://www.sharktale.com/"
            }
        ]
    },
    {
        "date": "2019-07-12T11:10:04.781Z",
        "movies": [
            {
                "title": "Jumanji: Welcome to the Jungle",
                "year": "2017",
                "rated": "PG-13",
                "released": "20 Dec 2017",
                "runtime": "119 min",
                "genre": [
                    "Action",
                    "Adventure",
                    "Comedy",
                    "Fantasy"
                ],
                "director": "Jake Kasdan",
                "writer": "Chris McKenna (screenplay by), Erik Sommers (screenplay by), Scott Rosenberg (screenplay by), Jeff Pinkner (screenplay by), Chris McKenna (screen story by), Chris Van Allsburg (based on the book \"Jumanji\" by), Greg Taylor (based on the film \"Jumanji\" screen story by), Jim Strain (based on the film \"Jumanji\" screen story by), Chris Van Allsburg (based on the film \"Jumanji\" screen story by), Jonathan Hensleigh (based on the film \"Jumanji\" screenplay by), Greg Taylor (based on the film \"Jumanji\" screenplay by), Jim Strain (based on the film \"Jumanji\" screenplay by)",
                "actors": "Dwayne Johnson, Kevin Hart, Jack Black, Karen Gillan",
                "plot": "Four teenagers are sucked into a magical video game, and the only way they can escape is to work together to finish the game.",
                "language": "English",
                "country": "USA",
                "awards": "2 wins & 3 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BODQ0NDhjYWItYTMxZi00NTk2LWIzNDEtOWZiYWYxZjc2MTgxXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.0/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "76%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "58/100"
                    }
                ],
                "meta_score": "58",
                "imdb_rating": "7.0",
                "imdb_votes": "240,479",
                "imdb_id": "tt2283362",
                "type": "movie",
                "dvd": "20 Mar 2018",
                "box_office": "$393,201,353",
                "production": "Columbia Pictures",
                "website": "http://www.jumanjimovie.com/"
            },
            {
                "title": "The Babadook",
                "year": "2014",
                "rated": "Not Rated",
                "released": "28 Nov 2014",
                "runtime": "94 min",
                "genre": [
                    "Drama",
                    "Horror"
                ],
                "director": "Jennifer Kent",
                "writer": "Jennifer Kent",
                "actors": "Essie Davis, Noah Wiseman, Hayley McElhinney, Daniel Henshall",
                "plot": "A widowed mother, plagued by the violent death of her husband, battles with her son's fear of a monster lurking in the house, but soon discovers a sinister presence all around her.",
                "language": "English",
                "country": "Australia, Canada",
                "awards": "55 wins & 61 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMTk0NzMzODc2NF5BMl5BanBnXkFtZTgwOTYzNTM1MzE@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "6.8/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "98%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "86/100"
                    }
                ],
                "meta_score": "86",
                "imdb_rating": "6.8",
                "imdb_votes": "170,529",
                "imdb_id": "tt2321549",
                "type": "movie",
                "dvd": "13 Apr 2015",
                "box_office": "N/A",
                "production": "IFC Films",
                "website": "http://www.thebabadook.com"
            },
            {
                "title": "The Host",
                "year": "2006",
                "rated": "R",
                "released": "30 Mar 2007",
                "runtime": "120 min",
                "genre": [
                    "Action",
                    "Drama",
                    "Horror",
                    "Sci-Fi"
                ],
                "director": "Joon-ho Bong",
                "writer": "Joon-ho Bong (screenplay), Won-jun Ha (screenplay), Chul-hyun Baek (screenplay)",
                "actors": "Kang-ho Song, Hee-Bong Byun, Hae-il Park, Doona Bae",
                "plot": "A monster emerges from Seoul's Han River and begins attacking people. One victim's loving family does what it can to rescue her from its clutches.",
                "language": "Korean, English",
                "country": "South Korea",
                "awards": "25 wins & 25 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMTYyNTAwOTUyNl5BMl5BanBnXkFtZTYwODY0MTQ3._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.0/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "93%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "85/100"
                    }
                ],
                "meta_score": "85",
                "imdb_rating": "7.0",
                "imdb_votes": "84,370",
                "imdb_id": "tt0468492",
                "type": "movie",
                "dvd": "24 Jul 2007",
                "box_office": "$2,010,000",
                "production": "Magnolia Pictures",
                "website": "http://www.hostmovie.com/"
            }
        ]
    },
    {
        "date": "2019-07-19T11:10:04.781Z",
        "movies": [
            {
                "title": "Pariah",
                "year": "2011",
                "rated": "R",
                "released": "20 Jan 2011",
                "runtime": "86 min",
                "genre": [
                    "Drama"
                ],
                "director": "Dee Rees",
                "writer": "Dee Rees",
                "actors": "Adepero Oduye, Pernell Walker, Aasha Davis, Charles Parnell",
                "plot": "A Brooklyn teenager juggles conflicting identities and risks friendship, heartbreak, and family in a desperate search for sexual expression.",
                "language": "English",
                "country": "USA",
                "awards": "15 wins & 28 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMTM1MTQyNTY3NV5BMl5BanBnXkFtZTcwODk0ODk2Ng@@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.2/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "95%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "79/100"
                    }
                ],
                "meta_score": "79",
                "imdb_rating": "7.2",
                "imdb_votes": "5,424",
                "imdb_id": "tt1233334",
                "type": "movie",
                "dvd": "24 Apr 2012",
                "box_office": "$758,099",
                "production": "Focus Features",
                "website": "http://PariahMovie.com"
            },
            {
                "title": "Black Dynamite",
                "year": "2009",
                "rated": "R",
                "released": "13 Jan 2010",
                "runtime": "84 min",
                "genre": [
                    "Action",
                    "Comedy"
                ],
                "director": "Scott Sanders",
                "writer": "Michael Jai White (screenplay), Byron Minns (screenplay), Scott Sanders (screenplay), Michael Jai White (story), Byron Minns (story)",
                "actors": "Phyllis Applegate, Obba Babatundé, William Bassett, Troy Lindsey Brown",
                "plot": "Black Dynamite is the greatest African-American action star of the 1970s. When his only brother is killed by The Man, it's up to him to find justice.",
                "language": "English",
                "country": "USA",
                "awards": "1 win & 4 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BODMyM2JiYzMtODY3OS00ODExLTg0YzYtYWNlZTczMDUzY2I3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.4/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "83%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "65/100"
                    }
                ],
                "meta_score": "65",
                "imdb_rating": "7.4",
                "imdb_votes": "42,853",
                "imdb_id": "tt1190536",
                "type": "movie",
                "dvd": "16 Feb 2010",
                "box_office": "$131,862",
                "production": "Sony Pictures",
                "website": "http://www.blackdynamite.com/"
            },
            {
                "title": "The Wrestler",
                "year": "2008",
                "rated": "R",
                "released": "30 Jan 2009",
                "runtime": "109 min",
                "genre": [
                    "Drama",
                    "Sport"
                ],
                "director": "Darren Aronofsky",
                "writer": "Robert Siegel",
                "actors": "Mickey Rourke, Marisa Tomei, Evan Rachel Wood, Mark Margolis",
                "plot": "A faded professional wrestler must retire, but finds his quest for a new life outside the ring a dispiriting struggle.",
                "language": "English",
                "country": "USA, France",
                "awards": "Nominated for 2 Oscars. Another 57 wins & 86 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMTc5MjYyOTg4MF5BMl5BanBnXkFtZTcwNDc2MzQwMg@@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.9/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "98%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "81/100"
                    }
                ],
                "meta_score": "81",
                "imdb_rating": "7.9",
                "imdb_votes": "276,953",
                "imdb_id": "tt1125849",
                "type": "movie",
                "dvd": "21 Apr 2009",
                "box_office": "$26,136,413",
                "production": "Fox Searchlight Pictures",
                "website": "http://www.thewrestlermovie.com/index.html"
            }
        ]
    },
    {
        "date": "2019-07-26T11:10:04.781Z",
        "movies": [
            {
                "title": "Human Traffic",
                "year": "1999",
                "rated": "R",
                "released": "05 May 2000",
                "runtime": "99 min",
                "genre": [
                    "Comedy",
                    "Music"
                ],
                "director": "Justin Kerrigan",
                "writer": "Justin Kerrigan",
                "actors": "John Simm, Lorraine Pilkington, Shaun Parkes, Nicola Reynolds",
                "plot": "Five friends spend one lost weekend in a mix of music, love and club culture.",
                "language": "English",
                "country": "UK, Ireland",
                "awards": "9 wins & 7 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BM2ZlMjIxZjgtZGJiMC00ODAwLWJhNWYtYWJkZDg2Y2VkM2QyXkEyXkFqcGdeQXVyMjA0MzYwMDY@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.1/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "59%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "53/100"
                    }
                ],
                "meta_score": "53",
                "imdb_rating": "7.1",
                "imdb_votes": "21,726",
                "imdb_id": "tt0188674",
                "type": "movie",
                "dvd": "12 Dec 2000",
                "box_office": "N/A",
                "production": "Miramax Films",
                "website": "N/A"
            },
            {
                "title": "Paris Is Burning",
                "year": "1990",
                "rated": "R",
                "released": "01 Aug 1991",
                "runtime": "71 min",
                "genre": [
                    "Documentary"
                ],
                "director": "Jennie Livingston",
                "writer": "N/A",
                "actors": "Brooke Xtravaganza, André Christian, Dorian Corey, Paris Duprée",
                "plot": "A chronicle of New York's drag scene in the 1980s, focusing on balls, voguing and the ambitions and dreams of those who gave the era its warmth and vitality.",
                "language": "English",
                "country": "USA",
                "awards": "16 wins & 1 nomination.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMTY2NTc4MjQwMV5BMl5BanBnXkFtZTcwNjg5MTAzMQ@@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "8.1/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "100%"
                    }
                ],
                "meta_score": "N/A",
                "imdb_rating": "8.1",
                "imdb_votes": "8,880",
                "imdb_id": "tt0100332",
                "type": "movie",
                "dvd": "06 Sep 2005",
                "box_office": "N/A",
                "production": "Academy Entertainment",
                "website": "N/A"
            },
            {
                "title": "King of New York",
                "year": "1990",
                "rated": "R",
                "released": "29 Aug 1991",
                "runtime": "103 min",
                "genre": [
                    "Crime",
                    "Thriller"
                ],
                "director": "Abel Ferrara",
                "writer": "Nicholas St. John",
                "actors": "Christopher Walken, David Caruso, Laurence Fishburne, Victor Argo",
                "plot": "A drug kingpin is released from prison and seeks to take total control of the criminal underworld in order to give back to the community.",
                "language": "English",
                "country": "Italy",
                "awards": "1 win & 2 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BOTE2NDcxNzE4N15BMl5BanBnXkFtZTgwMDc1NTk4NjE@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.0/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "71%"
                    }
                ],
                "meta_score": "N/A",
                "imdb_rating": "7.0",
                "imdb_votes": "27,448",
                "imdb_id": "tt0099939",
                "type": "movie",
                "dvd": "15 Aug 2000",
                "box_office": "N/A",
                "production": "Live Home Video",
                "website": "N/A"
            }
        ]
    },
    {
        "date": "2019-08-02T11:10:04.781Z",
        "movies": [
            {
                "title": "A Most Violent Year",
                "year": "2014",
                "rated": "R",
                "released": "30 Jan 2015",
                "runtime": "125 min",
                "genre": [
                    "Crime",
                    "Drama",
                    "Thriller"
                ],
                "director": "J.C. Chandor",
                "writer": "J.C. Chandor",
                "actors": "Oscar Isaac, Elyes Gabel, Jessica Chastain, Lorna Pruce",
                "plot": "In New York City 1981, an ambitious immigrant fights to protect his business and family during the most dangerous year in the city's history.",
                "language": "English, Spanish",
                "country": "United Arab Emirates, USA",
                "awards": "Nominated for 1 Golden Globe. Another 15 wins & 50 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMjE4OTY4ODg3Ml5BMl5BanBnXkFtZTgwMTI1MTg1MzE@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.0/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "89%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "79/100"
                    }
                ],
                "meta_score": "79",
                "imdb_rating": "7.0",
                "imdb_votes": "60,152",
                "imdb_id": "tt2937898",
                "type": "movie",
                "dvd": "07 Apr 2015",
                "box_office": "N/A",
                "production": "A24",
                "website": "http://amostviolentyear.com/"
            },
            {
                "title": "Us",
                "year": "2019",
                "rated": "R",
                "released": "22 Mar 2019",
                "runtime": "116 min",
                "genre": [
                    "Horror",
                    "Mystery",
                    "Thriller"
                ],
                "director": "Jordan Peele",
                "writer": "Jordan Peele",
                "actors": "Lupita Nyong'o, Winston Duke, Elisabeth Moss, Tim Heidecker",
                "plot": "A family's serene beach vacation turns to chaos when their doppelgängers appear and begin to terrorize them.",
                "language": "English",
                "country": "USA, Japan, China",
                "awards": "N/A",
                "poster": "https://m.media-amazon.com/images/M/MV5BZTliNWJhM2YtNDc1MC00YTk1LWE2MGYtZmE4M2Y5ODdlNzQzXkEyXkFqcGdeQXVyMzY0MTE3NzU@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.1/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "94%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "81/100"
                    }
                ],
                "meta_score": "81",
                "imdb_rating": "7.1",
                "imdb_votes": "107,752",
                "imdb_id": "tt6857112",
                "type": "movie",
                "dvd": "N/A",
                "box_office": "N/A",
                "production": "Universal Pictures",
                "website": "https://www.usmovie.com/"
            },
            {
                "title": "Perfect Blue",
                "year": "1997",
                "rated": "R",
                "released": "28 Feb 1998",
                "runtime": "81 min",
                "genre": [
                    "Animation",
                    "Horror",
                    "Mystery",
                    "Thriller"
                ],
                "director": "Satoshi Kon",
                "writer": "Sadayuki Murai (screenplay), Yoshikazu Takeuchi (novel), Rika Takahashi (translation), Lia Sargent (adaptation)",
                "actors": "Junko Iwao, Rica Matsumoto, Shinpachi Tsuji, Masaaki Ôkura",
                "plot": "A retired pop singer turned actress' sense of reality is shaken when she is stalked by an obsessed fan and seemingly a ghost of her past.",
                "language": "Japanese",
                "country": "Japan",
                "awards": "3 wins & 2 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BYzA1MWE2OWQtY2Y1Zi00Njg0LTg5YTAtYzk1Mjk2N2JiNGE5XkEyXkFqcGdeQXVyNjUxMDQ0MTg@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.9/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "77%"
                    }
                ],
                "meta_score": "N/A",
                "imdb_rating": "7.9",
                "imdb_votes": "43,529",
                "imdb_id": "tt0156887",
                "type": "movie",
                "dvd": "26 Jan 2010",
                "box_office": "N/A",
                "production": "Palm Pictures",
                "website": "N/A"
            }
        ]
    },
    {
        "date": "2019-08-09T11:10:04.781Z",
        "movies": [
            {
                "title": "Seconds",
                "year": "1966",
                "rated": "R",
                "released": "14 Nov 1966",
                "runtime": "106 min",
                "genre": [
                    "Sci-Fi",
                    "Thriller"
                ],
                "director": "John Frankenheimer",
                "writer": "Lewis John Carlino (screenplay), David Ely (based on the novel by)",
                "actors": "Frank Campanella, John Randolph, Frances Reid, Barbara Werle",
                "plot": "An unhappy middle-aged banker agrees to a procedure that will fake his death and give him a completely new look and identity - one that comes with its own price.",
                "language": "English",
                "country": "USA",
                "awards": "Nominated for 1 Oscar. Another 1 win & 2 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BYmYwMmFjMDYtYTEyYS00NzUwLWIyZTMtNjFjZmVmZjhkY2M1XkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.7/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "91%"
                    }
                ],
                "meta_score": "N/A",
                "imdb_rating": "7.7",
                "imdb_votes": "14,037",
                "imdb_id": "tt0060955",
                "type": "movie",
                "dvd": "08 Jan 2002",
                "box_office": "N/A",
                "production": "Paramount Pictures",
                "website": "http://www.criterion.com/"
            },
            {
                "title": "Tig Notaro: Happy To Be Here",
                "year": "2018",
                "rated": "TV-14",
                "released": "22 May 2018",
                "runtime": "58 min",
                "genre": [
                    "Comedy"
                ],
                "director": "Tig Notaro",
                "writer": "Tig Notaro",
                "actors": "Indigo Girls, Tig Notaro, Amy Ray, Emily Saliers",
                "plot": "Comedian Tig Notaro performs a stand-up set at the historic Heights Theater in Houston.",
                "language": "English",
                "country": "USA",
                "awards": "N/A",
                "poster": "https://m.media-amazon.com/images/M/MV5BNWQxMDgzYjAtZTZkOS00MWM2LWIxNTUtZTUwYmUxMWQ0NzM1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "6.5/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "100%"
                    }
                ],
                "meta_score": "N/A",
                "imdb_rating": "6.5",
                "imdb_votes": "833",
                "imdb_id": "tt8342946",
                "type": "movie",
                "dvd": "22 May 2018",
                "box_office": "N/A",
                "production": "Netflix",
                "website": "N/A"
            },
            {
                "title": "The Rundown",
                "year": "2003",
                "rated": "PG-13",
                "released": "26 Sep 2003",
                "runtime": "104 min",
                "genre": [
                    "Action",
                    "Adventure",
                    "Comedy",
                    "Thriller"
                ],
                "director": "Peter Berg",
                "writer": "R.J. Stewart (story), R.J. Stewart (screenplay), James Vanderbilt (screenplay)",
                "actors": "Dwayne Johnson, Seann William Scott, Rosario Dawson, Christopher Walken",
                "plot": "A tough aspiring chef is hired to bring home a mobster's son from the Amazon but becomes involved in the fight against an oppressive town operator and the search for a legendary treasure.",
                "language": "English, Portuguese",
                "country": "USA",
                "awards": "2 wins & 3 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMWU3ZDYxZjMtZmYyOS00NWQyLTk1MmItNDg4ZWM2ZGQxOTNiXkEyXkFqcGdeQXVyMTMxMTY0OTQ@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "6.7/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "69%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "59/100"
                    }
                ],
                "meta_score": "59",
                "imdb_rating": "6.7",
                "imdb_votes": "95,240",
                "imdb_id": "tt0327850",
                "type": "movie",
                "dvd": "23 Mar 2004",
                "box_office": "$47,592,825",
                "production": "Universal Pictures",
                "website": "http://www.therundown.com/"
            }
        ]
    },
    {
        "date": "2019-08-16T11:10:04.781Z",
        "movies": [
            {
                "title": "Walking Tall",
                "year": "2004",
                "rated": "PG-13",
                "released": "02 Apr 2004",
                "runtime": "86 min",
                "genre": [
                    "Action",
                    "Crime"
                ],
                "director": "Kevin Bray",
                "writer": "Mort Briskin (earlier screenplay), David Klass (screenplay), Channing Gibson (screenplay), David Levien (screenplay), Brian Koppelman (screenplay)",
                "actors": "Michael Bowen, Johnny Knoxville, Dwayne Johnson, Neal McDonough",
                "plot": "A former U.S. soldier returns to his hometown to find it overrun by crime and corruption, which prompts him to clean house.",
                "language": "English",
                "country": "USA",
                "awards": "2 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MjYzNzM1N15BMl5BanBnXkFtZTcwMDcwNDc3NA@@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "6.3/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "26%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "44/100"
                    }
                ],
                "meta_score": "44",
                "imdb_rating": "6.3",
                "imdb_votes": "65,785",
                "imdb_id": "tt0351977",
                "type": "movie",
                "dvd": "28 Sep 2004",
                "box_office": "$45,860,039",
                "production": "MGM",
                "website": "http://www.walkingtallmovie.com/home.html"
            },
            {
                "title": "Sorry to Bother You",
                "year": "2018",
                "rated": "R",
                "released": "13 Jul 2018",
                "runtime": "111 min",
                "genre": [
                    "Comedy",
                    "Fantasy",
                    "Sci-Fi"
                ],
                "director": "Boots Riley",
                "writer": "Boots Riley",
                "actors": "LaKeith Stanfield, Tessa Thompson, Jermaine Fowler, Omari Hardwick",
                "plot": "In an alternate present-day version of Oakland, telemarketer Cassius Green discovers a magical key to professional success, propelling him into a universe of greed.",
                "language": "English",
                "country": "USA",
                "awards": "1 nomination.",
                "poster": "https://m.media-amazon.com/images/M/MV5BNjgwMmI4YzUtZGI2Mi00M2MwLWIyMmMtZWYzMWZmNzAyNmYwXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.0/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "93%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "80/100"
                    }
                ],
                "meta_score": "80",
                "imdb_rating": "7.0",
                "imdb_votes": "38,721",
                "imdb_id": "tt5688932",
                "type": "movie",
                "dvd": "23 Oct 2018",
                "box_office": "N/A",
                "production": "Annapurna Pictures",
                "website": "http://sorrytobotheryou.movie/"
            },
            {
                "title": "RBG",
                "year": "2018",
                "rated": "PG",
                "released": "14 Sep 2018",
                "runtime": "98 min",
                "genre": [
                    "Documentary",
                    "Biography"
                ],
                "director": "Julie Cohen, Betsy West",
                "writer": "N/A",
                "actors": "Ruth Bader Ginsburg, Ann Kittner, Harryette Helsel, Nina Totenberg",
                "plot": "The exceptional life and career of U.S. Supreme Court Justice Ruth Bader Ginsburg, who has developed a breathtaking legal legacy while becoming an unexpected pop culture icon.",
                "language": "English, Italian, German, French",
                "country": "USA",
                "awards": "1 nomination.",
                "poster": "https://m.media-amazon.com/images/M/MV5BNTE4Nzc0NDU3Nl5BMl5BanBnXkFtZTgwODIzMTQzNTM@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.5/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "94%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "71/100"
                    }
                ],
                "meta_score": "71",
                "imdb_rating": "7.5",
                "imdb_votes": "8,143",
                "imdb_id": "tt7689964",
                "type": "movie",
                "dvd": "28 Aug 2018",
                "box_office": "N/A",
                "production": "Magnolia Pictures",
                "website": "http://www.rbgmovie.com/"
            }
        ]
    },
    {
        "date": "2019-08-23T14:32:36.724Z",
        "movies": [
            {
                "title": "Isle of Dogs",
                "year": "2018",
                "rated": "PG-13",
                "released": "13 Apr 2018",
                "runtime": "101 min",
                "genre": [
                    "Animation",
                    "Adventure",
                    "Comedy",
                    "Drama",
                    "Fantasy",
                    "Sci-Fi"
                ],
                "director": "Wes Anderson",
                "writer": "Wes Anderson (story by), Roman Coppola (story by), Jason Schwartzman (story by), Kunichi Nomura (story by), Wes Anderson (screenplay by)",
                "actors": "Bryan Cranston, Koyu Rankin, Edward Norton, Bob Balaban",
                "plot": "Set in Japan, Isle of Dogs follows a boy's odyssey in search of his lost dog.",
                "language": "English, Japanese",
                "country": "Germany, USA",
                "awards": "2 wins.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMTYyOTUwNjAxM15BMl5BanBnXkFtZTgwODcyMzE0NDM@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.9/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "90%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "82/100"
                    }
                ],
                "meta_score": "82",
                "imdb_rating": "7.9",
                "imdb_votes": "108,697",
                "imdb_id": "tt5104604",
                "type": "movie",
                "dvd": "17 Jul 2018",
                "box_office": "N/A",
                "production": "Scott Rudin Productions",
                "website": "http://www.foxmovies-jp.com/inugashima/"
            },
            {
                "title": "Paddington 2",
                "year": "2017",
                "rated": "PG",
                "released": "12 Jan 2018",
                "runtime": "103 min",
                "genre": [
                    "Adventure",
                    "Comedy",
                    "Family",
                    "Fantasy"
                ],
                "director": "Paul King",
                "writer": "Paul King, Simon Farnaby, Michael Bond (\"Paddington Bear\" created by), Jon Croker (additional material), Simon Stephenson (additional material)",
                "actors": "Michael Gambon, Imelda Staunton, Ben Whishaw, Madeleine Harris",
                "plot": "Paddington, now happily settled with the Brown family and a popular member of the local community, picks up a series of odd jobs to buy the perfect present for his Aunt Lucy's 100th birthday, only for the gift to be stolen.",
                "language": "English",
                "country": "UK, France, USA",
                "awards": "Nominated for 3 BAFTA Film Awards. Another 3 wins & 7 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BMmYwNWZlNzEtNjE4Zi00NzQ4LWI2YmUtOWZhNzZhZDYyNmVmXkEyXkFqcGdeQXVyNzYzODM3Mzg@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "7.9/10"
                    },
                    {
                        "source": "Metacritic",
                        "value": "88/100"
                    }
                ],
                "meta_score": "88",
                "imdb_rating": "7.9",
                "imdb_votes": "46,157",
                "imdb_id": "tt4468740",
                "type": "movie",
                "dvd": "N/A",
                "box_office": "N/A",
                "production": "N/A",
                "website": "N/A"
            },
            {
                "title": "Paris, Texas",
                "year": "1984",
                "rated": "R",
                "released": "23 Aug 1984",
                "runtime": "145 min",
                "genre": [
                    "Drama"
                ],
                "director": "Wim Wenders",
                "writer": "L.M. Kit Carson (adaptation), Sam Shepard, Walter Donohue (story editor: Channel 4)",
                "actors": "Harry Dean Stanton, Nastassja Kinski, Dean Stockwell, Aurore Clément",
                "plot": "Travis Henderson, an aimless drifter who has been missing for four years, wanders out of the desert and must reconnect with society, himself, his life, and his family.",
                "language": "English, Spanish",
                "country": "West Germany, France, UK, USA",
                "awards": "Nominated for 1 Golden Globe. Another 16 wins & 9 nominations.",
                "poster": "https://m.media-amazon.com/images/M/MV5BM2RjMmU3ZWItYzBlMy00ZmJkLWE5YzgtNTVkODdhOWM3NGZhXkEyXkFqcGdeQXVyNDA5Mjg5MjA@._V1_SX300.jpg",
                "Ratings": [
                    {
                        "source": "Internet Movie Database",
                        "value": "8.1/10"
                    },
                    {
                        "source": "Rotten Tomatoes",
                        "value": "97%"
                    },
                    {
                        "source": "Metacritic",
                        "value": "78/100"
                    }
                ],
                "meta_score": "78",
                "imdb_rating": "8.1",
                "imdb_votes": "74,813",
                "imdb_id": "tt0087884",
                "type": "movie",
                "dvd": "14 Dec 2004",
                "box_office": "N/A",
                "production": "20th Century Fox",
                "website": "N/A"
            }
        ]
    }
]



     
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page or dashboard
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')




def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout




def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Redirect to a home page or dashboard
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



@login_required
def home_page(request, search_word=None, genre=None):
    all_genres = Genre.objects.all().values_list('name',flat=True)

    max_meta_score_subquery = MovieSchedule.objects.filter(
        date=OuterRef('date')
    ).annotate(
        meta_score=Case(
            When(movie__meta_score='N/A', then=Value(0)),
            default=F('movie__meta_score'),
            output_field=IntegerField()
        )
    ).values('date').annotate(
        max_meta_score=Max('meta_score')
    ).values('max_meta_score')

    highest_meta_score_movies = MovieSchedule.objects.annotate(
        max_meta_score=Subquery(max_meta_score_subquery)
    ).annotate(
        meta_score=Case(
            When(movie__meta_score='N/A', then=Value(0)),
            default=F('movie__meta_score'),
            output_field=IntegerField()
        )
    ).filter(
        meta_score=F('max_meta_score')
    ).select_related('movie').prefetch_related('movie__genres').order_by('date')
    

    if search_word:
        highest_meta_score_movies.filter(movie__title__contains=search_word)    
        
    return render(request, 'movies/home.html', {'movies': highest_meta_score_movies, 'all_genres':all_genres})


    

@login_required
def movies_by_date(request, date):
    date = datetime.strptime(date, '%Y-%m-%d')
    movies = MovieSchedule.objects.filter(date=date)
    return render(request, 'movies/scheduled_movies_.html', {'date': date, 'movies': movies})




@login_required
def vote_for_movie(request):
    print('Function called')
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_schedule = MovieSchedule.objects.get(pk=movie_id)
        user = request.user  # Assuming user is logged in

        # Check if the user has already voted for a movie on this date
        if UserMovieVote.objects.filter(user=user, movie_schedule__date=movie_schedule.date).exists():
            return JsonResponse({'success': False, 'message': 'You have already voted for a movie on this date.'})

        # If not, create a new vote
        UserMovieVote.objects.create(user=user, movie_schedule=movie_schedule)

        # Update the Metacritic score
        if movie_schedule.movie.meta_score == 'N/A':
            movie_schedule.movie.meta_score = 1  # Set to 1 since 'N/A' is treated as 0 + 1
        else:
            movie_schedule.movie.meta_score = F('meta_score') + 1  # Increment Metacritic score by 1

        movie_schedule.movie.save()  # Save the updated Metacritic score
        
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})