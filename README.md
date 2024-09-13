import streamlit as st
import streamlit_authenticator as stauth

# Определяем пользователей и их пароли
names = ['Иван Иванов', 'Петр Петров']
usernames = ['ivan', 'petr']
passwords = ['password1', 'password2']

# Создание хэшей паролей (вызывается один раз)
hashed_passwords = stauth.Hasher(passwords).generate()

# Настройка аутентификации
authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30
)

# Создаем форму для аутентификации
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.success(f'Добро пожаловать {name}!')
    # Основная страница приложения
    st.write('Основное содержимое вашего приложения...')
    
elif authentication_status == False:
    st.error('Неверное имя пользователя или пароль')
    
elif authentication_status == None:
    st.warning('Пожалуйста, введите ваши учетные данные')

# Добавляем возможность выхода из аккаунта
authenticator.logout('Logout', 'sidebar')
