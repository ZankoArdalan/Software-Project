from PyQt5.QtWidgets import (
    QWidget, QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget,
    QTableWidgetItem, QComboBox, QHeaderView, QFormLayout
)
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator
from PyQt5.QtCore import Qt

from database_connection import create_connection


class EmployeePage(QWidget):
    def __init__(self, parent, role):
        super().__init__()
        self.parent = parent
        self.role = role
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # عنوان صفحه
        title_label = QLabel("مدیریت کارکنان")
        title_label.setFont(QFont("B Nazanin", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # بخش جستجو
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        search_label = QLabel("جستجوی کارمند:")
        search_label.setFont(QFont("B Nazanin", 12))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("نام کاربری...")
        self.search_input.textChanged.connect(self.search_employees)
        self.search_input.setFont(QFont("B Nazanin", 11))
        self.search_input.setMinimumHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
        """)

        search_button = QPushButton("جستجو")
        search_button.setFont(QFont("B Nazanin", 11))
        search_button.setMinimumHeight(40)
        search_button.setStyleSheet("background-color: #3498db; color: white;")
        search_button.clicked.connect(self.search_employees)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        # جدول کارکنان
        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(6)
        self.employees_table.setHorizontalHeaderLabels(
            ["ID", "نام کاربری", "نقش", "حقوق ماهیانه", "دستمزد ساعتی", "عملیات"])
        self.employees_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.employees_table.verticalHeader().setVisible(False)
        self.employees_table.setFont(QFont("B Nazanin", 10))
        self.employees_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #dfe4ea;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.employees_table.setEditTriggers(QTableWidget.NoEditTriggers)

        main_layout.addWidget(self.employees_table)

        # دکمه‌های مدیریت
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        add_button = QPushButton("افزودن کارمند")
        add_button.setIcon(QIcon("add_employee.png"))
        add_button.setFont(QFont("B Nazanin", 12))
        add_button.setMinimumHeight(45)
        add_button.setStyleSheet("background-color: #27ae60; color: white;")
        add_button.clicked.connect(self.add_employee)
        buttons_layout.addWidget(add_button)

        edit_button = QPushButton("ویرایش کارمند")
        edit_button.setIcon(QIcon("edit_employee.png"))
        edit_button.setFont(QFont("B Nazanin", 12))
        edit_button.setMinimumHeight(45)
        edit_button.setStyleSheet("background-color: #f39c12; color: white;")
        edit_button.clicked.connect(self.edit_employee)
        buttons_layout.addWidget(edit_button)

        delete_button = QPushButton("حذف کارمند")
        delete_button.setIcon(QIcon("delete_employee.png"))
        delete_button.setFont(QFont("B Nazanin", 12))
        delete_button.setMinimumHeight(45)
        delete_button.setStyleSheet("background-color: #e74c3c; color: white;")
        delete_button.clicked.connect(self.delete_employee)
        buttons_layout.addWidget(delete_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def load_employees(self):
        conn = create_connection()
        c = conn.cursor()

        # نمایش کارکنان و ادمین‌ها (به جز مدیر اصلی)
        c.execute("SELECT id, username, role, monthly_salary, hourly_wage FROM users WHERE role != 'owner'")
        employees = c.fetchall()
        conn.close()

        self.employees_table.setRowCount(len(employees))

        for row, employee in enumerate(employees):
            user_id, username, role, monthly_salary, hourly_wage = employee

            self.employees_table.setItem(row, 0, QTableWidgetItem(str(user_id)))
            self.employees_table.item(row, 0).setTextAlignment(Qt.AlignCenter)

            self.employees_table.setItem(row, 1, QTableWidgetItem(username))

            self.employees_table.setItem(row, 2, QTableWidgetItem(role))

            self.employees_table.setItem(row, 3, QTableWidgetItem(f"{monthly_salary:,.0f}" if monthly_salary else "-"))
            self.employees_table.item(row, 3).setTextAlignment(Qt.AlignCenter)

            self.employees_table.setItem(row, 4, QTableWidgetItem(f"{hourly_wage:,.0f}" if hourly_wage else "-"))
            self.employees_table.item(row, 4).setTextAlignment(Qt.AlignCenter)

            # دکمه ویرایش
            edit_button = QPushButton("ویرایش")
            edit_button.setFont(QFont("B Nazanin", 10))
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                    min-width: 80px;
                }
            """)
            edit_button.clicked.connect(lambda _, e=employee: self.edit_employee(e))
            self.employees_table.setCellWidget(row, 5, edit_button)

    def search_employees(self):
        search_text = self.search_input.text().strip()

        conn = create_connection()
        c = conn.cursor()

        query = "SELECT id, username, role, monthly_salary, hourly_wage FROM users WHERE role != 'owner'"
        params = []

        if search_text:
            query += " AND username LIKE ?"
            params.append(f"%{search_text}%")

        c.execute(query, params)
        employees = c.fetchall()
        conn.close()

        self.employees_table.setRowCount(len(employees))

        for row, employee in enumerate(employees):
            user_id, username, role, monthly_salary, hourly_wage = employee

            self.employees_table.setItem(row, 0, QTableWidgetItem(str(user_id)))
            self.employees_table.item(row, 0).setTextAlignment(Qt.AlignCenter)

            self.employees_table.setItem(row, 1, QTableWidgetItem(username))

            self.employees_table.setItem(row, 2, QTableWidgetItem(role))

            self.employees_table.setItem(row, 3, QTableWidgetItem(f"{monthly_salary:,.0f}" if monthly_salary else "-"))
            self.employees_table.item(row, 3).setTextAlignment(Qt.AlignCenter)

            self.employees_table.setItem(row, 4, QTableWidgetItem(f"{hourly_wage:,.0f}" if hourly_wage else "-"))
            self.employees_table.item(row, 4).setTextAlignment(Qt.AlignCenter)

            edit_button = QPushButton("ویرایش")
            edit_button.setFont(QFont("B Nazanin", 10))
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                    min-width: 80px;
                }
            """)
            edit_button.clicked.connect(lambda _, e=employee: self.edit_employee(e))
            self.employees_table.setCellWidget(row, 5, edit_button)

    def add_employee(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("افزودن کارمند جدید")
        dialog.setFixedSize(500, 400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
            QLabel {
                font-family: 'B Nazanin';
                font-size: 11pt;
            }
            QLineEdit, QComboBox {
                font-family: 'B Nazanin';
                font-size: 11pt;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                min-height: 35px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # عنوان
        title_label = QLabel("افزودن کارمند جدید")
        title_label.setFont(QFont("B Nazanin", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # فیلدهای فرم
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # نام کاربری
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("نام کاربری را وارد کنید")
        form_layout.addRow("نام کاربری:", self.username_input)

        # رمز عبور
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("رمز عبور را وارد کنید")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("رمز عبور:", self.password_input)

        # نقش
        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "staff"])
        self.role_combo.currentTextChanged.connect(self.update_salary_fields)
        form_layout.addRow("نقش:", self.role_combo)

        # حقوق ماهیانه
        self.monthly_salary_input = QLineEdit()
        self.monthly_salary_input.setPlaceholderText("حقوق ماهیانه به تومان")
        self.monthly_salary_input.setValidator(QDoubleValidator(0, 999999999, 0))
        form_layout.addRow("حقوق ماهیانه (تومان):", self.monthly_salary_input)

        # دستمزد ساعتی
        self.hourly_wage_input = QLineEdit()
        self.hourly_wage_input.setPlaceholderText("دستمزد ساعتی به تومان")
        self.hourly_wage_input.setValidator(QDoubleValidator(0, 999999, 0))
        form_layout.addRow("دستمزد ساعتی (تومان):", self.hourly_wage_input)

        layout.addLayout(form_layout)

        # تنظیم پیش‌فرض بر اساس نقش
        self.update_salary_fields()

        # دکمه‌های فرم
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        save_button = QPushButton("ذخیره کارمند")
        save_button.setFont(QFont("B Nazanin", 12))
        save_button.setMinimumHeight(45)
        save_button.setStyleSheet("background-color: #27ae60; color: white;")
        save_button.clicked.connect(lambda: self.save_employee(dialog))
        buttons_layout.addWidget(save_button)

        cancel_button = QPushButton("لغو")
        cancel_button.setFont(QFont("B Nazanin", 12))
        cancel_button.setMinimumHeight(45)
        cancel_button.setStyleSheet("background-color: #e74c3c; color: white;")
        cancel_button.clicked.connect(dialog.close)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def update_salary_fields(self):
        role = self.role_combo.currentText()
        if role == "admin":
            self.monthly_salary_input.setEnabled(True)
            self.hourly_wage_input.setEnabled(False)
            self.hourly_wage_input.clear()
        else:  # staff
            self.monthly_salary_input.setEnabled(False)
            self.monthly_salary_input.clear()
            self.hourly_wage_input.setEnabled(True)

    def save_employee(self, dialog):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()
        monthly_salary = self.monthly_salary_input.text().strip()
        hourly_wage = self.hourly_wage_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "خطا", "پر کردن فیلدهای نام کاربری و رمز عبور الزامی است.")
            return

        # تبدیل مقادیر حقوق به عدد
        try:
            monthly_salary = float(monthly_salary) if monthly_salary else None
            hourly_wage = float(hourly_wage) if hourly_wage else None
        except ValueError:
            QMessageBox.warning(self, "خطا", "مقادیر حقوق باید عددی باشند.")
            return

        # بررسی تکراری نبودن نام کاربری
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
        if c.fetchone()[0] > 0:
            QMessageBox.warning(self, "خطا", "نام کاربری تکراری است. لطفاً نام دیگری انتخاب کنید.")
            conn.close()
            return

        # ذخیره کارمند جدید
        c.execute("""
        INSERT INTO users (username, password, role, monthly_salary, hourly_wage)
        VALUES (?, ?, ?, ?, ?)
        """, (username, password, role, monthly_salary, hourly_wage))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "موفقیت", "کارمند جدید با موفقیت اضافه شد.")
        dialog.close()
        self.load_employees()

    def edit_employee(self, employee=None):
        if not employee:
            selected_row = self.employees_table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "خطا", "لطفاً یک کارمند را انتخاب کنید.")
                return

            user_id = int(self.employees_table.item(selected_row, 0).text())
            username = self.employees_table.item(selected_row, 1).text()
            role = self.employees_table.item(selected_row, 2).text()
            monthly_salary = self.employees_table.item(selected_row, 3).text().replace(",", "").replace("-", "") or None
            hourly_wage = self.employees_table.item(selected_row, 4).text().replace(",", "").replace("-", "") or None

            employee = (user_id, username, role, monthly_salary, hourly_wage)

        user_id, username, role, monthly_salary, hourly_wage = employee

        dialog = QDialog(self)
        dialog.setWindowTitle(f"ویرایش کارمند: {username}")
        dialog.setFixedSize(500, 400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
            QLabel {
                font-family: 'B Nazanin';
                font-size: 11pt;
            }
            QLineEdit, QComboBox {
                font-family: 'B Nazanin';
                font-size: 11pt;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                min-height: 35px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # عنوان
        title_label = QLabel(f"ویرایش کارمند: {username}")
        title_label.setFont(QFont("B Nazanin", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # فیلدهای ویرایش
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # نام کاربری جدید
        self.new_username_input = QLineEdit(username)
        form_layout.addRow("نام کاربری جدید:", self.new_username_input)

        # نقش جدید
        self.new_role_combo = QComboBox()
        self.new_role_combo.addItems(["admin", "staff"])
        self.new_role_combo.setCurrentText(role)
        self.new_role_combo.currentTextChanged.connect(self.update_salary_fields_edit)
        form_layout.addRow("نقش جدید:", self.new_role_combo)

        # حقوق ماهیانه جدید
        self.new_monthly_input = QLineEdit()
        self.new_monthly_input.setValidator(QDoubleValidator(0, 999999999, 0))
        if monthly_salary:
            self.new_monthly_input.setText(str(monthly_salary))
        form_layout.addRow("حقوق ماهیانه جدید (تومان):", self.new_monthly_input)

        # دستمزد ساعتی جدید
        self.new_hourly_input = QLineEdit()
        self.new_hourly_input.setValidator(QDoubleValidator(0, 999999, 0))
        if hourly_wage:
            self.new_hourly_input.setText(str(hourly_wage))
        form_layout.addRow("دستمزد ساعتی جدید (تومان):", self.new_hourly_input)

        layout.addLayout(form_layout)

        # تنظیم پیش‌فرض بر اساس نقش
        self.update_salary_fields_edit()

        # دکمه‌های فرم
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        save_button = QPushButton("ذخیره تغییرات")
        save_button.setFont(QFont("B Nazanin", 12))
        save_button.setMinimumHeight(45)
        save_button.setStyleSheet("background-color: #27ae60; color: white;")
        save_button.clicked.connect(lambda: self.update_employee(user_id, dialog))
        buttons_layout.addWidget(save_button)

        cancel_button = QPushButton("لغو")
        cancel_button.setFont(QFont("B Nazanin", 12))
        cancel_button.setMinimumHeight(45)
        cancel_button.setStyleSheet("background-color: #e74c3c; color: white;")
        cancel_button.clicked.connect(dialog.close)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def update_salary_fields_edit(self):
        role = self.new_role_combo.currentText()
        if role == "admin":
            self.new_monthly_input.setEnabled(True)
            self.new_hourly_input.setEnabled(False)
            self.new_hourly_input.clear()
        else:  # staff
            self.new_monthly_input.setEnabled(False)
            self.new_monthly_input.clear()
            self.new_hourly_input.setEnabled(True)

    def update_employee(self, user_id, dialog):
        new_username = self.new_username_input.text().strip()
        new_role = self.new_role_combo.currentText()
        new_monthly = self.new_monthly_input.text().strip()
        new_hourly = self.new_hourly_input.text().strip()

        if not new_username:
            QMessageBox.warning(self, "خطا", "نام کاربری نمی‌تواند خالی باشد.")
            return

        try:
            new_monthly = float(new_monthly) if new_monthly else None
            new_hourly = float(new_hourly) if new_hourly else None
        except ValueError:
            QMessageBox.warning(self, "خطا", "مقادیر حقوق باید عددی باشند.")
            return

        conn = create_connection()
        c = conn.cursor()

        # بررسی تکراری نبودن نام کاربری جدید
        if new_username != self.new_username_input.text():
            c.execute("SELECT COUNT(*) FROM users WHERE username=?", (new_username,))
            if c.fetchone()[0] > 0:
                QMessageBox.warning(self, "خطا", "نام کاربری جدید تکراری است. لطفاً نام دیگری انتخاب کنید.")
                conn.close()
                return

        # به‌روزرسانی اطلاعات
        c.execute("""
        UPDATE users 
        SET username=?, role=?, monthly_salary=?, hourly_wage=?
        WHERE id=?
        """, (new_username, new_role, new_monthly, new_hourly, user_id))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "موفقیت", "اطلاعات کارمند با موفقیت به‌روزرسانی شد.")
        dialog.close()
        self.load_employees()

    def delete_employee(self):
        selected_row = self.employees_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطا", "لطفاً یک کارمند را انتخاب کنید.")
            return

        user_id = int(self.employees_table.item(selected_row, 0).text())
        username = self.employees_table.item(selected_row, 1).text()

        reply = QMessageBox.question(self, "تأیید حذف",
                                     f"آیا از حذف کارمند '{username}' مطمئن هستید؟",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            conn = create_connection()
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "موفقیت", "کارمند با موفقیت حذف شد.")
            self.load_employees()