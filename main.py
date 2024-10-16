import flet as ft
import sqlite3


def maun (page: ft.Page):
    page.title = "IT PROGER"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 300
    page.window_height = 400
    page.window_resizable = False

    def register(e):
        db = sqlite3.connect('it.proger')

        cur  = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    login TEXT,
                    password TEXT
        )""")
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (user_login.value, user_password.value))       
        db.commit()
        db.close()

        user_login.value = ""
        user_password.value = ""
        btn_reg.text = 'Добавлено'
        page.update()



    def validate(e):
        if all ([user_login.value, user_password.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True

        page.update()
     
    def auth_user(e):
        db = sqlite3.connect('it.proger')

        cur  = db.cursor()
        cur.execute("SELECT * FROM users WHERE login = ? AND password = ?", (user_login.value, user_password.value))
        if cur.fetchone() != None:
            user_login.value = ""
            user_password.value = ""
            btn_auth.text = 'Авторизованно'

            if len (page.navigation_bar.destinations) == 2:
                page.navigation_bar.destinations.append(ft.NavigationBarDestination(
                    icon=ft.icons.BOOK,
                    label="Кабинет",
                    selected_icon=ft.icons.BOOK_OUTLINED
                ))

            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Пользователь не найден"))
            page.snack_bar.open = True
            page.update()

        db.commit()
        db.close()

        
    user_login = ft.TextField(label="Логин", width=200, on_change=validate)
    user_password = ft.TextField(label="Пароль", password=True, width=200, on_change=validate)
    btn_reg = ft.OutlinedButton (text="Регистрация", width=200,on_click=register, disabled=True)
    btn_auth = ft.OutlinedButton (text="Авторизовать", width=200,on_click=auth_user, disabled=True)
    

    #user cabinet

    user_list = ft.ListView(spacing=10, padding=20)

    

    #user cabinet end

    panel_register =ft.Row(
             [
                 ft.Column(
                     [
                         ft.Text("Добавить"),
                         user_login,
                         user_password,
                         btn_reg
                     ]
                 )    
             ],
             alignment=ft.MainAxisAlignment.CENTER
         )
    
    panel_auth = ft.Row(    
             [
                 ft.Column(
                     [
                         ft.Text("Авторизация"),
                         user_login,
                         user_password,
                         btn_auth
                     ]
                 )    
             ],
             alignment=ft.MainAxisAlignment.CENTER
         )
    
    panel_cabinet = ft.Row(    
             [
                 ft.Column(
                     [
                         ft.Text("Личный кабинет"),
                         user_list
                     ]
                 )    
             ],
             alignment=ft.MainAxisAlignment.CENTER
         )
    def validate(e):
        index = page.navigation_bar.selected_index
        page.clean ()

        if index == 0: page.add(panel_register,)
        elif index == 1: page.add(panel_auth,)
        elif index == 2:
            user_list.controls.clear()

            db = sqlite3.connect('it.proger')

            cur  = db.cursor()
            cur.execute("SELECT * FROM users" )
            res = cur.fetchall()

            if res :

                for user in res:
                    print(user)
                    user_list.controls.append(
                    ft.Row(
                        [
                            ft.Text('User {user[1]}'.format(user=user)),
                            ft.Icon(ft.icons.VERIFIED_USER_ROUNDED)
                        ]
                    )
                )
            db.commit()
            db.close()
            page.add(panel_cabinet)
        



    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.VERIFIED_USER, label="Регистрация"),
            ft.NavigationBarDestination(icon=ft.icons.VERIFIED_USER_OUTLINED, label="Авторизация"),
        ],on_change=validate
    )
    page.add(panel_register,)



ft.app(target=maun)
