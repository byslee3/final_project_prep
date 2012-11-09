import pull_json


batch = [

(62332524, "sin_t%C3%ADtulo_892"),
(62652167, "popular_trend_plaid_bag"),
(62652303, "am_who_because_my_choices"),
(62655046, "untitled_237"),
(62660147, "untitled_205")

]


for a, b in batch:
    
    print pull_json.create_set_file(a, b)