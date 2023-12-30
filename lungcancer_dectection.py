import os
import joblib
import numpy as np
import json

model_path = "model/lung_cancer_svc_model.pkl"


if not os.path.exists(model_path):
    raise FileNotFoundError(f"No such model directory or file: '{model_path}'")
else:
    model = joblib.load(model_path)


def load_test_data():
    with open("data/data.json", encoding='utf_8') as f:
        return json.load(f)


def change_json_field(test_data):
   
    for data in test_data:
        data["gender"] = data.pop("GENDER")
        data["age"] = data.pop("AGE")
        data["smoking"] = data.pop("SMOKING")
        data["yellow_fingers"] = data.pop("YELLOW_FINGERS")
        data["anxiety"] = data.pop("ANXIETY")
        data["peer_pressure"] = data.pop("PEER_PRESSURE")
        data["chronic_disease"] = data.pop("CHRONIC DISEASE")
        data["fatigue"] = data.pop("FATIGUE")
        data["allergy"] = data.pop("ALLERGY")
        data["wheezing"] = data.pop("WHEEZING")
        data["alcohol"] = data.pop("ALCOHOL CONSUMING")
        data["coughing"] = data.pop("COUGHING")
        data["shortness_of_breath"] = data.pop("SHORTNESS OF BREATH")
        data["swallowing_difficulty"] = data.pop("SWALLOWING DIFFICULTY")
        data["chest_pain"] = data.pop("CHEST PAIN")   


    with open("data/converted_data.json" , "w") as f:
        json.dump(test_data ,f)       

      
    
       


def dectect_cancer(data):
    np_arr = data.to_numpy().ravel()

    data_arr = np.reshape(np_arr, (-1, 15))

    pred = model.predict(data_arr)

    return pred


if __name__ == "__main__":
    data = load_test_data()
    change_json_field(data)
