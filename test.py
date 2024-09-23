import json
import base64
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

private_key = b"-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAwhvqCC+37A+UXgcvDl+7nbVjDI3QErdZBkI1VypVBMkKKWHM\nNLMdHk0bIKL+1aDYTRRsCKBy9ZmSSX1pwQlO/3+gRs/MWG27gdRNtf57uLk1+lQI\n6hBDozuyBR0YayQDIx6VsmpBn3Y8LS13p4pTBvirlsdX+jXrbOEaQphn0OdQo0WD\noOwwsPCNCKoIMbUOtUCowvjesFXlWkwG1zeMzlD1aDDS478PDZdckPjT96ICzqe4\nO1Ok6fRGnor2UTmuPy0f1tI0F7Ol5DHAD6pZbkhB70aTBuWDGLDR0iLenzyQecmD\n4aU19r1XC9AHsVbQzxHrP8FveZGlV/nJOBJwFwIDAQABAoIBAFCVFBA39yvJv/dV\nFiTqe1HahnckvFe4w/2EKO65xTfKWiyZzBOotBLrQbLH1/FJ5+H/82WVboQlMATQ\nSsH3olMRYbFj/NpNG8WnJGfEcQpb4Vu93UGGZP3z/1B+Jq/78E15Gf5KfFm91PeQ\nY5crJpLDU0CyGwTls4ms3aD98kNXuxhCGVbje5lCARizNKfm/+2qsnTYfKnAzN+n\nnm0WCjcHmvGYO8kGHWbFWMWvIlkoZ5YubSX2raNeg+YdMJUHz2ej1ocfW0A8/tmL\nwtFoBSuBe1Z2ykhX4t6mRHp0airhyc+MO0bIlW61vU/cPGPos16PoS7/V08S7ZED\nX64rkyECgYEA4iqeJZqny/PjOcYRuVOHBU9nEbsr2VJIf34/I9hta/mRq8hPxOdD\n/7ES/ZTZynTMnOdKht19Fi73Sf28NYE83y5WjGJV/JNj5uq2mLR7t2R0ZV8uK8tU\n4RR6b2bHBbhVLXZ9gqWtu9bWtsxWOkG1bs0iONgD3k5oZCXp+IWuklECgYEA27bA\n7UW+iBeB/2z4x1p/0wY+whBOtIUiZy6YCAOv/HtqppsUJM+W9GeaiMpPHlwDUWxr\n4xr6GbJSHrspkMtkX5bL9e7+9zBguqG5SiQVIzuues9Jio3ZHG1N2aNrr87+wMiB\nxX6Cyi0x1asmsmIBO7MdP/tSNB2ebr8qM6/6mecCgYBA82ZJfFm1+8uEuvo6E9/R\nyZTbBbq5BaVmX9Y4MB50hM6t26/050mi87J1err1Jofgg5fmlVMn/MLtz92uK/hU\nS9V1KYRyLc3h8gQQZLym1UWMG0KCNzmgDiZ/Oa/sV5y2mrG+xF/ZcwBkrNgSkO5O\n7MBoPLkXrcLTCARiZ9nTkQKBgQCsaBGnnkzOObQWnIny1L7s9j+UxHseCEJguR0v\nXMVh1+5uYc5CvGp1yj5nDGldJ1KrN+rIwMh0FYt+9dq99fwDTi8qAqoridi9Wl4t\nIXc8uH5HfBT3FivBtLucBjJgOIuK90ttj8JNp30tbynkXCcfk4NmS23L21oRCQyy\nlmqNDQKBgQDRvzEB26isJBr7/fwS0QbuIlgzEZ9T3ZkrGTFQNfUJZWcUllYI0ptv\ny7ShHOqyvjsC3LPrKGyEjeufaM5J8EFrqwtx6UB/tkGJ2bmd1YwOWFHvfHgHCZLP\n34ZNURCvxRV9ZojS1zmDRBJrSo7+/K0t28hXbiaTOjJA18XAyyWmGg==\n-----END RSA PRIVATE KEY-----\n"
public_key = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwhvqCC+37A+UXgcvDl+7\nnbVjDI3QErdZBkI1VypVBMkKKWHMNLMdHk0bIKL+1aDYTRRsCKBy9ZmSSX1pwQlO\n/3+gRs/MWG27gdRNtf57uLk1+lQI6hBDozuyBR0YayQDIx6VsmpBn3Y8LS13p4pT\nBvirlsdX+jXrbOEaQphn0OdQo0WDoOwwsPCNCKoIMbUOtUCowvjesFXlWkwG1zeM\nzlD1aDDS478PDZdckPjT96ICzqe4O1Ok6fRGnor2UTmuPy0f1tI0F7Ol5DHAD6pZ\nbkhB70aTBuWDGLDR0iLenzyQecmD4aU19r1XC9AHsVbQzxHrP8FveZGlV/nJOBJw\nFwIDAQAB\n-----END PUBLIC KEY-----\n"

