from flask import Flask, render_template,request, redirect, url_for, flash
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
ANALOG_PIN_23 = 23
ANALOG_PIN_19 = 19

# initialize the digital pin as output
a.set_pin_mode(LED_PIN,'O')
# a.set_pin_mode(ANALOG_PIN_19, 'I')
# a.set_pin_mode(ANALOG_PIN_23, 'I')

print('Arduino initialized')


# we are able to make 2 different requests on our webpage
# GET = we just type in the url
# POST = some sort of form submission like a button
@app.route('/', methods = ['POST','GET'])
def hello_page():
    # variables for template page (templates/index.html)
    status = ''
    status_time = ''
    # if we make a post request on the webpage aka press button then do stuff
    if request.method == 'POST':
        # выбор режима
        if request.form['submit'] == 'Ручное управление':
            return redirect(url_for('manualon'))
        else:
            pass
    return render_template('index.html')

@app.route('/manualon', methods = ['POST','GET'] )
def manual_on():
    if request.method == 'POST':
        if request.form['submit'] == '1 этаж':
            # проверяем текущее состояние лифта
            # current_floor из лог файла
            current_floor =0;
            if current_floor == 1:
                flash("Лифт находится на 1 этаже");
            else:
                sensor = a.digital_read(23)
                while (sensor!=0):
                    a.digital_write(LED_PIN, 1) #a.PWM_write(1000)
                    sensor = a.digital_read(23)
                    print("23 = "+sensor)
                    time.sleep(1)
                a.digital_write(LED_PIN, 0)
            #     остановка и запись в журнал что лифт на определенном этаже
        elif request.form['submit'] == '2 этаж':
            # проверяем текущее состояние лифта
            # current_floor из лог файла
            current_floor = 1;
            if current_floor == 2:
                flash("Лифт находится на 2 этаже");
            elif current_floor != 2:
                sensor = a.digital_read(ANALOG_PIN_23)
                while (sensor != 0):
                    a.digital_write(LED_PIN, 1)  # a.PWM_write(1000)
                    sensor = a.digital_read(ANALOG_PIN_23)
                    print("19 = "+ sensor)
                    time.sleep(3)
                a.digital_write(LED_PIN, 0)
            #     остановка и запись в журнал что лифт на определенном этаже
        else:
            pass
    return render_template('index.html')

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
