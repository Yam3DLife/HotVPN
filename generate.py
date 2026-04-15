import json
import base64
import os
from datetime import datetime

# 🔑 ВАША ОСНОВНАЯ ССЫЛКА (из вашего Keys.txt)
# Берём ВЕСЬ контент вашего Keys.txt как есть (с заголовками и всеми ключами)
BASE_CONFIG = """#profile-title: HotVPN🔥
#support-url: https://t.me/Wd_Life
#profile-update-interval: 5
#announce: ТГК: https://t.me/Wd_Life от 09.04.2026 21:09
################################

vless://81de8a98-9c3c-07d0-bdf4-91fba80fe7e9@cluster11.anti-vpn.ru:52006?security=tls&encryption=none&alpn=http/1.1&headerType=none&fp=chrome&allowinsecure=1&type=tcp&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA+%E2%9A%A1%F0%9F%9F%A9+%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F+%5BVPN%5D+%232
vless://e282bc50-e4e9-4a26-9837-ea6372bab3fc@extbalancer.msemse.ru:443?security=reality&encryption=none&pbk=-nZqMxt7meVxfnQeK46MAYh5scb0M6La82axD8KHJXk&headerType=none&fp=random&allowinsecure=0&type=tcp&flow=xtls-rprx-vision&sni=i.oneme.ru&sid=d4a9f26c#%F0%9F%87%B7%F0%9F%87%BA%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F+%28LTE+%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80+-+%D0%90%D0%B2%D1%82%D0%BE+%F0%9F%94%A5%F0%9F%9A%80%29+%F0%9F%A4%96
... (и все остальные ключи из вашего Keys.txt)
"""

def generate_subscription(user_id, user_info):
    if user_info.get('status') != 'active':
        return None
    
    expire_date = user_info.get('expire_date')
    if expire_date:
        expire_dt = datetime.fromisoformat(expire_date)
        if datetime.now() > expire_dt:
            return None
    
    # Берём вашу основную конфигурацию
    config = BASE_CONFIG
    
    # Кодируем в base64 (как требует Happ)
    encoded = base64.b64encode(config.encode()).decode()
    return encoded

def main():
    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    os.makedirs('subs', exist_ok=True)
    
    for user_id, user_info in users.items():
        subscription = generate_subscription(user_id, user_info)
        
        if subscription:
            with open(f'subs/{user_id}.txt', 'w', encoding='utf-8') as f:
                f.write(subscription)
            print(f"✅ Сгенерировано: {user_id}")
        else:
            if os.path.exists(f'subs/{user_id}.txt'):
                os.remove(f'subs/{user_id}.txt')
                print(f"❌ Удалён (неактивен): {user_id}")

if __name__ == "__main__":
    main()
