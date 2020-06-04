import os
from pocketsphinx.pocketsphinx import Decoder
from pydub import AudioSegment
from urllib.request import urlopen

MODELDIR = "en-us-adapt"
RESULT = "Result"

def ConvertMp3ToWav(srcPath):
    sound = AudioSegment.from_mp3(srcPath)
    dst = '{0}.wav'.format(srcPath.rsplit('.', 1)[0])
    sound.export(dst, format="wav")
    return dst

def ConvertFlacToWav(srcPath):
    sound = AudioSegment.from_file(srcPath)
    dst = '{0}.wav'.format(srcPath.rsplit('.', 1)[0])
    sound.export(dst, format="wav")
    return dst

def WriteFileFromLink(srcUrl):
  src = urlopen(srcUrl)
  getFileName = srcUrl.rsplit('/', 1)[1]
  with open('./{0}/{1}'.format(RESULT,getFileName),'wb') as output:
    output.write(src.read())
  return '{0}/{1}'.format(RESULT,getFileName)

def Process(srcPath):
    config = Decoder.default_config()
    config.set_string('-hmm', MODELDIR)
    config.set_string('-lm', 'en-us.lm.bin')
    config.set_string('-dict', 'cmudict-en-us.dict')
    decoder = Decoder(config)

    stream = open(srcPath, 'rb')

    buf = bytearray(1024)
    with stream as f:
        decoder.start_utt()
        while f.readinto(buf):
            decoder.process_raw(buf, False, False)
        decoder.end_utt()
    #print('Best hypothesis segments:', decoder.hyp().hypstr)
    return decoder.hyp().hypstr