from flask import Flask, request, render_template, jsonify
import pickle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

model = pickle.load(open('model.pkl','rb'))

@app.route('/process_form', methods =["POST"])

def process_form():
    age = float(request.form['d_age'])
    ratings = float(request.form['range'])
    traffic_density = request.form['Road_traffic_density']
    vehicle_condition = request.form['Vehicle_condition']
    multiple_deliveries = request.form['multiple_deliveries']
    distance = float(request.form['distance'])
    weather_condition = request.form['WeatherConditions']
    festival = request.form['Festival']
    city = request.form['City']
    
    # Define mappings for ordinal variables
    traffic_density_mapping = {'Low': 1, 'Medium': 2, 'High': 3, 'Jam': 4}
    deliveries_mapping = {"0": 0, "1": 1, "2": 2, "3": 3}
    vehicle_condition_mapping = {"0": 0, "1": 1, "2": 2}

    # Convert ordinal values to their corresponding numeric values
    traffic_density_value = traffic_density_mapping.get(traffic_density, 0)
    deliveries_value = deliveries_mapping.get(multiple_deliveries, 0)
    vehicle_condition_value = vehicle_condition_mapping.get(vehicle_condition, 0)

    # Construct the input vector
    import numpy as np

    input_vector =np.array([
        age,
        ratings,
        traffic_density_value,
        vehicle_condition_value,
        deliveries_value,   
    ])

    # Handle nominal variables (dummy variables)
    festival_values = ['Yes']
    
    for value in festival_values:
        input_vector = np.append(input_vector, 1 if festival == 'Yes' else 0)

    #add the distance
    input_vector = np.append(input_vector, distance)
    #add weather
    weather_conditions = ['Windy','Fog','Sunny', 'Sandstorms','Stormy']
    for condition in weather_conditions:
        input_vector = np.append(input_vector,1 if condition == weather_condition else 0)

    #add city
    City_types = ['Urban', 'Semi-Urban']
    for condition in City_types:
        input_vector = np.append(input_vector,1 if condition == city else 0)

    # Use your model to make predictions with the input data
    prediction = model.predict([input_vector])
    hours, minutes = divmod(prediction[0], 60)
    formatted_time = "{:02} hours :{:02} minutes".format(int(hours), int(minutes))

    # Return the prediction result to the user
    return render_template('delivery.html', prediction_result="{}".format(formatted_time))

if __name__ == "__main__":
    app.run(debug =True)


