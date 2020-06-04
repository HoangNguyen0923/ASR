from flask import Response, Flask, request
from SpeechToText import ConvertFlacToWav, ConvertMp3ToWav, Process, WriteFileFromLink
import json

app = Flask(__name__)

@app.route('/api/analyze', methods=['POST'])

def api_speech_analyze():
  srcUrl = request.form['file']
  
  src = WriteFileFromLink(srcUrl)
  #if (srcUrl.startswith('http')):
  #  src = WriteFileFromLink(srcUrl)
  #else:
  #  src = srcUrl

  if src.rsplit('.', 1)[1] == 'flac':
    src = ConvertFlacToWav(src)
  elif src.rsplit('.', 1)[1] == 'mp3':
    src = ConvertMp3ToWav(src)

  result = Process(ConvertFlacToWav(src))

  data = {
    'result' : result
  }
  js = json.dumps(data)

  resp = Response(js, status=200, mimetype='application/json')

  return resp

if __name__ == "__main__":
    app.run()
  