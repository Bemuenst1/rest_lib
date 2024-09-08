from flask import Flask, request, jsonify

def route(path, methods=['GET'], params=[]):
    def decorator(func):
        func.path = path
        func.methods = methods
        func.params = params
        return func
    return decorator

class API(object):
    app = Flask(__name__)

    def __new__(cls, api_keys=None, api_handler=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(API, cls).__new__(cls)
            cls.instance.init(api_keys, api_handler)
        return cls.instance
    
    @staticmethod
    def start():
        API.app.run(debug=True, threaded=True, host='0.0.0.0')
    
    @staticmethod
    def stop(self):
        API.app.shutdown()

    def init(self, api_keys, api_handler):
        self.keys = api_keys
        self.handler = api_handler

        # initialize routes
        for func_name in dir(self.handler):
            func = getattr(self.handler, func_name)

            if callable(func) and hasattr(func, 'path'):
                self.add_route(func.path, func, func.methods, func.params)

    
    def add_route(self, path, func, methods, params):
        if not path:
            print("[Error]: Invalid route configuration")
            return

        @self.app.route(path, methods=methods, endpoint=func.__name__)
        def route_handler(func=func, params=params):
            # API key validation
            if not self.validate_key():
                return self.error("Invalid API key")
            
            # collect arguments from parameters
            args = {param: request.args.get(param) for param in params}
            if None in args.values():
                return self.error("Missing required parameters")
            
            # call handler function
            return jsonify(func(**args))

    def validate_key(self):
        request_key = request.headers.get('key', None)
        if not request_key or not request_key in self.keys:
            return False
        return True
        
    def error(self, message):
        print(f"[Error]: {message}")
        return jsonify({"error": message}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404