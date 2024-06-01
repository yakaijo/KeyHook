# Under the Run | Edit Configurations menu, select "Emulate terminal in output console" to get the getpass to work.
"""This version of the Pizza Mongo demonstration suite will use references for both the
pizza sizes as well as the layers since we cannot enforce a {pizza name, layer number}
uniqueness constraint in a MongoDB schema nor a uniqueness constraint on the elements of
an embedded array."""
import getpass
from datetime import datetime
from pprint import pprint

import pymongo
from bson import DBRef
from pymongo import MongoClient
from pprint import pprint
from Utilities import Utilities

if __name__ == '__main__':

    db = Utilities.startup()
    print('In main: ', db.list_collection_names())
    # Creating employeee table
    employees = db.employees
    # Clear all currently existing data in employee table
    employees.delete_many({})
    # Creating attributes for employee table
    employees.create_index([("first_name", pymongo.ASCENDING)], unique=True)
    employees.create_index([("last_name", pymongo.ASCENDING)], unique=True)
    # inserting seed data for employee
    employee_result = employees.insert_many([
        {"first_name": "John", "last_name": "Wick"},
        {"first_name": "Dwayne", "last_name": "Johnson"},
        {"first_name": "Kanade", "last_name": "Tachibana"},
        {"first_name": "Kana", "last_name": "Hanazawa"},
        {"first_name": "Ariana", "last_name": "Grande"},
        {"first_name": "Inori", "last_name": "Minase"},
    ])
    # employee validator to make sure the data insert type is correct
    employee_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': "object",
                'description': "Valid employee names",
                'required': ["first_name", "last_name"],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'first_name': {
                        'bsonType': "string",
                    },
                    'last_name': {
                        'bsonType': "string",
                    }
                }
            }
        }
    }
    db.command('collMod', 'employees', **employee_validator)

    locations = db.locations
    locations.delete_many({})
    locations.create_index([("name", pymongo.ASCENDING)], unique=True)
    # insterting seed data for location
    location_result = locations.insert_many([
        {"name": "Front"},
        {"name": "Rear"},
        {"name": "Side"},
        {"name": "Back"},
        {"name": "South"},
        {"name": "North"},
    ])
    location_validator = {
        'validator': {
            '$jsonSchema': {
                # Signifies that this schema is complex, has parameters within it.
                # These can be nested.
                'bsonType': "object",
                'description': "Valid location names",
                'required': ["name"],
                'additionalProperties': False,
                'properties': {

                    '_id': {},
                    'name': {
                        'bsonType': "string",
                    },
                }
            }
        }
    }
    db.command('collMod', 'locations', **location_validator)

    # # Simple testing by inserting an invalid data
    # try:
    #     locations_testing = locations.insert_one({"name": 2})
    # except Exception as ex:
    #     print("After inserting a bad location")
    #     pprint(ex)

    doors = db.doors
    doors.delete_many({})
    doors.create_index([("name", pymongo.ASCENDING)], unique=True)
    doors.create_index([("locations_name", pymongo.ASCENDING)], unique=False)

    # inserting seed data for doors
    door_results = doors.insert_many([
        {"name": "4 panels", "locations_name": DBRef("locations", Utilities.get_location_name(db, "North"))},
        {"name": "Half glass", "locations_name": DBRef("locations", Utilities.get_location_name(db, "Back"))},
        {"name": "6 panels", "locations_name": DBRef("locations", Utilities.get_location_name(db, "Rear"))},
        {"name": "Flush", "locations_name": DBRef("locations", Utilities.get_location_name(db, "Side"))},
        {"name": "All Glass", "locations_name": DBRef("locations", Utilities.get_location_name(db, "North"))},
        {"name": "3 panels", "locations_name": DBRef("locations", Utilities.get_location_name(db, "South"))},
    ])
    door_validator = {
        'validator': {
            '$jsonSchema': {
                # Signifies that this schema is complex, has parameters within it.
                # These can be nested.
                'bsonType': "object",
                'description': "Valid location names",
                'required': ["name", "locations_name"],
                'additionalProperties': False,
                'properties': {

                    '_id': {},
                    'name': {
                        'bsonType': "string",
                    },
                    'locations_name': {
                        'bsonType': "object",
                    },
                }
            }
        }
    }
    db.command('collMod', 'doors', **door_validator)

    # # Simple testing by inserting an invalid data
    # try:
    #     doors_testing = doors.insert_one(
    #         {"name": "10 panels", "locations_name": DBRef("locations", Utilities.get_location_name(db, "East"))})
    # except Exception as ex:
    #     print("After inserting a bad door")
    #     pprint(ex)

    buildings = db.buildings
    buildings.delete_many({})
    buildings.create_index([("name", pymongo.ASCENDING)], unique=True)

    # inserting seed data for building
    building_results = buildings.insert_many([
        {"name": "VEC"},
        {"name": "PH1"},
        {"name": "PSY"},
        {"name": "NUR"},
        {"name": "HSCI"},
        {"name": "EN2"},
    ])

    building_validator = {
        'validator': {
            '$jsonSchema': {
                # Signifies that this schema is complex, has parameters within it.
                # These can be nested.
                'bsonType': "object",
                'description': "Valid location names",
                'required': ["name"],
                'additionalProperties': False,
                'properties': {

                    '_id': {},
                    'name': {
                        'bsonType': "string",
                    },
                }
            }
        }
    }
    db.command('collMod', 'buildings', **building_validator)

    rooms = db.rooms
    rooms.delete_many({})
    rooms.create_index([("number", pymongo.ASCENDING)])
    rooms.create_index([("buildings_name", pymongo.ASCENDING)])
    rooms.create_index([("doors_name", pymongo.ASCENDING)])

    # inserting seed data for rooms
    room_results = rooms.insert_many([
        {"number": 428, "buildings_name": DBRef("buildings", Utilities.get_building_name(db, "VEC")),
         "doors_name": DBRef("doors", Utilities.get_door_name(db, "4 panels"))},
        {"number": 326, "buildings_name": DBRef("buildings", Utilities.get_building_name(db, "VEC")),
         "doors_name": DBRef("doors", Utilities.get_door_name(db, "4 panels"))},
        {"number": 125, "buildings_name": DBRef("buildings", Utilities.get_building_name(db, "EN2")),
         "doors_name": DBRef("doors", Utilities.get_door_name(db, "Flush"))},
        {"number": 224, "buildings_name": DBRef("buildings", Utilities.get_building_name(db, "NUR")),
         "doors_name": DBRef("doors", Utilities.get_door_name(db, "6 panels"))},
        {"number": 100, "buildings_name": DBRef("buildings", Utilities.get_building_name(db, "HSCI")),
         "doors_name": DBRef("doors", Utilities.get_door_name(db, "3 panels"))},
        {"number": 512, "buildings_name": DBRef("buildings", Utilities.get_building_name(db, "PH1")),
         "doors_name": DBRef("doors", Utilities.get_door_name(db, "All Glass"))},
    ])

    room_validator = {
        'validator': {
            '$jsonSchema': {
                # Signifies that this schema is complex, has parameters within it.
                # These can be nested.
                'bsonType': "object",
                'description': "Valid rooms",
                'required': ["number", "buildings_name", "doors_name"],
                'additionalProperties': False,
                'properties': {

                    '_id': {},
                    'number': {
                        'bsonType': "number",
                    },
                    'buildings_name': {
                        'bsonType': "object",
                    },
                    'doors_name': {
                        'bsonType': "object",
                    },
                }
            }
        }
    }
    db.command('collMod', 'doors', **door_validator)

    requests = db.requests
    requests.delete_many({})
    requests.create_index([("employees_id_number", pymongo.ASCENDING)])
    requests.create_index([("rooms_id", pymongo.ASCENDING)])
    requests.create_index([("issue_date", pymongo.ASCENDING)])

    request_results = requests.insert_many([
        {"employees_id_number": DBRef("employees", Utilities.get_employee_id(db, "John", "Wick")),
         "rooms_id": DBRef("rooms", Utilities.get_room_id(db, 428, "VEC")),
         "issue_date": datetime(2022, 11, 10, 0, 0, 0)},
        {"employees_id_number": DBRef("employees", Utilities.get_employee_id(db, "Dwayne", "Johnson")),
         "rooms_id": DBRef("rooms", Utilities.get_room_id(db, 100, "HSCI")),
         "issue_date": datetime(2021, 11, 5, 0, 0, 0)},
        {"employees_id_number": DBRef("employees", Utilities.get_employee_id(db, "Ariana", "Grande")),
         "rooms_id": DBRef("rooms", Utilities.get_room_id(db, 224, "NUR")),
         "issue_date": datetime(2022, 1, 30, 0, 0, 0)},
        {"employees_id_number": DBRef("employees", Utilities.get_employee_id(db, "John", "Wick")),
         "rooms_id": DBRef("rooms", Utilities.get_room_id(db, 125, "EN2")),
         "issue_date": datetime(2019, 12, 12, 0, 0, 0)},
        {"employees_id_number": DBRef("employees", Utilities.get_employee_id(db, "Kana", "Hanazawa")),
         "rooms_id": DBRef("rooms", Utilities.get_room_id(db, 326, "VEC")),
         "issue_date": datetime(2022, 5, 15, 0, 0, 0)},
        {"employees_id_number": DBRef("employees", Utilities.get_employee_id(db, "Kanade", "Tachibana")),
         # request has not been fulfiled
         "rooms_id": DBRef("rooms", Utilities.get_room_id(db, 224, "NUR")),
         "issue_date": datetime(2020, 10, 3, 0, 0, 0)},
        {"employees_id_number": DBRef("employees", Utilities.get_employee_id(db, "John", "Wick")),
         "rooms_id": DBRef("rooms", Utilities.get_room_id(db, 512, "PH1")),
         "issue_date": datetime(2020, 11, 15, 0, 0, 0)},
    ])

    request_validator = {
        'validator': {
            '$jsonSchema': {
                # Signifies that this schema is complex, has parameters within it.
                # These can be nested.
                'bsonType': "object",
                'description': "Valid requests",
                'required': ["employees_id_number", "rooms_id", "issue_date"],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'employees_id_number': {
                        'bsonType': "object"
                    },
                    'rooms_id': {
                        'bsonType': "object"
                    },
                    'issue_date': {
                        'bsonType': "date",
                    },
                }
            }
        }
    }
    db.command('collMod', 'requests', **request_validator)

    # # Simple testing by inserting an invalid data
    # try:
    #     #test 1
    #     # request_testing = requests.insert_one({"employees_id_number": DBRef("employees", Utilities.get_employee_id(db, "John", "Wick")),
    #     #  "rooms_id": DBRef("rooms", Utilities.get_room_id(db, 428, "VEC")),"issue_date": "2022-11-10"},)
    #
    #     #test 2
    #     request_testing = requests.insert_one({"employees_id_number": DBRef("employees", Utilities.get_employee_id(db, "John", "Wick")),
    #      "rooms_id": "VEC 428","issue_date": datetime(2022, 11, 10, 0, 0, 0)},)
    # except Exception as ex:
    #     print("Invalid input for requests")
    #     pprint(ex)

    returns = db.returns
    returns.delete_many({})
    returns.create_index([("requests_id", pymongo.ASCENDING)])
    returns.create_index([("return_date", pymongo.ASCENDING)])

    return_results = returns.insert_many([
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "John", "Wick", 428, "VEC",
                                                                   datetime(2022, 11, 10, 0, 0, 0))),
         "return_date": None},
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "Dwayne", "Johnson", 100, "HSCI",
                                                                   datetime(2021, 11, 5, 0, 0, 0))),
         "return_date": None},
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "Ariana", "Grande", 224, "NUR",
                                                                   datetime(2022, 1, 30, 0, 0, 0))),
         "return_date": datetime(2022, 4, 30, 0, 0, 0)},
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "John", "Wick", 125, "EN2",
                                                                   datetime(2019, 12, 12, 0, 0, 0))),
         "return_date": datetime(2020, 3, 10, 0, 0, 0)},
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "Kana", "Hanazawa", 326, "VEC",
                                                                   datetime(2022, 5, 15, 0, 0, 0))),
         "return_date": None},
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "John", "Wick", 512, "PH1",
                                                                   datetime(2020, 11, 15, 0, 0, 0))),
         "return_date": datetime(2021, 11, 15, 0, 0, 0)},
    ])

    return_validator = {
        'validator': {
            '$jsonSchema': {
                # Signifies that this schema is complex, has parameters within it.
                # These can be nested.
                'bsonType': "object",
                'description': "Valid returns",
                'required': ["requests_id", "return_date"],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'requests_id': {
                        'bsonType': "object"
                    },
                    'return_date': {
                        'bsonType': "date",
                    },
                }
            }
        }
    }
    db.command('collMod', 'returns', **return_validator)

    # Simple testing by inserting an invalid data
    # try:
    #     returns_testing = returns.insert_one(
    #         {"requests_id": DBRef("requests", Utilities.get_request_id(db, "Ariana", "Grandee", 224, "NUR", '2022-01-30')),
    #          "return_date": '2022-04-30'},)
    # except Exception as ex:
    #     print("Invalid input for returns")
    #     #pprint(ex)

    losts = db.losts
    losts.delete_many({})
    losts.create_index([("requests_id", pymongo.ASCENDING)])
    losts.create_index([("date_reported", pymongo.ASCENDING)])

    lost_results = losts.insert_many([
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "John", "Wick", 428, "VEC",
                                                                   datetime(2022, 11, 10, 0, 0, 0))),
         "date_reported": None},
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "Dwayne", "Johnson", 100, "HSCI",
                                                                   datetime(2021, 11, 5, 0, 0, 0))),
         "date_reported": datetime(2022, 2, 12, 0, 0, 0)},
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "Ariana", "Grande", 224, "NUR",
                                                                   datetime(2022, 1, 30, 0, 0, 0))),
         "date_reported": None},
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "John", "Wick", 125, "EN2",
                                                                   datetime(2019, 12, 12, 0, 0, 0))),
         "date_reported": None},
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "Kana", "Hanazawa", 326, "VEC",
                                                                   datetime(2022, 5, 15, 0, 0, 0))),
         "date_reported": None},
        {"requests_id": DBRef("requests", Utilities.get_request_id(db, "John", "Wick", 512, "PH1",
                                                                   datetime(2020, 11, 15, 0, 0, 0))),
         "date_reported": None},
    ])
    lost_validator = {
        'validator': {
            '$jsonSchema': {
                # Signifies that this schema is complex, has parameters within it.
                # These can be nested.
                'bsonType': "object",
                'description': "Valid losts",
                'required': ["requests_id", "date_reported"],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'requests_id': {
                        'bsonType': "object"
                    },
                    'date_reported': {
                        'bsonType': "date",
                    },
                }
            }
        }
    }
    db.command('collMod', 'losts', **lost_validator)

    keys = db.keys
    keys.delete_many({})
    keys.create_index([("requests_id", pymongo.ASCENDING)])

    key1 = keys.insert_one({"requests_id": DBRef("requests", Utilities.get_request_id(db, "John", "Wick", 428, "VEC",
                                                                                      datetime(2022, 11, 10, 0, 0,
                                                                                               0)))})
    key2 = keys.insert_one({"requests_id": DBRef("requests", Utilities.get_request_id(db, "John", "Wick", 512, "PH1",
                                                                                      datetime(2020, 11, 15, 0, 0,
                                                                                               0)))})
    key3 = keys.insert_one({"requests_id": DBRef("requests", Utilities.get_request_id(db, "John", "Wick", 125, "EN2",
                                                                                      datetime(2019, 12, 12, 0, 0,
                                                                                               0)))})
    key4 = keys.insert_one({"requests_id": DBRef("requests",
                                                 Utilities.get_request_id(db, "Ariana", "Grande", 224, "NUR",
                                                                          datetime(2022, 1, 30, 0, 0, 0)))})
    key5 = keys.insert_one({"requests_id": DBRef("requests",
                                                 Utilities.get_request_id(db, "Dwayne", "Johnson", 100, "HSCI",
                                                                          datetime(2021, 11, 5, 0, 0, 0)))})
    key6 = keys.insert_one({"requests_id": DBRef("requests",
                                                 Utilities.get_request_id(db, "Kana", "Hanazawa", 326, "VEC",
                                                                          datetime(2022, 5, 15, 0, 0, 0)))})

    hooks = db.hooks
    hooks.delete_many({})
    hooks.create_index([("keys_id", pymongo.ASCENDING)])

    hook1 = hooks.insert_one({"keys_id": key1.inserted_id})
    hook2 = hooks.insert_one({"keys_id": key2.inserted_id})
    hook3 = hooks.insert_one({"keys_id": key3.inserted_id})
    hook4 = hooks.insert_one({"keys_id": key4.inserted_id})
    hook5 = hooks.insert_one({"keys_id": key5.inserted_id})
    hook6 = hooks.insert_one({"keys_id": key6.inserted_id})
    hook7 = hooks.insert_one({"keys_id": None})  # can open NUR 224 6 panels
    hook8 = hooks.insert_one({"keys_id": None})  # can open VEC 326 and 428 (4 panels)

    door_hooks = db.door_hooks
    door_hooks.delete_many({})
    door_hooks.create_index([("doors_name", pymongo.ASCENDING)])
    door_hooks.create_index([("hooks_id", pymongo.ASCENDING)])

    door_hook1 = door_hooks.insert_one(
        {"doors_name": DBRef("doors", Utilities.get_door_name(db, "4 panels")), "hooks_id": hook1.inserted_id})
    door_hook2 = door_hooks.insert_one(
        {"doors_name": DBRef("doors", Utilities.get_door_name(db, "Flush")), "hooks_id": hook3.inserted_id})
    door_hook3 = door_hooks.insert_one(
        {"doors_name": DBRef("doors", Utilities.get_door_name(db, "6 panels")), "hooks_id": hook4.inserted_id})
    door_hook4 = door_hooks.insert_one(
        {"doors_name": DBRef("doors", Utilities.get_door_name(db, "3 panels")), "hooks_id": hook5.inserted_id})
    door_hook5 = door_hooks.insert_one(
        {"doors_name": DBRef("doors", Utilities.get_door_name(db, "All Glass")), "hooks_id": hook2.inserted_id})
    door_hook6 = door_hooks.insert_one(
        {"doors_name": DBRef("doors", Utilities.get_door_name(db, "4 panels")), "hooks_id": hook6.inserted_id})
    door_hook7 = door_hooks.insert_one(
        {"doors_name": DBRef("doors", Utilities.get_door_name(db, "6 panels")), "hooks_id": hook7.inserted_id})
    door_hook8 = door_hooks.insert_one(
        {"doors_name": DBRef("doors", Utilities.get_door_name(db, "4 panels")), "hooks_id": hook8.inserted_id})

    # creating menu application
    print("------------------------------------------------------------------------------")
    print()
    print("Menu System:")
    print()
    print("1: Create a new Key")
    print("2: Request access to a room by a given employee")
    print("3: Capture issue of a key to an employee")
    print("4: Capture losing a key")
    print("5: Report all rooms an employee can enter, given the keys that he/she already has")
    print("6: Delete a key")
    print("7: Delete an employee")
    print("8: Add new door that can be opened by existing hook")
    print("9: Update access request to move it to a new employee")
    print("10: Report out all the employees who can get into a room")
    print("Type 0 to exit out")
    print()
    print("Please input the number you want: ")
    print()

    choice = input()
    while choice != "0":

        hooks_list = hooks.find({})
        doors_list = doors.find({})
        door_hooks_list = door_hooks.find({})
        rooms_list = rooms.find({})
        employees_list = employees.find({})
        keys_list = keys.find({})
        requests_list = requests.find({})
        losts_list = losts.find({})
        returns_list = returns.find({})
        # Create a new key
        if choice == "1":

            counter = 0
            valid_hook_list = []
            print("List of available hooks")
            for hook_document in hooks_list:
                hooks_list = hooks.find({})
                doors_list = doors.find({})
                door_hooks_list = door_hooks.find({})
                rooms_list = rooms.find({})
                if (hook_document["keys_id"] is None):
                    current_hook_id = hook_document["_id"]
                    counter += 1
                    valid_hook_list.append(hook_document)
                    print("hook #", counter, ": ", current_hook_id, "Can open rooms")
                    for door_hook_document in door_hooks_list:
                        if (current_hook_id == door_hook_document["hooks_id"]):
                            doors_can_open = []
                            doors_can_open.append(door_hook_document["doors_name"])
                            for room_document in rooms_list:
                                for door_name in doors_can_open:
                                    if room_document["doors_name"] == door_name:
                                        ref_building = db.dereference(room_document["buildings_name"])
                                        print("Room", ref_building["name"],
                                              room_document["number"])

            print("which hook would you like to pick")
            user_hook_choice = input()
            selected_hook = valid_hook_list[int(user_hook_choice) - 1]
            print("you selected hook: ", selected_hook)
            print("------------------------------------------------------------------------------")
            # create a key
            print("Creating key...")
            newkey = keys.insert_one({"requests_id": None})
            print("Key created")
            print("------------------------------------------------------------------------------")
            # update hook
            updated_hook = hooks.update_one({"_id": selected_hook["_id"]},
                                            {"$set": {"keys_id": newkey.inserted_id}})
            print("Selected hook has been updated")  # Create a em

        # Request access to a room by a given employee
        elif choice == "2":  # Request access to a room
            # present the user with a list of employees by name and prompt for which one
            employee_list = []
            counter = 0
            print("------------------------------------------------------------------------------")
            print("Employee list")
            for employee_document in employees_list:
                employee_list.append(employee_document)
                counter += 1
                print("Employee #", counter, ": ", employee_document["first_name"], employee_document["last_name"])
            print("Please select an employee ")
            user_employee_choice = input()
            print("You selected employee ", employee_list[int(user_employee_choice) - 1])
            selected_employee = employee_list[int(user_employee_choice) - 1]

            # present the user with a list of the buildings and rooms and prompt for which one
            rooms_list = rooms.find({})
            room_list = []
            counter = 0
            print("------------------------------------------------------------------------------")
            print("Room list")
            for room_document in rooms_list:
                room_list.append(room_document)
                counter += 1
                ref_building = db.dereference(room_document["buildings_name"])
                print("Room #", counter, ": ", ref_building["name"], room_document["number"])
            print("Please select a room you wish to request access")
            user_room_choice = input()
            print("You selected room ", room_list[int(user_room_choice) - 1])
            selected_room = room_list[int(user_room_choice) - 1]
            print("------------------------------------------------------------------------------")
            print("Please enter the current year:")
            year = input()
            print("Please enter the current month:")
            month = input()
            print("Please enter today date:")
            date = input()
            print("------------------------------------------------------------------------------")
            print("Creating new request")
            ref_building = db.dereference(selected_room["buildings_name"])
            newreq = requests.insert_one({"employees_id_number": DBRef("employees", Utilities.get_employee_id(db,
                                                                                                              selected_employee[
                                                                                                                  "first_name"],
                                                                                                              selected_employee[
                                                                                                                  "last_name"])),
                                          "rooms_id": DBRef("rooms",
                                                            Utilities.get_room_id(db, int(selected_room["number"]),
                                                                                  str(ref_building["name"]))),
                                          # str(deref_building_name)
                                          "issue_date": datetime(int(year), int(month), int(date), 0, 0, 0),
                                          })
            print("Create new request successfully")
            print("New request id is: ", newreq.inserted_id)

        # Capture issue of a key to an employee
        elif choice == "3":  # capture the issue of a key to an employee

            # Prompt employee
            employee_list = []
            counter = 0
            print("------------------------------------------------------------------------------")
            print("Employee list")
            for employee_document in employees_list:
                employee_list.append(employee_document)
                counter += 1
                print("Employee #", counter, ": ", employee_document["first_name"], employee_document["last_name"])
            print("Please select which employee are you")
            user_employee_choice = input()
            print("You selected employee ", employee_list[int(user_employee_choice) - 1])
            selected_employee = employee_list[int(user_employee_choice) - 1]

            # prompt which room want to access, based on existing rooms
            room_list = []
            counter = 0
            print("------------------------------------------------------------------------------")
            print("Room list")
            for room_document in rooms_list:
                room_list.append(room_document)
                counter += 1
                ref_building = db.dereference(room_document["buildings_name"])
                print("Room #", counter, ": ", ref_building["name"], room_document["number"], "   (room id: ",
                      room_document["_id"], ")")
            print("Please select a room that you wish to access ")
            user_room_choice = input()
            print("You selected room ", room_list[int(user_room_choice) - 1])
            selected_room = room_list[int(user_room_choice) - 1]

            # create new request based on answer
            print("------------------------------------------------------------------------------")
            print("Please enter the current year:")
            year = input()
            print("Please enter the current month:")
            month = input()
            print("Please enter today date:")
            date = input()
            print("------------------------------------------------------------------------------")
            print("Creating new request...")
            ref_building = db.dereference(selected_room["buildings_name"])
            newreq = requests.insert_one({
                "employees_id_number": DBRef("employees", Utilities.get_employee_id(db, selected_employee["first_name"],
                                                                                    selected_employee["last_name"])),
                "rooms_id": DBRef("rooms",
                                  Utilities.get_room_id(db, int(selected_room["number"]), str(ref_building["name"]))),
                "issue_date": datetime(int(year), int(month), int(date), 0, 0, 0), })
            print("Create new request successfully")
            print("New request id is: ", newreq.inserted_id)
            print("------------------------------------------------------------------------------")
            # then you either find the existing key that meets that need, or you make a new one on a hook of your choice that opens at least one of the door to that room
            selected_room = room_list[int(user_room_choice) - 1]
            newhook = hooks.insert_one({"keys_id": None})
            newdoor_hook = door_hooks.insert_one({"doors_name": selected_room["doors_name"],
                                                  "hooks_id": newhook.inserted_id})

            print("Creating new key...")

            newkey = keys.insert_one(
                {"requests_id": DBRef("requests", Utilities.get_request_id(db, selected_employee["first_name"],
                                                                           selected_employee["last_name"],
                                                                           int(selected_room["number"]),
                                                                           str(ref_building["name"]),
                                                                           datetime(int(year), int(month), int(date), 0,
                                                                                    0, 0)))})

            # newkey = keys.insert_one({"requests_id": newreq.inserted_id})
            print("Create new key sucessfully")
            print("------------------------------------------------------------------------------")
            print("Granting access...")
            updated_hook = hooks.update_one({"_id": newhook.inserted_id},
                                            {"$set": {"keys_id": newkey.inserted_id}})
            print("Key ", newkey.inserted_id, "that can open room", ref_building["name"], selected_room["number"],
                  "has successfully granted to employee",
                  selected_employee["first_name"], selected_employee["last_name"])

        # capture losing a key
        elif choice == "4":  # capture losing a key

            # checking if any key has already been lost, if yes remove them from the "valid keys"
            # Prompt them for the key request that they want to report lost from the "valid keys"
            counter = 0
            allkey_list = []
            key_list = []
            print("Key list")
            valid_DBRefRequest_id = []

            for key_document in keys_list:
                allkey_list.append(key_document["requests_id"])

            for allkey in allkey_list:
                losts_list = losts.find({})
                for lost_document in losts_list:
                    if allkey == lost_document["requests_id"]:
                        if lost_document["date_reported"] is None:
                            valid_DBRefRequest_id.append(allkey)

            for valid in valid_DBRefRequest_id:
                counter += 1
                # print (valid)
                keys_list = keys.find({})
                for key_document in keys_list:
                    if key_document["requests_id"] == valid:
                        print("Key #", counter, ": ", key_document)
                        key_list.append(key_document)

            print("Please select which key you want to report lost")
            user_key_choice = input()
            print("You selected key: ", key_list[int(user_key_choice) - 1])
            selected_key = key_list[int(user_key_choice) - 1]

            # prompting which employee is holding that key
            ref_request = db.dereference(selected_key["requests_id"])
            ref_employee = db.dereference(ref_request["employees_id_number"])
            print("That currently held by employee: ", ref_employee["first_name"], ref_employee["last_name"])

            # Capture the date and time of the lost. And update it
            print("------------------------------------------------------------------------------")
            print("Please enter year lost: ")
            year = input()
            print("Please enter month:")
            month = input()
            print("Please enter date:")
            date = input()
            losts_list = losts.find({})

            print("------------------------------------------------------------------------------")
            # now update it in lost table
            for lost_document in losts_list:
                if lost_document["requests_id"] == selected_key["requests_id"]:
                    print("updating lost document...")
                    updated_lost = losts.update_one({"_id": lost_document["_id"]},
                                                    {"$set": {
                                                        "date_reported": datetime(int(year), int(month), int(date), 0,
                                                                                  0, 0)}})
                    print("update successfully")

            print("------------------------------------------------------------------------------")
            # prompting the employee that lose the key
            print("Employee", ref_employee["first_name"], ref_employee["last_name"],
                  "will now be charged of $25 for losing key ")
            print(selected_key["_id"])

        # Report all rooms an employee can enter, given the keys that he/she already has
        elif choice == "5":  # Report out all the rooms that an employee can enter, given the keys that he/she already has
            # Prompt for the employee
            employee_list = []
            counter = 0
            print("------------------------------------------------------------------------------")
            print("Employee list")
            for employee_document in employees_list:
                employee_list.append(employee_document)
                counter += 1
                print("Employee #", counter, ": ", employee_document["first_name"], employee_document["last_name"])
            print("Please select an employee you want to check")
            user_employee_choice = input()
            print("You selected employee ", employee_list[int(user_employee_choice) - 1])
            selected_employee = employee_list[int(user_employee_choice) - 1]

            #list rooms they have access to
            requests_selected_employee_has = []
            # print("\nSelected employee has requests: ")
            for request_document in requests_list:
                if db.dereference(request_document["employees_id_number"]) == selected_employee:
                    losts_list = losts.find({})
                    for lost_document in losts_list:
                        if request_document == db.dereference(lost_document["requests_id"]):
                            if (lost_document["date_reported"] is None):
                                returns_list = returns.find({})
                                for return_document in returns_list:
                                    if request_document == db.dereference(return_document["requests_id"]):
                                        if (return_document["return_date"] is None):
                                            requests_selected_employee_has.append(request_document)
                                            # print(request_document)

            # print ("\nHas keys")
            selected_employee_keys =[]
            for emp_req in requests_selected_employee_has:
                for key_document in keys.find({}):
                    ref_request = db.dereference(key_document["requests_id"])
                    if emp_req["_id"] == ref_request["_id"]:
                        selected_employee_keys.append(key_document)
                        # print (key_document)

            # print ("\nWhere they are copied from hooks")
            selected_employee_hooks = []
            for emp_key in selected_employee_keys:
                for hook_document in hooks.find({}):
                    if (emp_key["_id"] == hook_document["keys_id"]):
                        selected_employee_hooks.append(hook_document)
                        # print (hook_document)

            # print ("\nCan open doors")
            selected_employee_doors = []
            for emp_hook in selected_employee_hooks:
                for door_hook_document in door_hooks.find({}):
                    if (emp_hook["_id"] == door_hook_document["hooks_id"]):
                        selected_employee_doors.append(door_hook_document["doors_name"])
                        ref_door = db.dereference(door_hook_document["doors_name"])
                        # print (door_hook_document["doors_name"], " Name: ", ref_door["name"])

            print("------------------------------------------------------------------------------")
            print ("Can open rooms")
            selected_employee_rooms_can_open = []
            for emp_door in selected_employee_doors:
                # print ("emp door", emp_door)
                for room_document in rooms.find({}):
                    # print ("room_document door name", room_document["doors_name"])
                    # ref_door = db.dereference(room_document["doors_name"])
                    if emp_door == room_document["doors_name"]:
                        ref_building = db.dereference(room_document["buildings_name"])
                        room = ref_building["name"] + " " + str(room_document["number"])
                        selected_employee_rooms_can_open.append(room)
                        # print (ref_building["name"], " ", room_document["number"])

            # filter dups and order buildings
            rooms_can_open_removed_dups = []
            for room in selected_employee_rooms_can_open:
                if room not in rooms_can_open_removed_dups:
                    rooms_can_open_removed_dups.append(room)
            rooms_can_open_removed_dups.sort()
            for room in rooms_can_open_removed_dups:
                print(room)


        elif choice == "6":
            print("Deleting a key")
            print("------------------------------------------------------------------------------")
            print("List of keys:")
            counter = 0

            for eachkey in db.keys.find({}):
                print("key #", counter + 1)
                counter += 1

            print("Which key would you like to remove?")

            keychoice = int(input())

            # find that key and change the requests_id to null
            reqidcounter = 0
            for eachkey2 in keys.find({}):
                if reqidcounter + 1 == keychoice:
                    # might need to change method of getting selected key later
                    selectedkey = eachkey2
                    updater = {"$set": {"requests_id": None}}
                    # change request id of current key here
                    db.keys.update_one(eachkey2, updater)
                    #print("request on this key successfully set to null")
                reqidcounter += 1

            # update key id on hook to null

            # remove key id attached to hook
            for eachhook in db.hooks.find({}):
                #print("doing hook loop !")
                if selectedkey["_id"] == eachhook["keys_id"]:
                    # print("this is when u should remove that id from hook")
                    hook_update = {"$set": {"keys_id": None}}
                    db.hooks.update_one(eachhook, hook_update)
                    #print("hook successfully updated")

            # finally, remove the key

            counter2 = 0
            for key_doc2 in keys_list:
                #print("current counter is ", counter2)
                if counter2 + 1 == keychoice:
                    db.keys.delete_one({"_id": key_doc2["_id"]})
                    #print("key successfully deleted")
                counter2 += 1
            print("Key and its references are successfully deleted.")

        elif choice == "7":
            print("Deleting employee...")
            
            print("------------------------------------------------------------------------------")
            curr_request_id = None

            # first show employees and get choice from user
            print("List of employees:")
            employee_counter = 0
            for eachemployee in db.employees.find({}):
                employee_counter += 1
                print("Employee #", employee_counter, ":", eachemployee["first_name"], eachemployee["last_name"])

            print("Which employee would you like to delete?")

            employee_choice = input()
            selectcounter = 0
            for selectemp in db.employees.find({}):
                if selectcounter + 1 == int(employee_choice):
                    #print("employee successfully chosen")
                    selected_employee = selectemp
                selectcounter += 1

            # now, find request_id that connects to selected employee in request table
            list_requests = []
            # from there, find key with that request id and set request id to null in key table
            for each_request in db.requests.find({}):
                employee_ref = db.dereference(each_request["employees_id_number"])
                if employee_ref["_id"] == selected_employee["_id"]:
                    curr_request_id = each_request["_id"]
                    list_requests.append(curr_request_id)
                    # found connection between request and employee by this point

            # update keys that correspond to those employees
            for any_key in db.keys.find({}):

                req_ref = db.dereference(any_key["requests_id"])
                for i in range(len(list_requests)):

                    if req_ref["_id"] == list_requests[i]:
                        keys_updater = {"$set": {"requests_id": None}}
                        db.keys.update_one(any_key, keys_updater)

            # delete corresponding requests from employee
            for gonerequest in db.requests.find({}):
                employe_ref = db.dereference(gonerequest["employees_id_number"])

                if selected_employee["_id"] == employe_ref["_id"]:
                    # print("you have found a deletion point")
                    db.requests.delete_one({"_id": gonerequest["_id"]})

            # finally, delete the employee
            for goneemployee in db.employees.find({}):
                if goneemployee["_id"] == selected_employee["_id"]:
                    db.employees.delete_one({"_id": goneemployee["_id"]})

            print("Employee successfully deleted")

        elif choice == "8":
            print("Adding new door...")

            # present the hooks to user
            print("List of Hooks:")
            hook_count = 1
            for hookdoc in db.hooks.find({}):
                print("Hook #", hook_count, " ", hookdoc["_id"])
                hook_count += 1

            print("Which hook do you want to choose?")

            hook_choice = input()

            # first find the current id of a selectedhook
            hook_count2 = 0
            for findhook in db.hooks.find({}):
                if hook_count2 == int(hook_choice):
                    # set that to selected hook
                    selected_hook = findhook
                    # now go to door hooks and find which doors match that
                    for finddoorhook in db.door_hooks.find({}):
                        if selected_hook["_id"] == finddoorhook["hooks_id"]:
                            # set finddoorhook to the one we want
                            selected_door_hook = finddoorhook
                            # print("door_hook is successfully found here")
                hook_count2 += 1

            # since we know which door_hook we got, we can find the door_name and id by dbreference
            selected_door = db.dereference(selected_door_hook["doors_name"])

            # go through rooms and see if theres duplicates for door ids on multiple rooms
            # create list of qualified room numbers for the selected door and the above is true ^

            list_qualified_rooms = []
            list_qualified_buildings = []

            for each_room in db.rooms.find({}):
                curr_room_door_id = db.dereference(each_room["doors_name"])

                if curr_room_door_id["_id"] == selected_door["_id"]:
                    building_refer = db.dereference(each_room["buildings_name"])
                    list_qualified_buildings.append(building_refer["_id"])
                    # append it to list since there may be multiple
                    list_qualified_rooms.append(curr_room_door_id["_id"])
                    

            #present buildings to user
            print("Here are the possible buildings for your hook")
            build_count = 0
            for each_building in db.buildings.find({}):
                build_count += 1
                print("Building #", build_count, ": ", each_building["name"])

            print("Which building would you like to choose?")

            building_choice = input()

            #get the building name and id for later use
            build_count2 = 0
            for new_building in db.buildings.find({}):
                build_count2 += 1
                if build_count2 == int(building_choice):
                    # set that to building choice
                    selected_building_id = new_building["_id"]
                    selected_buildingname = new_building["name"]

            print("Available rooms in that building:")
            list_rooms = []
            list_room_number = []
            outputcount = 0
            # compare rooms and building to get list of available rooms
            for new_rooms in db.rooms.find({}):
                newbuildref = db.dereference(new_rooms["buildings_name"])
                if newbuildref["_id"] == selected_building_id:
                    outputcount += 1
                    list_rooms.append(new_rooms["_id"])
                    list_room_number.append(new_rooms["number"])
                    print("Room #", outputcount, ":", new_rooms["number"])

            print("Which room would you like to choose?")

            room_choice = input()
            roomchoicecount = 0
            for choosing in list_rooms:
                roomchoicecount += 1
                if int(room_choice) == roomchoicecount:
                    selected_room_id = choosing

            #find selected room number here too
            roomchoicecount2 = 0
            for choosing2 in list_room_number:
                roomchoicecount2 += 1
                if int(room_choice) == roomchoicecount2:
                    selected_room_number = choosing2


            # present out possible doors here:
            doordoccount = 0
            for doordocs in db.doors.find({}):
                doordoccount += 1
                print("Door Choice #", doordoccount, ": ", doordocs["name"])

            print("Which door would you like to add to your room?")

            door_choice = input()

            # get door id of choice

            doorchoicecount = 0
            for doorchoice in db.doors.find({}):
                doorchoicecount += 1
                if doorchoicecount == int(door_choice):
                    #selecteddoor_id = doorchoice["_id"]
                    selecteddoor_name = doorchoice["name"]

            #add room with the selected door

            insertedroomdata = {"number": selected_room_number,
                                "buildings_name": DBRef("buildings", Utilities.get_building_name(db, selected_buildingname)), "doors_name": DBRef("doors", Utilities.get_door_name(db, selecteddoor_name))}

            x = db.rooms.insert_one(insertedroomdata)

            #create door_hook here

            inserteddoorhookdata = {"doors_name": DBRef("doors", Utilities.get_door_name(db, selecteddoor_name)), "hooks_id": selected_hook["_id"]}

            y = db.door_hooks.insert_one(inserteddoorhookdata)

            print("Door successfully added.")


        #update an access request to movie it to a new employee
        elif choice == "9":
            #Prompt for the old employee
            employee_list = []
            counter = 0
            print("------------------------------------------------------------------------------")
            print("Employee list")
            for employee_document in employees.find({}):
                employee_list.append(employee_document)
                counter += 1
                print("Employee #", counter, ": ", employee_document["first_name"], employee_document["last_name"])
            print("Please select an old employee")
            user_employee_choice = input()
            print("You selected employee ", employee_list[int(user_employee_choice) - 1])
            selected_employee = employee_list[int(user_employee_choice) - 1]


            #Prompt which access (by room) of the old employee that want to change
            print("------------------------------------------------------------------------------")
            print ("Who has requests")
            request_list = []
            old_employee_requests = []
            counter = 0
            for request_document in requests.find({}):
                ref_employee = db.dereference(request_document["employees_id_number"])
                if selected_employee["_id"] == ref_employee["_id"]:
                    old_employee_requests.append(request_document)
                    counter += 1
                    ref_room = db.dereference(request_document["rooms_id"])
                    ref_building = db.dereference(ref_room["buildings_name"])
                    print ("request #",counter ,": ", ref_building["name"], ref_room["number"] ," (request id: ", request_document["_id"], ")")
            print("Please select a request you wish to change")
            user_request_choice = input()
            print("You selected request ", old_employee_requests[int(user_request_choice) - 1])
            selected_request = old_employee_requests[int(user_request_choice) - 1]




            #Prompt for the new employee
            print("------------------------------------------------------------------------------")
            employee_list = []
            counter = 0
            print("Employee list")
            for employee_document in employees.find({}):
                if employee_document["_id"] != selected_employee["_id"]:
                    employee_list.append(employee_document)
                    counter += 1
                    print("Employee #", counter, ": ", employee_document["first_name"], employee_document["last_name"])
            print("Please select a new employee you wish to change to")
            user_employee_choice = input()
            print("You selected employee ", employee_list[int(user_employee_choice) - 1])
            selected_employee = employee_list[int(user_employee_choice) - 1]


            #update the request
            print("------------------------------------------------------------------------------")
            print ("Updating request...")
            updated_request = requests.update_one({"_id": selected_request["_id"]},
                                            {"$set": {"employees_id_number": DBRef("employees", Utilities.get_employee_id(db, selected_employee["first_name"], selected_employee["last_name"]))}})
            print ("Update request successfully")

        # report all employeees who can get into a room
        elif choice == "10":

            # prompt which room want to check
            room_list = []
            counter = 0
            print("------------------------------------------------------------------------------")
            print("Room list")
            for room_document in rooms_list:
                room_list.append(room_document)
                counter += 1
                ref_building = db.dereference(room_document["buildings_name"])
                print("Room #", counter, ": ", ref_building["name"], room_document["number"], "   (room id: ",
                      room_document["_id"], ")")
            print("Please select a room that you wish to check ")
            user_room_choice = input()
            print("You selected room ", room_list[int(user_room_choice) - 1])
            selected_room = room_list[int(user_room_choice) - 1]

            selected_ref_door = db.dereference(selected_room["doors_name"])

            selected_hooks = []
            for door_hook_document in door_hooks.find({}):
                if door_hook_document["doors_name"] == selected_room["doors_name"]:
                    selected_hooks.append(door_hook_document["hooks_id"])

            selected_keys = []
            for selected_hook in selected_hooks:
                for hook_document in hooks.find({}):
                    if hook_document["_id"] == selected_hook:
                        selected_keys.append(hook_document["keys_id"])

            selected_requests = []
            for selected_key in selected_keys:
                for key_document in keys.find({}):
                    if key_document["_id"] == selected_key:
                        selected_requests.append(db.dereference(key_document["requests_id"]))

            selected_employees = []
            for selected_request in selected_requests:
                for request_document in requests.find({}):
                    if (request_document["_id"] == selected_request["_id"]):
                        ref_employee = db.dereference(request_document["employees_id_number"])
                        employee_name = ref_employee["first_name"] + " " + ref_employee["last_name"]
                        # print (ref_employee["first_name"] + ref_employee["last_name"])
                        selected_employees.append(employee_name)

            print("------------------------------------------------------------------------------")
            ref_building = db.dereference(selected_room["buildings_name"])
            print("People can enter room", ref_building["name"], selected_room["number"], "are")
            selected_employees_removed_dups = []
            for employee_name in selected_employees:
                if employee_name not in selected_employees_removed_dups:
                    selected_employees_removed_dups.append(employee_name)
            selected_employees_removed_dups.sort()
            for employee_name in selected_employees_removed_dups:
                print(employee_name)


        else:
            print("invalid input")

        print("------------------------------------------------------------------------------")
        print()
        print("Menu System:")
        print()
        print("1: Create a new Key")
        print("2: Request access to a room by a given employee")
        print("3: Capture issue of a key to an employee")
        print("4: Capture losing a key")
        print("5: Report all rooms an employee can enter, given the keys that he/she already has")
        print("6: Delete a key")
        print("7: Delete an employee")
        print("8: Add new door that can be opened by existing hook")
        print("9: Update access request to move it to a new employee")
        print("10: Report out all the employees who can get into a room")
        print("Type 0 to exit out")
        print()
        print("Please input the number you want: ")
        print()
        choice = input()

    print("Exiting...")
