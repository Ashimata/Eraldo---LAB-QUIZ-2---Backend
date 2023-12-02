from flask import Flask, render_template, request, flash, redirect, url_for , jsonify
import mysql.connector
import secrets
from flask_cors import CORS


app = Flask(__name__,  static_folder='Python HTML\test-project', static_url_path='/App.js')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,CREATE')
    return response

CORS(app)

@app.route('/api/voters1', methods=['GET'])
def get_data():
    data = {"message": "Good Afternoon!"}
    return jsonify(data)


app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route('/api/voters1', methods=['POST'])
def create_voter():
    name = request.form['name']
    province = request.form['province']
    city = request.form['city']
    barangay = request.form['barangay']
    email = request.form['email']
    age = request.form['age']
    address = request.form['address']

    cnx = mysql.connector.connect(
        user=' root',
        password='',
        host='localhost',
        database='db_voters_registration'
    )

    cursor = cnx.cursor()
    cursor.execute('INSERT INTO voters1 (name, province, city, barangay, email, age, address) VALUES (%s, %s, %s, %s, '
                   '%s, %s, %s)', (name, province, city, barangay, email, age, address))
    cnx.commit()
    cursor.close()
    cnx.close()

    flash('Voter added successfully', 'success')
    return redirect(url_for('display_voter'))

@app.route('/api/voters1/display', methods=['GET'])
def display_voter():

    cnx = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='db_voters_registration'
    )

    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM voters1')
    data = cursor.fetchall()
    cursor.close()
    cnx.close()

    return jsonify(data)

@app.route('/api/voters1/update/<id>', methods=['GET', 'POST'])
def update_voter(id):
    try:
        # Establish a connection to the MySQL server
        cnx = mysql.connector.connect(
            user='root',
            password='',
            host='localhost',
            database='db_voters_registration'
        )

        cursor = cnx.cursor()

        if request.method == 'POST':
            # Get the JSON data from the request
            data = request.json

            # Extract the fields from the data
            name = data['name']
            province = data['province']
            city = data['city']
            barangay = data['barangay']
            email = data['email']
            age = data['age']
            address = data['address']

            print(f"Received data for update: name={name}, email={email}, age={age}, address={address}, province={province} city={city} barangay={barangay}, " )

            # Execute the update query with the values
            query = 'UPDATE voters1 SET name=%s, province=%s, city=%s, barangay=%s, email=%s, age=%s, address=%s WHERE id=%s'
            values = (name, province, city, barangay, email, age, address, id)

            cursor.execute(query, values)
            cnx.commit()

            print(f"Voter updated successfully with id={id}")

            # Return a JSON response with a success message and a status code of 200
            return jsonify({'message': 'Voter updated successfully'}), 200

        else:
            # Execute the select query with the id
            cursor.execute('SELECT * FROM voters1 WHERE id=%s', (id,))
            data = cursor.fetchone()
            cursor.close()
            cnx.close()

            print(f"Fetched data for id={id}: {data}")

            # Return a JSON response with the data and a status code of 200
            return jsonify(data), 200

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        # Return a JSON response with an error message and a status code of 500
        return jsonify({'error': str(err)}), 500

    except Exception as e:
        print(f"Error: {e}")
        # Return a JSON response with an error message and a status code of 500
        return jsonify({'error': str(e)}), 500

@app.route('/api/voters1/delete/<id>', methods=['GET'])
def delete_voter(id):
    # Establish a connection to the MySQL server
    cnx = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='db_voters_registration'
    )

    cursor = cnx.cursor()
    cursor.execute('DELETE FROM voters1 WHERE id=%s', (id,))
    cnx.commit()
    cursor.close()
    cnx.close()

    flash('Voter deleted successfully', 'success')
    return jsonify({'message': 'Voter deleted successfully'})

@app.route('/api/voters1/search', methods=['GET', 'POST'])
def search_voter():
    if request.method == 'POST':
        data = request.get_json()
        search = data['search']

        cnx = mysql.connector.connect(
            user='root',
            password='',
            host='localhost',
            database='db_voters_registration'
        )

        cursor = cnx.cursor()
        cursor.execute('SELECT * FROM voters1 WHERE name LIKE %s', (f'%{search}%',))
        data = cursor.fetchall()
        cursor.close()
        cnx.close()

        return jsonify(data)
    else:
        return render_template('search.html')



if __name__ == '__main__':
    app.run(debug=True)


