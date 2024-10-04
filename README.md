import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from ldap3 import Server, Connection, ALL, NTLM

# Инициализация приложения
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Список разрешённых логинов
allowUsers = ['VTB70217696', 'VTB70204926', 'VTB7027110', 'VTB70250595', 'VTB70250965']

# Интерфейс для страницы аутентификации
login_page = dbc.Container([
    dbc.Row(
        dbc.Col(html.H2("Вход в систему ВТБ", style={"color": "#003399"}), width=12, className="text-center")
    ),
    dbc.Row(
        dbc.Col([
            dbc.Input(id="username", placeholder="Введите логин", type="text", className="mb-3"),
            dbc.Input(id="password", placeholder="Введите пароль от компьютера", type="password", className="mb-3"),
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

# Функция аутентификации через LDAP
def authenticate(username, password):
    server = Server('ldap://your-ldap-server', get_info=ALL)  # Замените на ваш LDAP сервер
    try:
        conn = Connection(server, user=f'REGION\\{username}', password=password, authentication=NTLM)
        if conn.bind():
            return True
        else:
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
    # Проверяем логин пользователя
    if username in allowUsers:
        # Если логин разрешен, проверяем пароль через LDAP
        if authenticate(username, password):
            return main_page, ""
        else:
            return login_page, "Неверный пароль"
    else:
        return login_page, "Неверный логин"

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)

