import json
import base64
import os
from datetime import datetime

# ВСТАВЬТЕ СЮДА ВЕСЬ ТЕКСТ ИЗ ВАШЕГО Keys.txt (от #profile-title до последней строчки)
BASE_CONFIG = """#profile-title: HotVPN🔥
#support-url: https://t.me/Wd_Life
#profile-update-interval: 5
#announce: ТГК: https://t.me/Wd_Life от 09.04.2026 21:09
################################

ВАШИ ВСЕ VLESS КЛЮЧИ... (СКОПИРУЙТЕ ИХ СЮДА ИЗ ФАЙЛА Keys.txt)
"""

# --- ФУНКЦИЯ ДЛЯ ДОБАВЛЕНИЯ ИНФОРМАЦИИ О ПОДПИСКЕ ---
def add_metadata_to_config(base_config, expire_timestamp, total_bytes):
    """
    Добавляет в начало конфига заголовки для Happ.
    """
    # Формируем строку с информацией о трафике и сроке
    # upload=0; download=0 - мы не можем считать трафик, поэтому просто показываем лимит
    user_info = f"upload=0; download=0; total={total_bytes}; expire={expire_timestamp}"
    
    # Формируем финальный конфиг. Порядок важен: сначала метаданные, потом ключи.
    final_config = (
        f"#profile-title: HotVPN🔥\n"
        f"#profile-update-interval: 5\n"
        f"#support-url: https://t.me/Wd_Life\n"
        f"#subscription-userinfo: {user_info}\n"
        f"#sub-expire: true\n" # Включаем напоминание об истечении подписки в Happ
        f"\n{base_config}"
    )
    # Кодируем в base64, как и раньше
    return base64.b64encode(final_config.encode()).decode()
# ----------------------------------------------------

def main():
    # Создаем папку, если её нет
    os.makedirs('subs', exist_ok=True)
    
    # Читаем список пользователей
    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    # Обрабатываем каждого пользователя
    for user_id, user_info in users.items():
        if user_info.get('status') != 'active':
            # Если пользователь не активен, удаляем его файл, если он есть
            if os.path.exists(f'subs/{user_id}.txt'):
                os.remove(f'subs/{user_id}.txt')
                print(f"❌ Пользователь {user_id} заблокирован, файл удален.")
            continue
        
        # --- ПОЛУЧАЕМ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ ---
        # 1. Срок подписки (переводим дату из users.json в timestamp)
        expire_date_str = user_info.get('expire_date')
        if expire_date_str:
            expire_timestamp = int(datetime.strptime(expire_date_str, "%Y-%m-%d").timestamp())
        else:
            expire_timestamp = 0 # Если даты нет, значит подписка вечная или не указана

        # 2. Лимит трафика (в байтах)
        # Добавьте поле 'traffic_limit_gb' в ваш файл users.json!
        traffic_limit_gb = user_info.get('traffic_limit_gb', 50) # По умолчанию 50GB
        total_bytes = traffic_limit_gb * 1073741824 # Переводим гигабайты в байты
        # ---------------------------------
        
        # Генерируем финальную подписку с метаданными
        final_subscription = add_metadata_to_config(BASE_CONFIG, expire_timestamp, total_bytes)
        
        # Записываем результат в файл пользователя
        with open(f'subs/{user_id}.txt', 'w', encoding='utf-8') as f:
            f.write(final_subscription)
            
        print(f"✅ Подписка для {user_id} обновлена. Срок: {expire_date_str}, Лимит: {traffic_limit_gb} GB.")

if __name__ == "__main__":
    main()
