from flask import Flask
from endpoints.Routes import registerEndpoint

main = Flask(__name__)


#links all the endpoints to the API
registerEndpoint(main)

#executor
if __name__ == '__main__':
    main.run(debug=True,port=5000)