header = {
  "alg": "RS256",
  "typ": "JWT"
}

payload = {
  "sub": "1234567890",
  "name": "John Doe",
  "admin": True,
  "iat": 1516239022
}

class Jwt:
    def encode(self, header, payload):
        h = self._encode(header)
        p = self._encode(payload)
        sign_payload = f"{h}.{p}"
        s = self._sign(sign_payload)
        return f"{h}.{p}.{s}"
        

    def _sign(self, contents):
        """
        Signing Details:
        https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#signing 
        """
        pk = serialization.load_pem_private_key(private_key, password=None)
        sig = pk.sign(
            bytes(contents, "utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        encoded = base64.urlsafe_b64encode(sig).replace(b"=", b"").decode("utf-8")
        return encoded

    def _encode(self, contents) -> str:
        """
        Base 64 encoding:
        https://en.wikipedia.org/wiki/Base64
        """
        h = json.dumps(contents, separators=(',', ':'))
        b = h.encode("utf-8")
        e = base64.urlsafe_b64encode(b).replace(b"=", b"").decode("utf-8")
        return e


encoded = jwt.encode(payload, private_key, algorithm="RS256")
ha, hp, hs = encoded.split(".")

h, p, s = Jwt().encode(header, payload).split(".")

print(h == ha, h)
print(p == hp, p)
print(s == hs, s)
print(hs)
print(s)

# header - eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9
# payload - eyJpc3MiOiJqb2UiLCJleHAiOjEzMDA4MTkzODAsImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ
# signed rsa256 - voCLHGV6fiw5ECP-7lhMEmYqINcGwsm8iadzLPZC_Vhyy8t3jXiDUv0RkOfhBk6k_gqUciBZqyaX51AKIwy2cxjMvV3xL_wAmyPXOz54iutmrleT699TAeOONBbrrWpEh4dYsTS3yzpdMdLC8wfqHQ2nHy9fjL5p6ERHPle89umxjo1j4JsQYZffhtQ_DDFIi4TaPamy5phamIY5sMY-4eQs-xURtWeSjnIiHoYqKA6wLDKfr48gjE3e_OjRqQ9RyZAf2NFfXAtEAEMAgBW2aH_zMBWNKbo8CSA_HpnMO7_yP7CWx3S4Sn7mgdeMGGXcLYjpsL0M_3WXvH9It5RjrA

# header eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9
# payload eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0
# sign c2S8PX0vOe8yn51usQBlO-6f5SGaIdbilq94Zpyezv_BCfV4oVo_IxWEoNoz9gsdmd17MtwG3FqBto-eubn0lJy9Pf4u_eXCginnpoaUkIjCKcxBvIpRt7_Zin1f2BDGPxa_ow4DuBamlpsILV8hyf6uJStd0L-0gcrfkwbWca8ohFSKA-Pckufrw_-Nf38jJgflUPmsi3e7U8JC28vuwiF6bzPiR4l3gS3h7qAth8UVPBhA3xKOGI4kYdzvmh5M1NzeG916iB82-xH6PyDYDAwmW836k-1Y8GycN7Ep4-T-BPRRZI7aSfZRIe7ENVBQ974MoT1u2963afoBG_LT-w

def verify(signature, message):
    signature1 = base64.urlsafe_b64decode(signature + "=" * (4 - len(signature) % 4))
    key = serialization.load_pem_public_key(public_key)
    try:
      key.verify(
          signature1, 
          bytes(message, "utf-8"), 
          padding.PKCS1v15(),
          hashes.SHA256())
    except InvalidSignature as e:
        return (None, True)
    h, p = message.split(".")
    p1 = base64.urlsafe_b64decode(p + "=" * (4 - len(signature) % 4))
    return (p1, False)

decoded = jwt.decode(encoded, public_key, algorithms=["RS256"])
print("-----------------------")
print(decoded)
actual = verify(s, f"{h}.{p}")
print(actual)