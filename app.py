from flask import Flask, request
import subprocess
import arduino_serial
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

#cribbed from https://github.com/amperka/ino/blob/f23ee5cb14edc30ec087d3eab7b301736da42362/ino/commands/upload.py
def load_hex(hexfile):
    subprocess.call('avrdude -p atmega2560 -P /dev/ttyACM0 -c wiring -b 115200 -D -U flash:w:%s:i' % hexfile,shell=True)

@app.route('/test')
def test_load():
    hexfile='/home/pi/test_sketch2/.build/mega2560/firmware.hex'
    load_hex(hexfile)

    return 'loaded'
@app.route('/test2')
def test_load2():
    hexfile='/home/pi/test_sketch/.build/mega2560/firmware.hex'
    load_hex(hexfile)

    return 'loaded'
@app.route('/color',methods=['GET'])
def color():
    hue=request.args.get('hue')
    arduino_serial.send(bytes(chr(int(hue))))
    return 'loaded'



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
