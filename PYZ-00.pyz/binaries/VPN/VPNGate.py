# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\binaries\VPN\VPNGate.py
if __name__ == 'binaries.VPN.VPNGate':
    import requests, os, sys, tempfile, subprocess, base64, time, json, re, pycountry
    from urllib.request import urlopen
    from __main__ import dirPath
    debug = False
    if debug:
        debuglevel = '3'
    else:
        debuglevel = '1'

    def GetVPNGateServer(country):
        global path
        if len(country) == 2:
            i = 6
        else:
            if len(country) > 2:
                i = 5
            else:
                print('Country is too short!')
                exit(1)
        try:
            vpn_data = requests.get('http://www.vpngate.net/api/iphone/').text.replace('\r', '')
            servers = [line.split(',') for line in vpn_data.split('\n')]
            labels = servers[1]
            labels[0] = labels[0][1:]
            servers = [s for s in servers[2:] if len(s) > 1]
        except:
            print('Cannot get VPN servers data')
            exit(1)

        desired = [s for s in servers if country.lower() in s[i].lower()]
        found = len(desired)
        print('Found ' + str(found) + ' servers for country ' + country)
        if found == 0:
            exit(1)
        supported = [s for s in desired if len(s[(-1)]) > 0]
        print(str(len(supported)) + ' of these servers support OpenVPN')
        winner = sorted(supported, key=(lambda s: float(s[2].replace(',', '.'))), reverse=True)[0]
        print('\n== Best server ==')
        pairs = list(zip(labels, winner))[:-1]
        for l, d in pairs[:4]:
            print(l + ': ' + d)

        print(pairs[4][0] + ': ' + str(float(pairs[4][1]) / 1000000) + ' MBps')
        print('Country: ' + pairs[5][1] + '\n')
        _, path = tempfile.mkstemp()
        f = open(path, 'wb')
        f.write(base64.b64decode(winner[(-1)]))
        f.close()


    def GetLocationInfo():
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        print('IP Info:')
        print('IP: {4} \nRegion: {1} \nCountry: {2} \nCity: {3} \nCompany: {0}\n'.format(data['org'], data['region'], data['country'], data['city'], data['ip']))
        return (
         data['ip'], data['country'])


    def ConnectToVPN(OVPNFile):
        global dirPath
        x = subprocess.Popen([dirPath + '\\binaries\\VPN\\openvpn\\openvpn.exe', '--config', OVPNFile, '--verb', debuglevel, '--auth-nocache'], stdout=(subprocess.PIPE), universal_newlines=True)
        for line in x.stdout:
            if 'Errors' in line.strip():
                print('Error! Killing process and trying to connect again...')
                os.system('taskkill /im openvpn.exe /f')
                ConnectToVPN(OVPNFile)
            else:
                if 'Initialization Sequence Completed' in line.strip():
                    sys.stdout.write(line[25:] + '\n')
                    return
                if not (not debug and ('WARNING' in line.strip() or 'version' in line.strip() or 'link' in line.strip() or 'open_tun' in line.strip() or 'ifconfig' in line.strip())):
                    sys.stdout.write(line[25:])


    def VPNGateConnect(country_code):
        CurrentIP, CurrentCountry = GetLocationInfo()
        GetVPNGateServer(country_code)
        ConnectToVPN(path)
        NewCurrentIP, NewCurrentCountry = GetLocationInfo()
        if NewCurrentIP != CurrentIP:
            if NewCurrentCountry != CurrentCountry:
                print('Successfully connected!')
        else:
            print("The current location hasn't changed! Reconnecting...")
            attempt = 0
            while NewCurrentIP == CurrentIP and NewCurrentCountry == CurrentCountry:
                attempt += 1
                if attempt == 6:
                    print('Too many attemps! Quitting...')
                    sys.exit(0)
                print('Attempt ' + str(attempt) + '...')
                ConnectToVPN(path)

            sys.exit(0)