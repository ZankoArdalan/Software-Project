import sys
import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QMessageBox,
    QCheckBox, QStatusBar,
    QToolButton, QFrame, QButtonGroup, QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, QSize

from backpage import BackupPage
from database_connection import create_connection
from emppage import EmployeePage
from product import ProductPage
from profpage import ProfilePage
from reportpage import ReportsPage
from salepage import SalesPage
from shitpage import ShiftPage


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ورود به سیستم مدیریت لباس فروشی")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(500, 400)
        
        # تنظیم پس‌زمینه
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 248, 255))
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # هدر با لوگو و عنوان
        header_layout = QHBoxLayout()
        
        # لوگو
        logo_label = QLabel()
        pixmap = QPixmap("logo.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo_label)
        
        # عنوان
        title_label = QLabel("سیستم مدیریت لباس فروشی")
        title_label.setFont(QFont("B Nazanin", 20, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # دکمه راهنما
        help_button = QToolButton()
        help_button.setIcon(QIcon("help.png"))
        help_button.setIconSize(QSize(30, 30))
        help_button.setToolTip("راهنما")
        help_button.setStyleSheet("""
            QToolButton {
                background-color: #3498db;
                border-radius: 15px;
                padding: 5px;
            }
            QToolButton:hover {
                background-color: #2980b9;
            }
        """)
        help_button.clicked.connect(self.show_help)
        header_layout.addWidget(help_button)
        
        main_layout.addLayout(header_layout)

        # فرم ورود
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # فیلد نام کاربری
        username_layout = QHBoxLayout()
        username_label = QLabel("نام کاربری:")
        username_label.setFont(QFont("B Nazanin", 12))
        username_label.setFixedWidth(100)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("نام کاربری خود را وارد کنید")
        self.username_input.setFont(QFont("B Nazanin", 11))
        self.username_input.setMinimumHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        form_layout.addLayout(username_layout)

        # فیلد رمز عبور
        password_layout = QHBoxLayout()
        password_label = QLabel("رمز عبور:")
        password_label.setFont(QFont("B Nazanin", 12))
        password_label.setFixedWidth(100)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("رمز عبور خود را وارد کنید")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("B Nazanin", 11))
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        form_layout.addLayout(password_layout)

        # نمایش/عدم نمایش رمز عبور
        self.show_password = QCheckBox("نمایش رمز عبور")
        self.show_password.setFont(QFont("B Nazanin", 10))
        self.show_password.stateChanged.connect(self.toggle_password_visibility)
        form_layout.addWidget(self.show_password)

        main_layout.addLayout(form_layout)

        # دکمه ورود
        login_button = QPushButton("ورود به سیستم")
        login_button.setFont(QFont("B Nazanin", 12, QFont.Bold))
        login_button.setMinimumHeight(45)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
        """)
        login_button.clicked.connect(self.authenticate)
        main_layout.addWidget(login_button)

        self.setLayout(main_layout)

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            
    def show_help(self):
        help_text = (
            "در صورت داشتن هر گونه سوال یا بروز هرگونه مشکلی با اطلاعات زیر در ارتباط باشید:\n\n"
            "شماره تماس: 09142148859\n"
            "آیدی تلگرام: @nima_saadati\n"
            "ایمیل: saadatinima7832@gmail.com"
        )
        QMessageBox.information(self, "راهنما و پشتیبانی", help_text)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            user_id, username, password, role, hourly_wage, monthly_salary = user
            self.accept()
            return user_id, role
        else:
            QMessageBox.warning(self, "خطا در ورود", "نام کاربری یا رمز عبور اشتباه است!")
            return None


class MainWindow(QMainWindow):
    def __init__(self, user_id, role):
        super().__init__()
        self.user_id = user_id
        self.role = role
        self.setWindowTitle(f"سیستم مدیریت لباس فروشی - کاربر: {role}")
        self.setWindowIcon(QIcon("icon.png"))
        self.setMinimumSize(1200, 800)
        
        # تنظیم استایل کلی
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QWidget {
                font-family: 'B Nazanin';
                font-size: 11pt;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                min-height: 30px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #dfe4ea;
                border-radius: 5px;
                gridline-color: #dfe4ea;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
            QGroupBox {
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 20px;
                font-weight: bold;
                padding: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: #3498db;
                color: white;
                border-radius: 5px;
            }
        """)

        # ایجاد لایه اصلی
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ایجاد نوار کناری
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-right: 1px solid #34495e;
            }
            QPushButton {
                background-color: transparent;
                color: #ecf0f1;
                text-align: left;
                padding: 15px 20px;
                border: none;
                border-radius: 0;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #3498db;
                border-left: 4px solid #ecf0f1;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setSpacing(5)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)

        # عنوان نوار کناری
        sidebar_title = QLabel("منوی سیستم")
        sidebar_title.setFont(QFont("B Nazanin", 14, QFont.Bold))
        sidebar_title.setStyleSheet("color: #ecf0f1; padding: 10px 20px;")
        sidebar_title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(sidebar_title)

        # خط جداکننده
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #34495e;")
        sidebar_layout.addWidget(separator)

        # ایجاد گروه دکمه‌ها برای انتخاب صفحه
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)

        # دکمه‌های نوار کناری
        buttons = [
            ("مدیریت محصولات", self.show_product_page),
            ("مدیریت فروش", self.show_sales_page),
            ("گزارشات", self.show_reports_page),
        ]

        if role in ['owner', 'admin']:
            buttons.append(("مدیریت کارکنان", self.show_employee_page))
            
        buttons.append(("پروفایل کاربری", self.show_profile_page))
            
        if role in ['owner', 'admin']:
            buttons.append(("پشتیبان‌گیری", self.show_backup_page))
            
        if role == 'staff':
            buttons.append(("مدیریت شیفت", self.show_shift_page))

        buttons.append(("خروج", self.close))

        for text, handler in buttons:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFont(QFont("B Nazanin", 11))
            btn.setFixedHeight(50)
            btn.clicked.connect(handler)
            self.button_group.addButton(btn)
            sidebar_layout.addWidget(btn)

        # اسپیسر برای پر کردن فضای خالی
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sidebar_layout.addWidget(spacer)

        main_layout.addWidget(sidebar)

        # ویجت صفحه‌بندی شده
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background-color: white;
                border-radius: 10px;
                margin: 15px;
                padding: 15px;
                border: 1px solid #dfe4ea;
            }
        """)
        main_layout.addWidget(self.stacked_widget, 1)

        # صفحات مختلف
        self.product_page = ProductPage(self)
        self.sales_page = SalesPage(self)
        self.reports_page = ReportsPage(self, role)
        self.employee_page = EmployeePage(self, role)
        self.profile_page = ProfilePage(self)
        self.backup_page = BackupPage(self)
        self.shift_page = ShiftPage(self)

        # افزودن صفحات به ویجت صفحه‌بندی شده
        self.stacked_widget.addWidget(self.product_page)
        self.stacked_widget.addWidget(self.sales_page)
        self.stacked_widget.addWidget(self.reports_page)
        self.stacked_widget.addWidget(self.employee_page)
        self.stacked_widget.addWidget(self.profile_page)
        self.stacked_widget.addWidget(self.backup_page)
        self.stacked_widget.addWidget(self.shift_page)

        # نمایش صفحه پیش‌فرض
        self.show_product_page()

        # نوار وضعیت
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #2c3e50;
                color: white;
                padding: 5px;
            }
        """)
        self.setStatusBar(self.status_bar)
        self.update_status_bar()

    def update_status_bar(self):
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE id=?", (self.user_id,))
        username = c.fetchone()[0]
        conn.close()

        current_date = datetime.datetime.now().strftime("%Y/%m/%d")
        status_text = f"کاربر: {username} | نقش: {self.role} | تاریخ: {current_date}"
        self.status_bar.showMessage(status_text)

    def show_product_page(self):
        self.stacked_widget.setCurrentWidget(self.product_page)
        self.product_page.load_products()
        self.setWindowTitle(f"سیستم مدیریت لباس فروشی - مدیریت محصولات")
        self.update_button_state("مدیریت محصولات")

    def show_sales_page(self):
        self.stacked_widget.setCurrentWidget(self.sales_page)
        self.sales_page.load_products()
        self.setWindowTitle(f"سیستم مدیریت لباس فروشی - مدیریت فروش")
        self.update_button_state("مدیریت فروش")

    def show_reports_page(self):
        self.stacked_widget.setCurrentWidget(self.reports_page)
        self.reports_page.load_data()
        self.setWindowTitle(f"سیستم مدیریت لباس فروشی - گزارشات")
        self.update_button_state("گزارشات")

    def show_employee_page(self):
        self.stacked_widget.setCurrentWidget(self.employee_page)
        self.employee_page.load_employees()
        self.setWindowTitle(f"سیستم مدیریت لباس فروشی - مدیریت کارکنان")
        self.update_button_state("مدیریت کارکنان")

    def show_profile_page(self):
        self.stacked_widget.setCurrentWidget(self.profile_page)
        self.profile_page.load_profile()
        self.setWindowTitle(f"سیستم مدیریت لباس فروشی - پروفایل کاربری")
        self.update_button_state("پروفایل کاربری")

    def show_backup_page(self):
        self.stacked_widget.setCurrentWidget(self.backup_page)
        self.setWindowTitle(f"سیستم مدیریت لباس فروشی - پشتیبان‌گیری")
        self.update_button_state("پشتیبان‌گیری")

    def show_shift_page(self):
        self.stacked_widget.setCurrentWidget(self.shift_page)
        self.shift_page.load_shifts()
        self.setWindowTitle(f"سیستم مدیریت لباس فروشی - مدیریت شیفت")
        self.update_button_state("مدیریت شیفت")
        
    def update_button_state(self, button_text):
        for button in self.button_group.buttons():
            if button.text() == button_text:
                button.setChecked(True)
            else:
                button.setChecked(False)


if __name__ == "__main__":
    # ایجاد دیتابیس و جداول
    create_connection()

    app = QApplication(sys.argv)
    app.setFont(QFont("B Nazanin", 11))

    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        user_id, role = login_window.authenticate()
        if user_id:
            main_window = MainWindow(user_id, role)
            main_window.show()
            sys.exit(app.exec_())
    else:
        sys.exit()