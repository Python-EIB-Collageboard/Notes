from flask import Flask, request

# Initialize an instance of a flask app
app = Flask(__name__)

# A simple flask app that serves notes from a hardcoded list 
_notes = [
    {"id": "1", "title": "groceries", "body": "milk, eggs"},
    {"id": "2", "title": "idea", "body": "flask is just express, in python"},
    {"id": "3", "title": "todo", "body": "finish demo"}
]

# Express JS example below 

# app.get('/notes', (req, res) => {
#     const limit = req.query.limit;
#     res.status(200).json({ notes: [] });
# });

# Lets create our first route, in python
# Remember: this is basically express

# This method is really simple - get ALL the notes in our collection
@app.route('/notes', methods=['GET'])
def list_notes():
    # If we wanted to fully realize the equvilant to the above Express endpoint
    # and engage with the limit argument. Arguments come in as k-v pairs, we can 
    # ask for one by the key
    limit = request.args.get('limit', type=int)
    
    # So IF the user sends in a limit argument (i.e. limit above is not null)
    # THEN get us positions 1-Limit (exclusive) from our _notes list
    # otherwise, if limit is null, just return the whole list
    data = _notes[:limit] if limit else _notes
    
    # Returning data - either the limited slice with the argument OR the whole thing
    return {"notes": data}

# Lets use the "short hand"/modern flask route decorator
@app.post('/notes')
def create_note():
    # request.get_json() -> Express req.body 
    # If theres no request body this holds None
    payload = request.get_json(silent=True)
    
    if not payload:
        return {"error": "JSON body required"}, 400 # If payload is None, send back an error
    
    # Creating our note
    # Inferring the note ID from the length of the list
    note = {"id": f"{len(_notes) + 1}", **payload}
    
    _notes.append(note)
    
    # Because this is python, we can do a Tuple return
    # Equivalent to:
    # res.status(201).json(note)
    return note, 201

# If we run this file directly
# Start our flask app, set debug to true, expose on port 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)