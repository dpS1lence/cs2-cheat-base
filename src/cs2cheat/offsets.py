from requests import get


class Client:
    def __init__(self):
        try:
            self.offsets = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/generated/offsets.json').json()
            self.client_dll = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/generated/client.dll.json').json()
        except:
            print('Unable to get offsets.')
            exit()

    def offset(self, a):
        try:
            return self.offsets['client_dll']['data'][a]['value']
        except:
            print(f'Offset {a} not found.')
            exit()

    def get(self, a, b):
        try:
            return self.client_dll[a]['data'][b]['value']
        except:
            print(f'Unable to get {a}, {b}.')
            exit()