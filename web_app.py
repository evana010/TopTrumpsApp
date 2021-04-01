from flask import Flask, render_template, request
import random
import requests
import urllib3

def random_superhero():
    superhero_number = random.randint(1, 731)
    url = 'https://superheroapi.com/api/2816318138625130/{}'.format(superhero_number)
    urllib3.disable_warnings()
    response = requests.get(url, verify=False)
    superhero = response.json()
    name = superhero['name']
    intelligence = superhero['powerstats']['intelligence']
    strength = superhero['powerstats']['strength']
    speed = superhero['powerstats']['speed']
    durability = superhero['powerstats']['durability']
    power = superhero['powerstats']['power']
    combat = superhero['powerstats']['combat']
    image = superhero['image']['url']

    if (intelligence != 'null') and (strength != 'null') and (speed != 'null') and (durability != 'null') and (power != 'null') and (combat != 'null'):
        return {
            'name': name,
            'intelligence': intelligence,
            'strength': strength,
            'speed': speed,
            'durability': durability,
            'power': power,
            'combat': combat,
            'image' : image
        }
    else:
        return random_superhero()
superhero_computer = random_superhero()
superhero_user = random_superhero()
user_score = 0
computer_score = 0

app = Flask("first-app")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/page1.html")
def page1():
    return render_template('page1.html', name=superhero_user["name"], intelligence=superhero_user["intelligence"], strength=superhero_user["strength"], speed=superhero_user["speed"], durability=superhero_user["durability"], power=superhero_user["power"], combat=superhero_user["combat"], image=superhero_user["image"], user_score=user_score, computer_score=computer_score)


@app.route("/request_form", methods=["POST", "GET"])
def submit_form():
    global user_score
    global computer_score
    global superhero_user
    global superhero_computer
    select_value = request.form.get('dropdown')
    select_value = str(select_value.lower())
    if int(superhero_user[select_value]) > int(superhero_computer[select_value]):
        user_score = user_score + 1
    elif int(superhero_user[select_value]) < int(superhero_computer[select_value]):
        computer_score = computer_score + 1
    else:
        pass

    superhero_computer = random_superhero()
    superhero_user = random_superhero()
    if user_score == 10:
        user_score = 0
        computer_score = 0
        return render_template('you_win.html')
    elif computer_score == 10:
        user_score = 0
        computer_score = 0
        return render_template('you_lose.html')
    else:
        return render_template('page1.html', name=superhero_user["name"], intelligence=superhero_user["intelligence"], strength=superhero_user["strength"], speed=superhero_user["speed"], durability=superhero_user["durability"], power=superhero_user["power"], combat=superhero_user["combat"], image=superhero_user["image"], user_score=user_score, computer_score=computer_score)

@app.route('/you_win.html')
def win():
    return render_template('/you_win.html')
@app.route('/you_lose.html')
def lose():
    return render_template('/you_lose.html')


app.run()
