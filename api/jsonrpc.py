import ssl
import json
import http.client
import tempfile

class JsonRpcClient:
    def __init__(self, endpoint, certificate, key):
        self.endpoint = endpoint

        # Создаем временные файлы для сертификата и ключа
        self.cert_file = tempfile.NamedTemporaryFile(delete=False)
        self.key_file = tempfile.NamedTemporaryFile(delete=False)

        self.cert_file.write(certificate.encode('utf-8'))
        self.cert_file.flush()
        self.key_file.write(key.encode('utf-8'))
        self.key_file.flush()

        # Создаем SSL-контекст для клиента
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_cert_chain(certfile=self.cert_file.name, keyfile=self.key_file.name)


    def call_method(self, method, params=None):
        params = params or {}
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1,
        }
        body = json.dumps(payload)
        try:
            conn = http.client.HTTPSConnection(self.endpoint.split("/")[2], context=self.context)
            conn.request("POST", self.endpoint, body, headers={"Content-Type": "application/json"})
            response = conn.getresponse()
            data = response.read()
            return json.loads(data)
        except Exception as e:
            return {"error": str(e)}

    def __del__(self):
        # Удаляем временные файлы при завершении работы
        self.cert_file.close()
        self.key_file.close()
