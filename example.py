import json

from rest import API, route
from threading import Thread

class Handler:
    @route("/hello", ["GET"], ["name"])
    def hello(self, name):
        return {"message": f"Hello, {name}!"}
    
    @route("/goodbye", ["GET"], ["name"])
    def goodbye(self, name):
        return {"message": f"Goodbye, {name}!"}

def load_config():
    with open("api_config.json", "r") as f:
        return json.loads(f.read())

def dummy_worker():
    while True:
        print(input("Enter something: "))

def main():
    #dummy_thread = Thread(target=dummy_worker)
    #dummy_thread.start()

    API(api_config=load_config(), handler=Handler()).start()

    #dummy_thread.join()

if __name__ == "__main__":
    main()