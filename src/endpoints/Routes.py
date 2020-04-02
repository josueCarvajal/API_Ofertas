from endpoints.Business import business_endpoint
from endpoints.User import user_endpoint
from endpoints.Post import post_endpoint

def registerEndpoint(main):
    main.register_blueprint(user_endpoint, url_prefix='/user')
    main.register_blueprint(business_endpoint, url_prefix='/business')
    main.register_blueprint(post_endpoint, url_prefix='/post')

