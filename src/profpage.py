from PyQt5.QtWidgets import (
   QWidget,  QLabel, QLineEdit, QPushButton,
    QVBoxLayout,  QMessageBox, QFormLayout
)
from PyQt5.QtGui import  QFont, QDoubleValidator
from PyQt5.QtCore import Qt

from database_connection import create_connection


class ProfilePage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 30, 50, 30)

        # عنوان
        title_label = QLabel("پروفایل کاربری")
        title_label.setFont(QFont("B Nazanin", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # فرم اطلاعات کاربر
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setContentsMargins(50, 30, 50, 30)

        # نام کاربری فعلی
        self.current_username = QLineEdit()
        self.current_username.setReadOnly(True)
        self.current_username.setStyleSheet("""
            QLineEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
            }
        """)
        form_layout.addRow("نام کاربری فعلی:", self.current_username)

        # نام کاربری جدید
        self.new_username_input = QLineEdit()
        self.new_username_input.setPlaceholderText("نام کاربری جدید را وارد کنید")
        form_layout.addRow("نام کاربری جدید:", self.new_username_input)

        # رمز عبور جدید
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("رمز عبور جدید را وارد کنید")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("رمز عبور جدید:", self.password_input)

        # تکرار رمز عبور جدید
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("رمز عبور جدید را تکرار کنید")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("تکرار رمز عبور جدید:", self.confirm_password_input)

        # برای مدیر و ادمین نمایش حقوق ماهیانه
        if self.parent.role in ['owner', 'admin']:
            self.salary_input = QLineEdit()
            self.salary_input.setValidator(QDoubleValidator(0, 999999999, 0))
            form_layout.addRow("حقوق ماهیانه (تومان):", self.salary_input)

        # برای کارمندان نمایش دستمزد ساعتی
        if self.parent.role == 'staff':
            self.wage_input = QLineEdit()
            self.wage_input.setValidator(QDoubleValidator(0, 999999, 0))
            form_layout.addRow("دستمزد ساعتی (تومان):", self.wage_input)

        layout.addLayout(form_layout)

        # دکمه ذخیره
        save_button = QPushButton("ذخیره تغییرات")
        save_button.setFont(QFont("B Nazanin", 12))
        save_button.setMinimumHeight(45)
        save_button.setStyleSheet("background-color: #27ae60; color: white;")
        save_button.clicked.connect(self.save_profile)
        layout.addWidget(save_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def load_profile(self):
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT username, monthly_salary, hourly_wage FROM users WHERE id=?", (self.parent.user_id,))
        user = c.fetchone()
        conn.close()

        if user:
            username, monthly_salary, hourly_wage = user

            self.current_username.setText(username)

            if self.parent.role in ['owner', 'admin']:
                self.salary_input.setText(str(monthly_salary))

            if self.parent.role == 'staff':
                self.wage_input.setText(str(hourly_wage))

    def save_profile(self):
        new_username = self.new_username_input.text().strip()
        new_password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        # بررسی تطابق رمزهای عبور
        if new_password and new_password != confirm_password:
            QMessageBox.warning(self, "خطا", "رمزهای عبور وارد شده مطابقت ندارند.")
            return

        # به‌روزرسانی اطلاعات در دیتابیس
        conn = create_connection()
        c = conn.cursor()

        update_fields = []
        params = []

        # به‌روزرسانی نام کاربری
        if new_username:
            # بررسی تکراری نبودن نام کاربری جدید
            c.execute("SELECT COUNT(*) FROM users WHERE username=?", (new_username,))
            if c.fetchone()[0] > 0:
                QMessageBox.warning(self, "خطا", "نام کاربری جدید تکراری است. لطفاً نام دیگری انتخاب کنید.")
                conn.close()
                return

            update_fields.append("username = ?")
            params.append(new_username)

        # به‌روزرسانی رمز عبور
        if new_password:
            update_fields.append("password = ?")
            params.append(new_password)

        # به‌روزرسانی حقوق ماهیانه برای مدیر/ادمین
        if self.parent.role in ['owner', 'admin']:
            try:
                new_salary = float(self.salary_input.text()) if self.salary_input.text() else None
                update_fields.append("monthly_salary = ?")
                params.append(new_salary)
            except ValueError:
                QMessageBox.warning(self, "خطا", "مقدار حقوق ماهیانه نامعتبر است.")
                conn.close()
                return

        # به‌روزرسانی دستمزد ساعتی برای کارمندان
        if self.parent.role == 'staff':
            try:
                new_wage = float(self.wage_input.text()) if self.wage_input.text() else None
                update_fields.append("hourly_wage = ?")
                params.append(new_wage)
            except ValueError:
                QMessageBox.warning(self, "خطا", "مقدار دستمزد ساعتی نامعتبر است.")
                conn.close()
                return

        # اگر هیچ فیلدی برای به‌روزرسانی وجود ندارد
        if not update_fields:
            QMessageBox.information(self, "اطلاع", "هیچ تغییری اعمال نشد.")
            conn.close()
            return

        # اجرای کوئری به‌روزرسانی
        update_query = "UPDATE users SET " + ", ".join(update_fields) + " WHERE id = ?"
        params.append(self.parent.user_id)

        c.execute(update_query, params)
        conn.commit()
        conn.close()

        QMessageBox.information(self, "موفقیت", "تغییرات با موفقیت ذخیره شد.")
        self.load_profile()
        self.parent.update_status_bar()  # به‌روزرسانی نوار وضعیت