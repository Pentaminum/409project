from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from ..cli import CLI

# Get the absolute path to the static directory
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')

app = Flask(__name__, static_folder=static_dir, static_url_path='')
CORS(app)

cli = CLI()
cli.initialize_system()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('message', '')
    
    try:
        response = cli.chat_interface.chat(query)
        return jsonify({
            'answer': response['answer'],
            'sources': [
                {
                    'source': doc.metadata['source'],
                    'directory': doc.metadata['directory'],
                    'description': doc.metadata.get('description', '')
                }
                for doc in response.get('source_documents', [])
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)