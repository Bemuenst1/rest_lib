from rest import API, route

class Handler:
    
    @route("/hello", ["GET"], ["name"])
    def hello(self, name):
        return {"message": f"Hello, {name}!"}

    @route("/goodbye", ["GET"], ["name"])
    def goodbye(self, name):
        return {"message": f"Goodbye, {name}!"}

    @route("/test")
    def test(self):
        return "test"

def main():

    api_keys = ["12345678", "abcdefgh"]	

    API(api_keys, api_handler=Handler()).start()

if __name__ == "__main__":
    main()