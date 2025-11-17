from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import random

app = Flask(__name__)
CORS(app)

# Load zodiac data
def load_zodiacs():
    with open('data/zodiacs.json', 'r') as f:
        return json.load(f)

# Route to get all zodiacs
@app.route('/api/zodiacs', methods=['GET'])
def get_all_zodiacs():
    try:
        zodiacs = load_zodiacs()
        return jsonify({
            'success': True,
            'data': zodiacs,
            'count': len(zodiacs)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Route to get a specific zodiac by name
@app.route('/api/zodiacs/<name>', methods=['GET'])
def get_zodiac(name):
    try:
        zodiacs = load_zodiacs()
        zodiac = next((z for z in zodiacs if z['name'].lower() == name.lower()), None)
        
        if not zodiac:
            return jsonify({
                'success': False,
                'error': f'Zodiac sign "{name}" not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': zodiac
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Route to search zodiacs by name or element
@app.route('/api/zodiacs/search', methods=['GET'])
def search_zodiacs():
    try:
        query = request.args.get('q', '').lower()
        element = request.args.get('element', '').lower()
        
        if not query and not element:
            return jsonify({
                'success': False,
                'error': 'Please provide search query or element filter'
            }), 400
        
        zodiacs = load_zodiacs()
        results = []
        
        for zodiac in zodiacs:
            if query and query in zodiac['name'].lower():
                results.append(zodiac)
            elif element and zodiac['element'].lower() == element:
                results.append(zodiac)
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Route to get random zodiac
@app.route('/api/zodiacs/random', methods=['GET'])
def get_random_zodiac():
    try:
        zodiacs = load_zodiacs()
        zodiac = random.choice(zodiacs)
        
        return jsonify({
            'success': True,
            'data': zodiac
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Route to get all elements
@app.route('/api/elements', methods=['GET'])
def get_elements():
    try:
        zodiacs = load_zodiacs()
        elements = list(set(z['element'] for z in zodiacs))
        
        return jsonify({
            'success': True,
            'data': sorted(elements)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'Zodiac Explorer API is running'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
