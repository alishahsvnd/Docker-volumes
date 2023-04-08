import requests
import hashlib
import os 

# Define the base URL of the server API
SERVER_URL = "http://server:3000"

# Define the paths of the API endpoints
INSERT_PERSON_ENDPOINT = "/persons"
LIST_PERSONS_ENDPOINT = "/persons"
GET_PERSON_ENDPOINT = "/persons/{id}"
REMOVE_PERSON_ENDPOINT = "/persons/{id}"
GET_FILE_ENDPOINT = "/file"

# Define a function to calculate the checksum of a file
def calculate_checksum(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

# Define a function to insert a person into the server
def insert_person(name, family):
    url = SERVER_URL + INSERT_PERSON_ENDPOINT
    data = {'name': name, 'family': family}
    response = requests.post(url, json=data)
    return response.json()

# Define a function to get a list of all persons from the server
def list_persons():
    persons = []
    url = SERVER_URL + LIST_PERSONS_ENDPOINT
    response = requests.get(url)
    for person in response.json():
        persons.append({"id: " + person.get("_id") + ", name: "+ person.get("name") + ", family: " + person.get("family")} )
    return persons

# Define a function to get a person by ID from the server
def get_person(person_id):
    url = SERVER_URL + GET_PERSON_ENDPOINT.format(id=person_id)
    response = requests.get(url)
    return response.json()

# Define a function to remove a person by ID from the server
def remove_person(person_id):
    url = SERVER_URL + REMOVE_PERSON_ENDPOINT.format(id=person_id)
    response = requests.delete(url)
    return response.json()

# Define a function to download a file from the server and verify its checksum
def get_file():
    url = SERVER_URL + GET_FILE_ENDPOINT
    response = requests.get(url)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Get the file content and checksum from the response headers
    file_content = response.content
    checksum = response.headers.get('X-Checksum')

    # create new directory in the current directory if it does not exist
    if not os.path.exists(dir_path+ "/clientdata"):
        os.makedirs(dir_path+ "/clientdata")
    file_path = dir_path + "/clientdata/file.txt"
    with open(file_path, 'wb') as f:
        f.write(response.content)

    # Verify the checksum of the file
    checksum_calculated = hashlib.sha256(file_content).hexdigest()
    if checksum == checksum_calculated:
        print('Checksum verified.')
    else:
        print('Checksum does not match.')

  
    return

# Define a function to run the client
def run():
    # check if the server is running
    try:
       get =  requests.get(SERVER_URL + "/persons")
       if get.status_code == 200:
            print(SERVER_URL + " is running!!!")

    except requests.exceptions.ConnectionError:
        print(SERVER_URL + " is not running!")
        return
    exit = False
    while not exit:
        print("-----------------------------------------------------------------")
        print("1. Insert Person")
        print("2. List of persons")
        print("3. Get Person by ID")
        print("4. Remove Person by ID")
        print("5. Get File")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter name: ")
            family = input("Enter family: ")
            person = insert_person(name, family)
            print("Inserted person: {}".format(person))
        elif choice == "2":
            persons = list_persons()
            print("List of persons: {}".format(persons))
        elif choice == "3":
            person_id = input("Enter person ID: ")
            person = get_person(person_id)
            print("Got person: {}".format(person))
        elif choice == "4":
            person_id = input("Enter person ID: ")
            person = remove_person(person_id)
            print("Removed person: {}".format(person))
        elif choice == "5":
            get_file()
        elif choice == "6":
            exit = True
        else:
            print("Invalid choice!")

# Run the client
run()