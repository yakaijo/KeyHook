import getpass
import pymongo
from pymongo import MongoClient
from bson import DBRef

class Utilities:
    """I have several variations on a theme in this project, and each one will need to start up
    with the same MongoDB database.  So I'm putting any sort of random little utilities in here
    as I need them.

    startup - creates the connection and returns the database client."""
    @staticmethod
    def startup():
        #Dat's connection
        # print("Connecting to atlast...")
        # #password = getpass.getpass(prompt='MongoDB password --> ')
        # cluster = "mongodb+srv://Dat:01249143073@mycluster.qbsczr4.mongodb.net/?retryWrites=true&w=majority"
        # client = MongoClient(cluster)
        # # I could also have said "db = client.demo_database" to do the same thing.
        # db = client.CECS323ProjectPhase3
        # print("Successful")
        # return db

        #Jacob's connection
        print("Connecting to atlast...")
        #password = getpass.getpass(prompt='MongoDB password --> ')
        cluster = your string
        client = MongoClient(cluster)
        # I could also have said "db = client.demo_database" to do the same thing.
        db = client.<YOUR DATABASE>
        print("Successful")
        return db

    """Return the size document for the given name."""
    @staticmethod
    def get_location_name(db, location_name):
        result = db.locations.find_one({"name": location_name})['_id']
        return result

    @staticmethod
    def get_building_name(db, building_name):
        result = db.buildings.find_one({"name": building_name})['_id']
        return result

    @staticmethod
    def get_door_name(db, door_name):
        result = db.doors.find_one({"name": door_name})['_id']
        return result

    @staticmethod
    def get_employee_id(db, employee_first_name, employee_last_name):
        result = db.employees.find_one({"first_name": employee_first_name, "last_name": employee_last_name})['_id']
        return result

    @staticmethod
    def get_room_id(db, room_number, building_name):
        result = db.rooms.find_one({"number": room_number,
                                    "buildings_name": DBRef("buildings", Utilities.get_building_name(db, building_name)) })['_id']
        return result

    @staticmethod
    def get_request_id(db, first_name,last_name, room_number, building_name, issue_date):
        result = db.requests.find_one({"employees_id_number" : DBRef("employees", Utilities.get_employee_id(db, first_name, last_name)),
                                       "rooms_id" : DBRef("rooms", Utilities.get_room_id(db, room_number, building_name)),
                                       "issue_date" : issue_date})['_id']
        return result

