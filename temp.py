import jwt
import datetime

class SigUtils:
    @staticmethod
    def create_sig(app_id, app_key, sig_exp):
        issued_at = datetime.datetime.utcnow()
        expires_at = issued_at + datetime.timedelta(seconds=sig_exp)
        
        # create JWT payload
        payload = {
            "appId": app_id,       # 加入会话标识
            "iat": issued_at,      # 发行时间
            "exp": expires_at      # 过期时间
        }
        
        # 使用 HMAC256 算法和 app_key 签名
        token = jwt.encode(payload, app_key, algorithm="HS256")
        return token

app_id = "1304042845279227904"
app_key = "062a9e0c-a62f-45f9-a9f8-1136a2d45da3"
sig_exp = 1800

token = SigUtils.create_sig(app_id, app_key, sig_exp)
print(token)
