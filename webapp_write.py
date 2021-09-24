from flask import Flask, render_template,request
import os, platform, subprocess, netifaces, random, requests


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
color = os.environ.get('COLOR')
# color = os.environ['COLOR'] = 'red'

bgcolor1 = '#63c3e9'
bgcolor2 = '#a8d179'
bgcolor3 = '#51d8d8'
bgcolors = [bgcolor1,bgcolor2,bgcolor3]
bgcolor=random.choice(bgcolors)


@app.route('/',methods=['GET','POST'])
def index():

    ints = netifaces.interfaces()
    # ['lo', 'ens33', 'virbr0', 'virbr0-nic', 'docker0', 'veth07996f3']
    ip = netifaces.ifaddresses(ints[1])[2][0]['addr']
    netmask = netifaces.ifaddresses(ints[1])[2][0]['netmask']

    gateways = netifaces.gateways()
    gateway = gateways[2][0][0]

    # print("Gateway: " + gateways[2][0][0])
    # [('172.31.1.1', 'ens33', True)]

    hostname = subprocess.getstatusoutput("hostname")[1]
    # os.path.exists('/tmp/data'),

    if os.system('df -h | grep /data') == 0 :

        mount = True

        if  os.path.exists('/tmp/data') :
            
            try:
                with open('/tmp/data/message.txt', 'r') as file:
                    texts = file.read()

            except:
                texts = "message.txt not found in /tmp/data"

    else :
        mount = False
        texts = 'volume not mount'


    var1 = {
        'name': hostname,
        'ip': ip,
        'netmask': netmask,
        'gateway': gateway,
        'mount': mount,
        'os-base': platform.linux_distribution()[0],
        'os-version': platform.linux_distribution()[1],
    }
    
    if request.method == 'POST':
        
        inputText = request.form.get('MessageBox')
        print(inputText)
        if mount:
            with open('/tmp/data/message.txt','w') as file:
                file.write(inputText + '\n')            

    if mount:
        allow = 'enabled'
    else:
        allow = 'disabled'
    
    return render_template('webapp_write.html', page='Index', var=var1, text=texts, color=color,bgcolor=bgcolor,allow=allow)


if __name__ == '__main__':
    app.run(debug=True,port=30002,host='0.0.0.0')
