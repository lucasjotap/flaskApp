from flask import Flask, jsonify
from faker import Faker

import requests
import random
import json

number_of_people: int = random.randint(1, 1000)

fake = Faker()
app = Flask(__name__)

def write_to_file(person_dict) -> str:
	with open('another_json.json', 'a') as file:
		dumped = json.dumps(person_dict, indent=4)
		file.write(str(dumped))
	return "\nFile written"

@app.route("/persons")
def retrieve_persons() -> dict:
	persons = []
	for person in range(0, number_of_people):
		full_name = fake.name().split()
		person = {
			"first_name": full_name[0],
			"second_name": full_name[-1],
			"address": fake.address(),
			"age": fake.random.randint(1, 100)
			}
		persons.append(person)
		write_to_file(person)
	return persons

@app.route("/trigger_azure_function", methods=['POST'])
def azure_func():
	try:
		azure_function_url = 'https://my-app-funct.azurewebsites.net/api/http_trigger1?code=fzFYiiidF8c_rR6wVw47vFxkgg2k3VAjXwwW7nwFdBbQAzFuQEvPhA%3D%3D'
		response = requests.post(azure_function_url)
		breakpoint()
		return jsonify({"message":"Azure function triggered successfully", "status_code": response.status_code})
	except Exception as e:
		return jsonify({"message":"Azure function triggered successfully", "status_code": response.status_code})
		print(e)


if __name__ == '__main__':
	app.run(debug=True, host="127.0.0.1", port=8000, passthrough_errors=True, use_reloader=False)