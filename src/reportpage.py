import datetime
from PyQt5.QtWidgets import (
    QWidget, QDialog, QLabel,QPushButton,
    QVBoxLayout, QHBoxLayout,QMessageBox, QTableWidget,
    QTableWidgetItem, QDateEdit, QHeaderView,
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QDate, QSize

from database_connection import create_connection


class ReportsPage(QWidget):
    def __init__(self, parent, role):
        super().__init__()
        self.parent = parent
        self.role = role
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # عنوان صفحه
        title_label = QLabel("گزارشات سیستم")
        title_label.setFont(QFont("B Nazanin", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # دکمه‌های گزارشات
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)
        buttons_layout.setContentsMargins(50, 30, 50, 30)

        # دکمه گزارش روزانه
        daily_button = QPushButton("گزارش روزانه")
        daily_button.setIcon(QIcon("daily_report.png"))
        daily_button.setIconSize(QSize(60, 60))
        daily_button.setFont(QFont("B Nazanin", 14, QFont.Bold))
        daily_button.setMinimumSize(250, 150)
        daily_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        daily_button.clicked.connect(self.show_daily_report)
        buttons_layout.addWidget(daily_button)

        # دکمه گزارش هفتگی
        weekly_button = QPushButton("گزارش هفتگی")
        weekly_button.setIcon(QIcon("weekly_report.png"))
        weekly_button.setIconSize(QSize(60, 60))
        weekly_button.setFont(QFont("B Nazanin", 14, QFont.Bold))
        weekly_button.setMinimumSize(250, 150)
        weekly_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        weekly_button.clicked.connect(self.show_weekly_report)
        buttons_layout.addWidget(weekly_button)

        # دکمه گزارش شیفت
        shift_button = QPushButton("گزارش شیفت")
        shift_button.setIcon(QIcon("shift_report.png"))
        shift_button.setIconSize(QSize(60, 60))
        shift_button.setFont(QFont("B Nazanin", 14, QFont.Bold))
        shift_button.setMinimumSize(250, 150)
        shift_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        shift_button.clicked.connect(self.show_shift_report)
        buttons_layout.addWidget(shift_button)

        main_layout.addLayout(buttons_layout)

        # توضیحات
        desc_label = QLabel(
            "برای مشاهده هر گزارش، دکمه مربوطه را انتخاب کنید. گزارش روزانه شامل فروش‌های یک روز خاص، "
            "گزارش هفتگی فروش‌های هفته جاری و گزارش شیفت زمان‌های ورود و خروج کارکنان را نمایش می‌دهد."
        )
        desc_label.setFont(QFont("B Nazanin", 11))
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #7f8c8d; padding: 20px;")
        desc_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc_label)

        self.setLayout(main_layout)

    def load_data(self):
        # این تابع دیگر استفاده نمی‌شود
        pass

    def show_daily_report(self):
        # ایجاد دیالوگ برای انتخاب تاریخ
        dialog = QDialog(self)
        dialog.setWindowTitle("گزارش روزانه")
        dialog.setFixedSize(400, 200)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
            QLabel {
                font-family: 'B Nazanin';
                font-size: 12pt;
            }
            QPushButton {
                font-family: 'B Nazanin';
                font-size: 11pt;
                min-height: 35px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title_label = QLabel("انتخاب تاریخ برای گزارش روزانه")
        title_label.setFont(QFont("B Nazanin", 14))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # انتخاب تاریخ
        date_layout = QHBoxLayout()
        date_label = QLabel("تاریخ:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setFont(QFont("B Nazanin", 11))

        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        # دکمه‌ها
        buttons_layout = QHBoxLayout()

        show_button = QPushButton("نمایش گزارش")
        show_button.setStyleSheet("background-color: #3498db; color: white;")
        show_button.clicked.connect(lambda: self.generate_daily_report(dialog))
        buttons_layout.addWidget(show_button)

        cancel_button = QPushButton("لغو")
        cancel_button.setStyleSheet("background-color: #e74c3c; color: white;")
        cancel_button.clicked.connect(dialog.close)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def generate_daily_report(self, dialog):
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")

        conn = create_connection()
        c = conn.cursor()

        # دریافت فروش‌های روز انتخاب شده
        c.execute("""
            SELECT s.id, s.sale_date, p.name, s.quantity, s.total_price, u.username 
            FROM sales s
            JOIN products p ON s.product_id = p.id
            JOIN users u ON s.user_id = u.id
            WHERE DATE(s.sale_date) = ?
        """, (selected_date,))

        sales = c.fetchall()
        conn.close()

        if not sales:
            QMessageBox.information(self, "گزارش روزانه", "هیچ فروشی در تاریخ انتخاب شده ثبت نشده است.")
            dialog.close()
            return

        # ایجاد پنجره نمایش گزارش
        report_dialog = QDialog(self)
        report_dialog.setWindowTitle(f"گزارش فروش روزانه - تاریخ {selected_date}")
        report_dialog.setMinimumSize(800, 600)
        report_dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-family: 'B Nazanin';
                font-size: 11pt;
            }
            QTableWidget {
                font-family: 'B Nazanin';
                font-size: 10pt;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # عنوان گزارش
        title_label = QLabel(f"گزارش فروش روزانه - تاریخ {selected_date}")
        title_label.setFont(QFont("B Nazanin", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # جدول گزارش
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "زمان فروش", "نام محصول", "تعداد", "قیمت کل", "کارمند"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setRowCount(len(sales))

        total_sales = 0
        total_revenue = 0

        for row, sale in enumerate(sales):
            sale_id, sale_date, product_name, quantity, total_price, username = sale

            # نمایش تاریخ به صورت خوانا
            sale_time = datetime.datetime.strptime(sale_date, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")

            table.setItem(row, 0, QTableWidgetItem(str(sale_id)))
            table.item(row, 0).setTextAlignment(Qt.AlignCenter)

            table.setItem(row, 1, QTableWidgetItem(sale_time))
            table.item(row, 1).setTextAlignment(Qt.AlignCenter)

            table.setItem(row, 2, QTableWidgetItem(product_name))

            table.setItem(row, 3, QTableWidgetItem(str(quantity)))
            table.item(row, 3).setTextAlignment(Qt.AlignCenter)

            table.setItem(row, 4, QTableWidgetItem(f"{total_price:,.0f}"))
            table.item(row, 4).setTextAlignment(Qt.AlignCenter)

            table.setItem(row, 5, QTableWidgetItem(username))

            total_sales += quantity
            total_revenue += total_price

        # خلاصه گزارش
        summary_label = QLabel(
            f"<b>جمع‌بندی:</b> {len(sales)} فروش | "
            f"تعداد کل کالاها: {total_sales} | "
            f"درآمد کل: {total_revenue:,.0f} تومان"
        )
        summary_label.setFont(QFont("B Nazanin", 12))
        summary_label.setStyleSheet("color: #27ae60;")

        layout.addWidget(table)
        layout.addWidget(summary_label)

        report_dialog.setLayout(layout)
        dialog.close()
        report_dialog.exec_()

    def show_weekly_report(self):
        # تاریخ شروع هفته جاری (شنبه)
        today = QDate.currentDate()
        start_of_week = today.addDays(-today.dayOfWeek() + 1)  # Qt::Monday is 1

        conn = create_connection()
        c = conn.cursor()

        # دریافت فروش‌های هفته جاری
        c.execute("""
            SELECT s.id, s.sale_date, p.name, s.quantity, s.total_price, u.username 
            FROM sales s
            JOIN products p ON s.product_id = p.id
            JOIN users u ON s.user_id = u.id
            WHERE DATE(s.sale_date) >= ?
        """, (start_of_week.toString("yyyy-MM-dd"),))

        sales = c.fetchall()
        conn.close()

        if not sales:
            QMessageBox.information(self, "گزارش هفتگی", "هیچ فروشی در هفته جاری ثبت نشده است.")
            return

        # ایجاد پنجره نمایش گزارش
        report_dialog = QDialog(self)
        report_dialog.setWindowTitle(f"گزارش فروش هفتگی - از {start_of_week.toString('yyyy/MM/dd')}")
        report_dialog.setMinimumSize(800, 600)
        report_dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-family: 'B Nazanin';
                font-size: 11pt;
            }
            QTableWidget {
                font-family: 'B Nazanin';
                font-size: 10pt;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # عنوان گزارش
        title_label = QLabel(
            f"گزارش فروش هفتگی - از {start_of_week.toString('yyyy/MM/dd')} تا {today.toString('yyyy/MM/dd')}")
        title_label.setFont(QFont("B Nazanin", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # جدول گزارش
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["ID", "تاریخ", "زمان", "نام محصول", "تعداد", "قیمت کل", "کارمند"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setRowCount(len(sales))

        total_sales = 0
        total_revenue = 0

        for row, sale in enumerate(sales):
            sale_id, sale_date, product_name, quantity, total_price, username = sale

            # نمایش تاریخ به صورت خوانا
            sale_datetime = datetime.datetime.strptime(sale_date, "%Y-%m-%d %H:%M:%S")
            sale_date_str = sale_datetime.strftime("%Y/%m/%d")
            sale_time_str = sale_datetime.strftime("%H:%M")

            table.setItem(row, 0, QTableWidgetItem(str(sale_id)))
            table.item(row, 0).setTextAlignment(Qt.AlignCenter)

            table.setItem(row, 1, QTableWidgetItem(sale_date_str))
            table.item(row, 1).setTextAlignment(Qt.AlignCenter)

            table.setItem(row, 2, QTableWidgetItem(sale_time_str))
            table.item(row, 2).setTextAlignment(Qt.AlignCenter)

            table.setItem(row, 3, QTableWidgetItem(product_name))

            table.setItem(row, 4, QTableWidgetItem(str(quantity)))
            table.item(row, 4).setTextAlignment(Qt.AlignCenter)

            table.setItem(row, 5, QTableWidgetItem(f"{total_price:,.0f}"))
            table.item(row, 5).setTextAlignment(Qt.AlignCenter)

            table.setItem(row, 6, QTableWidgetItem(username))

            total_sales += quantity
            total_revenue += total_price

        # خلاصه گزارش
        summary_label = QLabel(
            f"<b>جمع‌بندی:</b> {len(sales)} فروش | "
            f"تعداد کل کالاها: {total_sales} | "
            f"درآمد کل: {total_revenue:,.0f} تومان"
        )
        summary_label.setFont(QFont("B Nazanin", 12))
        summary_label.setStyleSheet("color: #27ae60;")

        layout.addWidget(table)
        layout.addWidget(summary_label)

        report_dialog.setLayout(layout)
        report_dialog.exec_()

    def show_shift_report(self):
        # ایجاد دیالوگ برای انتخاب تاریخ
        dialog = QDialog(self)
        dialog.setWindowTitle("گزارش شیفت")
        dialog.setFixedSize(400, 200)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
            QLabel {
                font-family: 'B Nazanin';
                font-size: 12pt;
            }
            QPushButton {
                font-family: 'B Nazanin';
                font-size: 11pt;
                min-height: 35px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title_label = QLabel("انتخاب تاریخ برای گزارش شیفت")
        title_label.setFont(QFont("B Nazanin", 14))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # انتخاب تاریخ
        date_layout = QHBoxLayout()
        date_label = QLabel("تاریخ:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setFont(QFont("B Nazanin", 11))

        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        # دکمه‌ها
        buttons_layout = QHBoxLayout()

        show_button = QPushButton("نمایش گزارش")
        show_button.setStyleSheet("background-color: #9b59b6; color: white;")
        show_button.clicked.connect(lambda: self.generate_shift_report(dialog))
        buttons_layout.addWidget(show_button)

        cancel_button = QPushButton("لغو")
        cancel_button.setStyleSheet("background-color: #e74c3c; color: white;")
        cancel_button.clicked.connect(dialog.close)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def generate_shift_report(self, dialog):
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")

        conn = create_connection()
        c = conn.cursor()

        # دریافت شیفت‌های روز انتخاب شده
        c.execute("""
            SELECT u.username, s.start_time, s.end_time 
            FROM shifts s
            JOIN users u ON s.user_id = u.id
            WHERE s.date = ? AND s.end_time IS NOT NULL
        """, (selected_date,))

        shifts = c.fetchall()
        conn.close()

        if not shifts:
            QMessageBox.information(self, "گزارش شیفت", "هیچ شیفتی در تاریخ انتخاب شده ثبت نشده است.")
            dialog.close()
            return

        # ایجاد پنجره نمایش گزارش
        report_dialog = QDialog(self)
        report_dialog.setWindowTitle(f"گزارش شیفت - تاریخ {selected_date}")
        report_dialog.setMinimumSize(600, 400)
        report_dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-family: 'B Nazanin';
                font-size: 11pt;
            }
            QTableWidget {
                font-family: 'B Nazanin';
                font-size: 10pt;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # عنوان گزارش
        title_label = QLabel(f"گزارش شیفت - تاریخ {selected_date}")
        title_label.setFont(QFont("B Nazanin", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # جدول گزارش
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["نام کاربر", "شروع شیفت", "پایان شیفت", "مدت زمان (ساعت)"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setRowCount(len(shifts))

        for row, shift in enumerate(shifts):
            username, start_time, end_time = shift

            start_dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_dt = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            duration = (end_dt - start_dt).total_seconds() / 3600  # ساعت

            table.setItem(row, 0, QTableWidgetItem(username))

            table.setItem(row, 1, QTableWidgetItem(start_dt.strftime("%H:%M")))
            table.item(row, 1).setTextAlignment(Qt.AlignCenter)

            table.setItem(row, 2, QTableWidgetItem(end_dt.strftime("%H:%M")))
            table.item(row, 2).setTextAlignment(Qt.AlignCenter)

            table.setItem(row, 3, QTableWidgetItem(f"{duration:.2f}"))
            table.item(row, 3).setTextAlignment(Qt.AlignCenter)

        layout.addWidget(table)

        report_dialog.setLayout(layout)
        dialog.close()
        report_dialog.exec_()