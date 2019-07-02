from simplerr.web import web

@web('/api-v2/users/<id>')
def get(request, id):
    return {'id': id, 'name': 'John Doe'}

