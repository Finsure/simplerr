from simplerr.web import web

@web('/api-v2/pets/<id>')
def get(request, id):
    return {'id': id, 'name': 'Fido'}

