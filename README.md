import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import os
from ldap3 import Server, Connection, ALL, NTLM

# Инициализация приложения
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Имитируем работу с секретами из переменных окружения
LDAP_SERVER = os.getenv('LDAP_SERVER', 'ldap://your-default-server')  # Замените на ваш сервер LDAP
allowUsers = ['VTB70217696@REGION.VTB.RU', 'VTB70204926@REGION.VTB.RU', 'VTB7027110@REGION.VTB.RU', 'VTB70250595@REGION.VTB.RU', 'VTB70250965@REGION.VTB.RU']

# Интерфейс страницы аутентификации
login_page = dbc.Container([
    dbc.Row(
        dbc.Col(html.H2("Вход в систему ВТБ", style={"color": "#003399"}), width=12, className="text-center")
    ),
    dbc.Row(
        dbc.Col([
            dbc.Input(id="username", placeholder="Введите логин в формате 'логин@REGION.VTB.RU'", type="text", className="mb-3"),
            dbc.Input(id="password", placeholder="Введите пароль", type="password", className="mb-3"),
            dbc.Button("Войти", id="login-button", color="primary", className="w-100"),
            html.Div(id="login-output", className="mt-3", style={"color": "red"})
        ], width=6, className="offset-md-3")
    )
], fluid=True, style={"backgroundColor": "#6699FF", "padding": "100px"})

# Главная страница после успешной аутентификации
main_page = html.Div([
    dbc.NavbarSimple(
        brand="ВТБ Панель",
        brand_href="#",
        color="#003399",
        dark=True
    ),
    dbc.Container([
        html.H1("Добро пожаловать в ВТБ Панель", style={"color": "#003399"}),
        dcc.Graph(figure={})  # Здесь будет график
    ], fluid=True, style={"backgroundColor": "#6699FF", "padding": "20px"})
])

# Описание интерфейса
app.layout = html.Div(id="page-content", children=[login_page])

# Функция для аутентификации через LDAP
def authenticate(username, password):
    server = Server(LDAP_SERVER, get_info=ALL)
    try:
        print(f"Попытка подключения к серверу: {LDAP_SERVER}")
        print(f"Проверяем логин: {username}")
        conn = Connection(server, user=username, password=password, authentication=NTLM)
        if conn.bind():
            print("Аутентификация прошла успешно.")
            return True
        else:
            print("Ошибка аутентификации: неверный пароль или логин.")
            return False
    except Exception as e:
        print(f"Ошибка аутентификации: {str(e)}")
        return False

# Логика аутентификации
@app.callback(
    Output("page-content", "children"),
    Output("login-output", "children"),
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def authenticate_user(n_clicks, username, password):
    # Проверяем логин на наличие в списке разрешённых
    print(f"Полученные данные: логин - {username}, пароль - {'*' * len(password)}")

    # Проверяем, что логин имеет правильный формат и есть в списке разрешенных
    if username not in allowUsers:
        return login_page, "Логин не найден в списке разрешённых пользователей"

    # Если логин разрешён, проверяем пароль через системную аутентификацию
    if authenticate(username, password):
        return main_page, ""
    else:
        return login_page, "Неверный пароль"

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
