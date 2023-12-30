from flask import Flask
from flask_cors import CORS
import os
from functools import wraps
from flask import Flask, request, json
from lungcancer_dectection import dectect_cancer
from werkzeug.exceptions import BadRequest
from jsonschema import validate, ValidationError
import pandas as pd 

app = Flask(__name__)
cors = CORS(app)


def response_config(data, status_code, mime_type):
    return app.response_class(
        response=json.dumps(data), status=status_code, mimetype=mime_type
    )


app.config["JSON_SCHEMA"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "User data scheme",
    "type": "object",
    "properties": {
        "user_properties": {
            "type": "object",
            "properties": {
                "gender": {"type": "number", "minimum": 0, "maximum": 1},
                "age": {"type": "number", "minimum": 0, "maximum": 100},
                "smoking": {"type": "number", "minimum": 0, "maximum": 2},
                "yellow_fingers": {"type": "number", "minimum": 0, "maximum": 2},
                "anxiety": {"type": "number", "minimum": 0, "maximum": 2},
                "peer_pressure": {"type": "number", "minimum": 0, "maximum": 2},
                "chronic_disease": {"type": "number", "minimum": 0, "maximum": 2},
                "fatigue": {"type": "number", "minimum": 0, "maximum": 2},
                "allergy": {"type": "number", "minimum": 0, "maximum": 2},
                "wheezing": {"type": "number", "minimum": 0, "maximum": 2},
                "alcohol": {"type": "number", "minimum": 0, "maximum": 2},
                "coughing": {"type": "number", "minimum": 0, "maximum": 2},
                "shortness_of_breath": {"type": "number", "minimum": 0, "maximum": 2},
                "swallowing_difficulty": {"type": "number", "minimum": 0, "maximum": 2},
                "chest_pain": {"type": "number", "minimum": 0, "maximum": 2},
            },
            "required": [
                "gender",
                "age",
                "smoking",
                "yellow_fingers",
                "anxiety",
                "peer_pressure",
                "chronic_disease",
                "fatigue",
                "allergy",
                "wheezing",
                "alcohol",
                "coughing",
                "shortness_of_breath",
                "swallowing_difficulty",
                "chest_pain",
            ],
        },
    },
    "required": ["user_properties"],
}


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except BadRequest as e:
            data = {"Message": "400 Bad Request: Payload must be a valid json"}
            return response_config(data, 400, "application/json")
        return f(*args, **kw)

    return wrapper


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.json, app.config[schema_name])
            except ValidationError as e:
                data = {"Message": str(e.message)}
                return response_config(data, 400, "application/json")
            return f(*args, **kw)

        return wrapper

    return decorator


@app.route("/api/detect-lung-cancer", methods=["POST"])
@validate_json
@validate_schema("JSON_SCHEMA")
def get_properties():
    try:
        json_data = request.json
        json_to_pd = pd.json_normalize(json_data['user_properties'])

        res = dectect_cancer(json_to_pd)

        return response_config(str(res[0]), 200, "application/json")

    except Exception as e:
        app.logger.error("Error : ", str(e))
        data = {"Message": str(e)}
        return response_config(data, 500, "application/json")


if __name__ == "__main__":
    app.run(port=8000, debug=False)
