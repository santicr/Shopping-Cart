import sys, requests
from sys import stdin
import csv
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller')
from controller_user import register_user

def reg_process():
    passw = "Prueba1234@"
    user = stdin.readline().strip()
    while user != "":
        params = {
            'name': user,
            'passw': passw
        }
        requests.post('http://127.0.0.1:8000/api/users/user', json = params)
        user = stdin.readline().strip()

def put_csv():
    with open('data.csv', 'w', encoding='UTF8', newline='') as f:
        user = stdin.readline().strip()
        writer = csv.DictWriter(f, fieldnames=['name', 'passw'])
        while user != '':
            passw = "Prueba1234@"
            params = {
                'name': user,
                'passw': passw
            }
            writer.writerow(params)
            user = stdin.readline().strip()

def main():
    put_csv()

main()