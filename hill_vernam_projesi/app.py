from flask import Flask, render_template, request, jsonify
import kutuphanesiz_versiyon
import kutuphaneli_versiyon
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    text = data.get('text', '')
    mode = data.get('mode', 'kutuphanesiz')
    
    try:
        if mode == 'kutuphaneli':
            res = kutuphaneli_versiyon.web_icin_sifrele(text)
            return jsonify(res)
        elif mode == 'kutuphanesiz':
            res = kutuphanesiz_versiyon.web_icin_sifrele(text)
            return jsonify(res)
        elif mode == 'ikisi':
            res1 = kutuphaneli_versiyon.web_icin_sifrele(text)
            res2 = kutuphanesiz_versiyon.web_icin_sifrele(text)
            
            # İkisini yan yana döndürüyoruz. Ön uç (frontend) bunu ayıracak.
            return jsonify({
                "ikili_mod": True,
                "kutuphaneli": res1,
                "kutuphanesiz": res2
            })
        else:
            return jsonify({"error": "Geçersiz mod"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/source', methods=['GET'])
def source():
    mode = request.args.get('mode', 'kutuphanesiz')
    filename = 'kutuphaneli_versiyon.py' if mode == 'kutuphaneli' else 'kutuphanesiz_versiyon.py'
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify({"source": f.read()})
    except Exception as e:
        return jsonify({"error": "Dosya okunamadı: " + str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
