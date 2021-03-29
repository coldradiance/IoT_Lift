from flask import Flask, render_template,request, redirect, url_for
from pyduino import *
import time
import datetime

app = Flask(__name__)

# initialize connection to Arduino
# if your arduino was running on a serial port other than '/dev/ttyACM0/'
# declare: a = Arduino(serial_port='/dev/ttyXXXX')
a = Arduino() 
time.sleep(3)

# declare the pins we're using
LED_PIN = 2

ANALOG_PIN = 23

# initialize the digital pin as output
a.set_pin_mode(LED_PIN,'O')

print('Arduino initialized')


# we are able to make 2 different requests on our webpage
# GET = we just type in the url
# POST = some sort of form submission like a button
@app.route('/', methods = ['POST','GET'])
def hello_world():

    # variables for template page (templates/index.html)
    status = ''
    status_time = ''

    # if we make a post request on the webpage aka press button then do stuff
    if request.method == 'POST':

        # if we press the turn on button
        if request.form['submit'] == '1':
            status = 'Двигатель включен, едет на первый этаж'
            status_time = str(datetime.datetime.now())

            # turn on LED on arduino
            a.digital_write(LED_PIN,1)
            # a.PWM_write(100)

        # if we press the turn off button
        elif request.form['submit'] == '2':
            status = 'Двигатель включен, едет на 2й этаж'
            status_time = str(datetime.datetime.now())
            # turn off LED on arduino
            a.digital_write(LED_PIN, 0)
            # a.PWM_write(100)
        elif request.form['submit'] == 'Остановить':
            status = 'Двигатель выключен'
            status_time = str(datetime.datetime.now())
            # turn off LED on arduino
            a.digital_write(LED_PIN, 0)
            # a.PWM_write_stop()


        else:
            pass

    # read in analog value from photoresistor
    readval = a.digital_read(ANALOG_PIN)

    # the default page to display will be our template with our template variables
    return render_template('index.html', status=status, status_time=status_time)


# unsecure API urls
@app.route('/turnon', methods=['GET'] )
def turn_on():
    # turn on LED on arduino
    a.digital_write(LED_PIN,1)
    return redirect( url_for('hello_world') )


@app.route('/turnoff', methods=['GET'] )
def turn_off():
    # turn off LED on arduino
    a.digital_write(LED_PIN,0)
    return redirect( url_for('hello_world') )



if __name__ == "__main__":

    # lets launch our webpage!
    # do 0.0.0.0 so that we can log into this webpage
    # using another computer on the same network later
    app.run()
