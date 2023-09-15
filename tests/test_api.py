from unittest import TestCase

import requests


class ApiTest(TestCase):

    def setUp(self) -> None:
        self.url = "http://127.0.0.1:5000/consultas/"
        self.body = { ##Mudar o body de acordo com os dados
            "tribunal":"tjal",
            "numero_processo":"0034520-06.2010.8.02.0001"
        }

    def test_api(self): ## Test if result_code is OK
        response = requests.post(self.url,json=self.body)
        self.assertEquals(response.status_code, 200)
        assert response.content is not None


if __name__ == "__main__":
    test = ApiTest()
    test.test_api()