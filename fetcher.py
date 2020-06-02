import requests
import json

From = input("From: ")
to = input("To: ")
dod = int(input("Enter the date of departure (in YYYYMMDD format): "))
adults = int(input("Enter the number of adults: "))
children = int(input("Enter the number of children: "))
infants = int(input("Enter the number of infants: "))
sc = input(
            "Enter the code for the seating class you would like to book: \n1.Business (CODE: B) \n2.Economy (CODE: E)\n")
print("PLEASE WAIT YOUR REQUEST IS BEING PROCESSED.................")
print("")
response = requests.get("http://developer.goibibo.com/api/search/?app_id=1a7d2727&app_key=a7e093b62d62716c630ffe3017553829&format=json&source={FROM}&destination={TO}&dateofdeparture={DOD}&seatingclass={sc}&adults={ADULTS}&children={CHILDREN}&infants={INFANTS}&counter=100".format(FROM=From, TO=to, DOD=dod, sc=sc, ADULTS=adults, CHILDREN=children, INFANTS=infants))


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(response.json())
for q in response.json()['data']['onwardflights']:
        print("Airline: " + q['airline'])
        print("Arrival date: ", end="")
        for d in range(0, 9):
            print(q['arrdate'][d], end="")
        print("")
        print("Arrival terminal: " + q['arrterminal'])
        print("Arrival time: " + q['arrtime'])
        print("Departure terminal: " + q['depterminal'])
        print("Departure time: " + q['deptime'])
        print("Duration: " + q['duration'])
        print("Destination: " + q['destination'])
        print("Total Base Fare: " + str(q['fare']['totalfare']))
        print("Flight code: " + q['flightcode'])
        print("Flight Number: " + q['flightno'])
        print("Seats Available: " + q['seatsavailable'])
        print("Refundable status: " + q['warnings'])
        print("")

