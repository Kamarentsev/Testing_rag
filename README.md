import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import getpass

# Инициализация приложения
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Логины, которые разрешены
VALID_LOGINS = ['admin', 'user1', 'user2']

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

# Основная страница после входа
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

# Описание интерфейса (layout) — начнем со страницы аутентификации
app.layout = html.Div(id="page-content", children=[login_page])

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
    # Проверка логина
    if username in VALID_LOGINS:
        try:
            # Имитация проверки системного пароля с помощью getpass (для локальной проверки)
            if password == getpass.getpass(f"Введите системный пароль для пользователя {username}: "):
                return main_page, ""
            else:
                return login_page, "Неверный системный пароль"
        except Exception as e:
            return login_page, str(e)
    else:
        return login_page, "Неверный логин"

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
