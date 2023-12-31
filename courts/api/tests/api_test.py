from django.test import TestCase
import requests
from django.conf import settings  # Import Django settings module
from dotenv import load_dotenv
import os
import sys

load_dotenv()


class ApiTest(TestCase):
    databases = {'test'}
    apiUrl = os.getenv('API_URL')
    processos = [
        {'processo': '0010484-60.2011.8.02.0001','segundaInstancia': False, 'tribunal': 'tjal' },
        {'processo': '0710802-55.2018.8.02.0001','segundaInstancia': True, 'tribunal': 'tjal' },
        {'processo': '0070337-91.2008.8.06.0001','segundaInstancia': False, 'tribunal': 'tjce' },
    ]


    def testApi(self):
        for processo in self.processos:
            respose = requests.post(self.apiUrl,
                                data={'tribunal': processo['tribunal'],
                                      'processo': processo['processo']}
                                )
            data = respose.json()[0].get('data')
            self.assertEqual(respose.status_code, 200)
            self.assertIsNotNone(data['area'])
            self.assertIsNotNone(data['lista_movimentacoes'])
            print(data)
            if(processo['segundaInstancia']):
                data = respose.json()[1].get('data')
                self.assertEqual(data['grau'], '2º grau')


    def testApiWrongCourt(self):
        for processo in self.processos:
            respose = requests.post(self.apiUrl,
                                data={'tribunal': 'TJRR',  ##Court not supported
                                      'processo': processo['processo']}
                                )
            self.assertEqual(respose.status_code, 400)
