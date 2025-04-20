# BLUEPRINT | DONT EDIT

from requests import get

movie_ids = [
    238, 680, 550, 185, 641, 515042, 152532, 120467, 872585, 906126, 840430
]

# /BLUEPRINT

# 👇🏻 YOUR CODE 👇🏻:
for movie_id in movie_ids:
    response = get(f"https://nomad-movies.nomadcoders.workers.dev/movies/{movie_id}")
    data = response.json()
    print(f"Title : {data["title"]} \nOverview : {data["overview"]}\nvote_average : {data["vote_average"]}\n")
    
# /YOUR CODE