import tornado.ioloop
import tornado.web
import base64
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Key and IV for AES encryption
AES_KEY = get_random_bytes(16)
AES_IV = get_random_bytes(16)

class HSM:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        plaintext = unpad(cipher.decrypt(base64.b64decode(ciphertext)), AES.block_size)
        return plaintext.decode('utf-8')

    def generate_random_key(self):
        return ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(16))

class EncryptHandler(tornado.web.RequestHandler):
    def initialize(self, hsm):
        self.hsm = hsm

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        plaintext = data.get("plaintext")
        if plaintext:
            encrypted = self.hsm.encrypt(plaintext)
            self.write({"ciphertext": encrypted})
        else:
            self.set_status(400)
            self.write({"error": "Missing plaintext"})


class DecryptHandler(tornado.web.RequestHandler):
    def initialize(self, hsm):
        self.hsm = hsm

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        ciphertext = data.get("ciphertext")
        if ciphertext:
            try:
                decrypted = self.hsm.decrypt(ciphertext)
                self.write({"plaintext": decrypted})
            except Exception as e:
                self.set_status(400)
                self.write({"error": "Decryption failed", "details": str(e)})
        else:
            self.set_status(400)
            self.write({"error": "Missing ciphertext"})


class KeyGenerationHandler(tornado.web.RequestHandler):
    def initialize(self, hsm):
        self.hsm = hsm

    def get(self):
        random_key = self.hsm.generate_random_key()
        self.write({"random_key": random_key})


def make_app():
    hsm = HSM(AES_KEY, AES_IV)
    return tornado.web.Application([
        (r"/encrypt", EncryptHandler, dict(hsm=hsm)),
        (r"/decrypt", DecryptHandler, dict(hsm=hsm)),
        (r"/generate_key", KeyGenerationHandler, dict(hsm=hsm)),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("HSM Simulation running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
