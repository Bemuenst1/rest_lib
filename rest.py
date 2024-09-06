from flask import Flask, request, jsonify

class API(object):
    app = Flask(__name__)

    def __new__(cls, api_config=None, handler=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(API, cls).__new__(cls)
            cls.instance.init(api_config, handler)

        return cls.instance
    
    @staticmethod
    def start():
        API.app.run(debug=True, threaded=True, host='0.0.0.0')

    def init(self, api_config, handler):
        self.config = api_config
        self.handler = handler

        self.api_keys = set(self.config.get('api_keys', []))

        # 404 route
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({"error": "Not found"}), 404

        # initialize routes
        for route in self.config.get('routes', []):
            self.add_route(route)
    
    def add_route(self, route):
        # route configuration
        path = route.get('path', None)
        func_name = route.get('func', None)
        methods = route.get('methods', ['GET'])
        params = route.get('params', [])

        if not path or not func_name:
            print("[Error]: Invalid route configuration")
            return

        @self.app.route(path, methods=methods, endpoint=func_name)
        def route_handler(func_name=func_name, params=params):
            # API key validation
            if not self.validate_key():
                return self.error("Invalid API key")
            
            # load handler function
            func = getattr(self.handler, func_name, None)
            if not func:
                return self.error("Invalid handler function")
            
            # collect arguments from parameters
            args = {param: request.args.get(param) for param in params}
            if None in args.values():
                return self.error("Missing required parameters")
            
            # call handler function
            return jsonify(func(**args))

    def validate_key(self):
        request_key = request.headers.get('key', None)
        if not request_key or not request_key in self.api_keys:
            return False
        return True
        
    def error(self, message):
        print(f"[Error]: {message}")
        return jsonify({"error": message}), 400