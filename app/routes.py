from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

# refactored function to validate_model
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model
# helper function 
# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         abort(make_response({"message": f"Planet {planet_id} was invalid"}, 400))

#     planet = Planet.query.get(planet_id)
    
#     if not planet:
#         abort(make_response({"message":f"Planet with id {planet_id} was not found"}, 404))
        
#     return planet

# retrieves all planets
@planets_bp.route("", methods = ["GET"])
def handle_planets():

    request.method == "GET"

    name_param = request.args.get("name")
    if name_param:
        planets = Planet.query.filter_by(name = name_param)
    else:
        planets = Planet.query.all()
    
    planets_response = [planet.make_planet_dict() for planet in planets]
    # for planet in planets:
    #     planets_response.append(planet.make_planet_dict())
    
    return jsonify(planets_response), 200

# makes a new planet
@planets_bp.route("", methods = ["POST"])
def create_planet():
    request.method == "POST"
    request_body = request.get_json()

    # if "name" not in request_body or "description" not in request_body or "color" not in request_body:
    #     return make_response("Invalid request!", 400)
    
    new_planet = Planet.from_dict(request_body)

    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} sucessfully created", 201)

# retrieves one planet by planet_id 
@planets_bp.route("/<planet_id>", methods = ["GET"])
def handle_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    
    return jsonify(planet.make_planet_dict()), 200

# updates one existing planet by planet_id
@planets_bp.route("/<planet_id>", methods = ["PUT"])
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    
    request_body = request.get_json()
    
    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.color = request_body["color"]
    
    db.session.commit()
    
    return make_response(jsonify(f"Planet #{planet_id} sucessfully updated"), 200)

# deletes one planet by planet_id
@planets_bp.route("/<planet_id>", methods = ["DELETE"])
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    
    db.session.delete(planet)
    db.session.commit()
    
    return make_response(jsonify(f"Planet #{planet_id} successfully deleted"), 200)

# class Planet:
#     def __init__(self, id, name, description, color):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.color = color

#     def make_planet_dict(self):
#         return dict(
#             id=self.id,
#             name=self.name,
#             description=self.description,
#             color=self.color
#         )

# planets = [
#     Planet(1, "Mercury", "hot", "grey"), 
#     Planet(2, "Venus", "Planet of love", "orange"), 
#     Planet(3, "Earth", "Home", "blue-green"),
#     Planet(4, "Mars", "volatile", "red"), 
#     Planet(5, "Jupiter", "stormy", "beige"), 
#     Planet(6, "Saturn", "the rings", "yellow"), 
#     Planet(7, "Uranus", "the single ring", "light blue"), 
#     Planet(8, "Neptune", "far away", "blue") 
# ]

# planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except: 
#         abort(make_response({"message": f"Planet with id {planet_id} is invalid"}, 400))
    
#     for planet in planets:
#         if planet.id == planet_id:
#             return planet
    
#     return abort(make_response({"message": f"Planet with id {planet_id} was not found"}, 404))


# @planets_bp.route("", methods = ["GET"])
# def handle_planets():
#     planets_response = []
#     for planet in planets:
#         planets_response.append(planet.make_planet_dict())
#     return jsonify(planets_response), 200


# @planets_bp.route("/<planet_id>", methods = ["GET"])
# def handle_planet(planet_id):
#     planet = validate_planet(planet_id)

#     return planet.make_planet_dict()






