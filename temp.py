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

# ==== 舊local ====
# app_id = "1304042845279227904"
# app_key = "062a9e0c-a62f-45f9-a9f8-1136a2d45da3"

# ==== 新Saas ====
# app_id = "1312090463162994688"
# app_key = "8102e5a4-051d-423d-a16f-8b8b14a7989e"

# ==== Saas付費 ====
app_id = "1317195753466236928"
app_key = "e9cdc886-5801-488f-949a-39baf65a2d2a"

# ==== 新local default ====
# app_id = "1312090463343349760"
# app_key = "318807eb-1a17-42a8-ab0c-a0d5c8a2a379"

# ==== 新local duix_df26z ====
# app_id = "1313214945982287872"
# app_key = "cfea5534-721b-4cb8-b804-a9e0e3d8cece"
sig_exp = 7200

token = SigUtils.create_sig(app_id, app_key, sig_exp)
print(token)
