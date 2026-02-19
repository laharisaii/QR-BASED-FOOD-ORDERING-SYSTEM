from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
			path("Login.html", views.Login, name="Login"),
			path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
			path("Register.html", views.Register, name="Register"),
			path("SignupAction", views.SignupAction, name="SignupAction"),
			path("AddChairs.html", views.AddChairs, name="AddChairs"),
			path("AddChairsAction", views.AddChairsAction, name="AddChairsAction"),	
			path("CreateMenu.html", views.CreateMenu, name="CreateMenu"),
			path("CreateMenuAction", views.CreateMenuAction, name="CreateMenuAction"),	
			path("ViewMenu", views.ViewMenu, name="ViewMenu"),	
			path("ViewRestaurants", views.ViewRestaurants, name="ViewRestaurants"),
			path("DownloadAction", views.DownloadAction, name="DownloadAction"),
			path("ScanQR.html", views.ScanQR, name="ScanQR"),
			path("BookOrder", views.BookOrder, name="BookOrder"),
			path("ViewBills", views.ViewBills, name="ViewBills"),
			path("ViewOrders", views.ViewOrders, name="ViewOrders"),
			path("ShowMenu", views.ShowMenu, name="ShowMenu"),
]