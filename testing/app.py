from flask import Flask, jsonify
from flask_cors import CORS

# initialize a flask application (app)
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# ... your existing Flask

# add an api endpoint to flask app
@app.route('/api/kiruthic')
def get_kiruthic():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Kiruthic",
        "LastName": "Selvakumar",
        "DOB": "October 25",
        "Residence": "San Diego",
        "Email": "kiruthic.selvakumar@gmail.com",
        "Owns_Cars": ["BMW, Tesla"]
    })

    return jsonify(InfoDb)

@app.route('/api/aadi')
def get_aadi():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Aadi",
        "LastName": "Bhat",
        "DOB": "July 8",
        "Residence": "San Diego",
        "Email": "aadibhat09@gmail.com",
        "Owns_Cars": ["Lexus", "Tesla", "Honda"]
    })

    return jsonify(InfoDb)

@app.route('/api/aaditya')
def get_aaditya():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Aaditya",
        "LastName": "Taleppady",
        "DOB": "May 4",
        "Residence": "San Diego",
        "Email": "aadityar.taleppady@gmail.com",
        "Owns_Cars": ["Lamborghini, Tesla, Mercedes"]
    })

    return jsonify(InfoDb)

# add an api endpoint to flask app
@app.route('/api/derek')
def get_derek():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Derek",
        "LastName": "Kang",
        "DOB": "April 13",
        "Residence": "San Diego",
        "Email": "derek.j.kang@gmail.com",
        "Owns_Cars": ["Lamborghini, Tesla, Mercedes"]
    })

    return jsonify(InfoDb)

@app.route('/api/arhaan')
def get_arhaan():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Arhaan",
        "LastName": "Memon",
        "DOB": "August 13",
        "Residence": "San Diego",
        "Email": "arhaansporty@gmail.com",
        "Owns_Cars": ["Honda, Tesla, Ferrari"]
    })

    return jsonify(InfoDb)

# add an HTML endpoint to flask app
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Group Members</title>
    </head>
    <body>
        <h2>Group Members Data</h2>
        <table border="1" style="width: 100%; text-align: left;">
            <thead>
                <tr>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Date of Birth</th>
                    <th>Residence</th>
                    <th>Email</th>
                    <th>Owns Cars</th>
                </tr>
            </thead>
            <tbody>
    """
    
    # List of API endpoints
    api_endpoints = [
        '/api/kiruthic',
        '/api/tarun',
        '/api/rohan',
        '/api/arhaan',
        '/api/derek',
        '/api/aadi',
        '/api/aaditya',
    ]
    
    # Fetch data from APIs and populate the table
    for endpoint in api_endpoints:
        # Fetch data from the endpoint
        try:
            response = app.test_client().get(endpoint)
            data = response.get_json()
            if data:  # Iterate over the data if it exists
                for member in data:
                    html_content += f"""
                    <tr>
                        <td>{member['FirstName']}</td>
                        <td>{member['LastName']}</td>
                        <td>{member['DOB']}</td>
                        <td>{member['Residence']}</td>
                        <td>{member['Email']}</td>
                        <td>{', '.join(member['Owns_Cars'])}</td>
                    </tr>
                    """
        except Exception as e:
            html_content += f"<tr><td colspan='6'>Error fetching data from {endpoint}: {str(e)}</td></tr>"
    
    # Close the table and body
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    return html_content

if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:3003
    app.run(port=8887)