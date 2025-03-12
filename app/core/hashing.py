def get_password_hash(password: str) -> str:
    """
    Хеширует пароль с использованием алгоритма PBKDF2.

    Эта функция используется для хеширования паролей перед их сохранением в базе данных.
    Она генерирует уникальный хеш для каждого пароля, что повышает безопасность.

    Аргументы:
    - password: str — строка, представляющая пароль пользователя.

    Возвращает:
    - str — хешированный пароль, который будет сохранен в базе данных.

    Пример:
    >>> get_password_hash("my_secure_password")
    'pbkdf2_sha256$260000$9v...'
    """
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, совпадает ли переданный пароль с хешированным значением.

    Эта функция используется для проверки введенного пароля пользователя при логине.
    Она сравнивает введенный пароль с хешированным значением в базе данных.

    Аргументы:
    - plain_password: str — строка, представляющая пароль, введенный пользователем.
    - hashed_password: str — строка, представляющая ранее сохраненный хешированный пароль.

    Возвращает:
    - bool — True, если пароль совпадает с хешем, иначе False.

    Пример:
    >>> verify_password("my_secure_password", 'pbkdf2_sha256$260000$9v...')
    True
    """
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)
