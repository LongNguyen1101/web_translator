# Turn off FutureWarning
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from translate import translate
from config import get_config

app = Flask(__name__)
CORS(app)

# Khởi tạo Swagger
swagger = Swagger(app)

@app.route('/translate', methods=['POST'])
def translate_api():
    """
    Translate Text
    ---
    tags:
      - Translation
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - translation_from_to
            - text
          properties:
            translation_from_to:
              type: string
              description: Language source
              example: 'en-vi'
            text:
              type: string
              description: Text to be translated
              example: "Hello"
    responses:
      200:
        description: Translation successful
        schema:
          type: object
          properties:
            Translated text:
              type: string
              description: Translated output
              example: "Xin chào"
      400:
        description: Input text is missing
      500:
        description: Internal server error
    """
    try:
        data = request.get_json()
        translation_from_to = data.get('translation_from_to', '')
        input_text = data.get('text', '')

        if not input_text:
            return jsonify({"error": "No input text provided"}), 400

        config = get_config()
        if translation_from_to == 'vi-en':
          config['datasource'] = 'harouzie/vi_en-translation'
          config['lang_src'] = 'Vietnamese'
          config['lang_tgt'] = 'English'
        else:
          config['datasource'] = 'harouzie/en_vi-translation'
          config['lang_src'] = 'English'
          config['lang_tgt'] = 'Vietnamese'
          
        translated_text = translate(input_text, config)

        return jsonify({'Translated text': translated_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
