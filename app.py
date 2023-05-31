from flask import Flask, request, render_template
import subprocess
import struct
import base64
import hashlib
import re

app = Flask(__name__)

def execute_dig_command(domain):
    command = ["dig", "DNSKEY", domain]
    output = subprocess.check_output(command, universal_newlines=True)

    dnskey_pattern = re.compile(r'^{}.\s+\d+\s+IN\s+DNSKEY\s+(.*)$'.format(domain), re.MULTILINE)
    dnskeys = dnskey_pattern.findall(output)

    dnskeys = [key for key in dnskeys if key.split(' ')[0] == '257']

    return dnskeys

def _calc_keyid(flags, protocol, algorithm, dnskey):
    st = struct.pack('!HBB', int(flags), int(protocol), int(algorithm))
    st += base64.b64decode(dnskey)

    cnt = 0
    for idx in range(len(st)):
        s = struct.unpack('B', st[idx:idx+1])[0]
        if (idx % 2) == 0:
            cnt += s << 8
        else:
            cnt += s

    return ((cnt & 0xFFFF) + (cnt >> 16)) & 0xFFFF

def _calc_ds(domain, flags, protocol, algorithm, dnskey):
    if domain.endswith('.') is False:
        domain += '.'

    signature = bytes()
    for i in domain.split('.'):
        signature += struct.pack('B', len(i)) + i.encode()

    signature += struct.pack('!HBB', int(flags), int(protocol), int(algorithm))
    signature += base64.b64decode(dnskey)

    return {
        'sha1':    hashlib.sha1(signature).hexdigest().upper(),
        'sha256':  hashlib.sha256(signature).hexdigest().upper(),
    }

def dnskey_to_ds(domain, dnskey):
    dnskeylist = dnskey.split(' ', 3)

    flags = dnskeylist[0]
    protocol = dnskeylist[1]
    algorithm = dnskeylist[2]
    key = dnskeylist[3].replace(' ', '')

    keyid = _calc_keyid(flags, protocol, algorithm, key)
    ds = _calc_ds(domain, flags, protocol, algorithm, key)

    ds_output = []
    ds_output.append("Key Tag: " + str(keyid))
    ds_output.append("Algorithm: " + str(algorithm))
    ds_output.append("Digest Type: 1 | Digest: " + ds['sha1'].lower())
    ds_output.append("Digest Type: 2 | Digest: " + ds['sha256'].lower())

    return ds_output

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    if request.method == 'POST':
        domain = request.form.get('domain', '').strip()
        if domain:
            dnskeys = execute_dig_command(domain)
            for dnskey in dnskeys:
                ds_output = dnskey_to_ds(domain, dnskey)
                result.extend(ds_output)
                result.append('') # To insert a blank line between outputs of different dnskeys
        else:
            result.append("Invalid domain name. Please try again.")

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
