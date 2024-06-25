import datetime
import json
import platform, psutil
import socket, subprocess

def ping(destination):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    result = subprocess.run(
        ['ping', param, '4', destination],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # report = ' | '.join([
    #     ' '.join(result.stdout.split()[36:45]), 
    #     ' '.join(result.stdout.split()[53:])
    # ])

    return {
        'sent': float(result.stdout.split()[39][:-1]),
        'received': float(result.stdout.split()[42][:-1]),
        'lost': float(result.stdout.split()[45]),
        'loss_percentage': float(result.stdout.split()[46][1:-1]),
        'minimum_ms': float(result.stdout.split()[56][:-3]),
        'maximum_ms': float(result.stdout.split()[59][:-3]),
        'average_ms': float(result.stdout.split()[62][:-2])
    }

if __name__ == '__main__':
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    destinations = ['google.com', 'myits-app.its.ac.id']

    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except:
            data = []
            
    data.append({'timestamp': timestamp})
    for destination in destinations:
        ping_data = ping(destination)
        data[-1][destination] = ping_data

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=3)