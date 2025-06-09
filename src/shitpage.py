import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from database_connection import create_connection


class ShiftPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # عنوان صفحه
        title_label = QLabel("مدیریت شیفت")
        title_label.setFont(QFont("B Nazanin", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # وضعیت شیفت فعلی
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        status_layout = QVBoxLayout(status_frame)

        self.shift_status_label = QLabel("وضعیت شیفت: نامشخص")
        self.shift_status_label.setFont(QFont("B Nazanin", 14))
        self.shift_status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.shift_status_label)

        layout.addWidget(status_frame)

        # دکمه‌های شروع و پایان شیفت
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(50, 20, 50, 20)

        self.start_shift_button = QPushButton("شروع شیفت")
        self.start_shift_button.setIcon(QIcon("start_shift.png"))
        self.start_shift_button.setFont(QFont("B Nazanin", 12))
        self.start_shift_button.setMinimumHeight(50)
        self.start_shift_button.setStyleSheet("background-color: #2ecc71; color: white;")
        self.start_shift_button.clicked.connect(self.start_shift)
        buttons_layout.addWidget(self.start_shift_button)

        self.end_shift_button = QPushButton("پایان شیفت")
        self.end_shift_button.setIcon(QIcon("end_shift.png"))
        self.end_shift_button.setFont(QFont("B Nazanin", 12))
        self.end_shift_button.setMinimumHeight(50)
        self.end_shift_button.setStyleSheet("background-color: #e74c3c; color: white;")
        self.end_shift_button.clicked.connect(self.end_shift)
        self.end_shift_button.setEnabled(False)
        buttons_layout.addWidget(self.end_shift_button)

        layout.addLayout(buttons_layout)

        # تاریخچه شیفت‌ها
        history_label = QLabel("تاریخچه شیفت‌های اخیر")
        history_label.setFont(QFont("B Nazanin", 14, QFont.Bold))
        history_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(history_label)

        self.shifts_table = QTableWidget()
        self.shifts_table.setColumnCount(4)
        self.shifts_table.setHorizontalHeaderLabels(["تاریخ", "شروع", "پایان", "مدت زمان (ساعت)"])
        self.shifts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.shifts_table.verticalHeader().setVisible(False)
        self.shifts_table.setFont(QFont("B Nazanin", 10))
        self.shifts_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #dfe4ea;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #9b59b6;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.shifts_table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.shifts_table)

        self.setLayout(layout)

    def load_shifts(self):
        # بررسی وضعیت شیفت فعلی
        conn = create_connection()
        c = conn.cursor()

        # بررسی شیفت فعال
        c.execute("""
        SELECT id, start_time, date 
        FROM shifts 
        WHERE user_id=? AND end_time IS NULL
        """, (self.parent.user_id,))
        active_shift = c.fetchone()

        if active_shift:
            shift_id, start_time, date = active_shift
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            start_str = start_time.strftime("%H:%M")

            self.shift_status_label.setText(f"شیفت فعال در تاریخ {date} شروع شده: {start_str}")
            self.start_shift_button.setEnabled(False)
            self.end_shift_button.setEnabled(True)
        else:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            self.shift_status_label.setText(f"وضعیت شیفت: بدون شیفت فعال")
            self.start_shift_button.setEnabled(True)
            self.end_shift_button.setEnabled(False)

        # بارگیری تاریخچه شیفت‌ها
        c.execute("""
        SELECT date, start_time, end_time 
        FROM shifts 
        WHERE user_id=? AND end_time IS NOT NULL
        ORDER BY date DESC, start_time DESC
        LIMIT 10
        """, (self.parent.user_id,))
        shifts = c.fetchall()
        conn.close()

        self.shifts_table.setRowCount(len(shifts))

        for row, shift in enumerate(shifts):
            date, start_time, end_time = shift

            start_dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_dt = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            duration = (end_dt - start_dt).total_seconds() / 3600  # ساعت

            self.shifts_table.setItem(row, 0, QTableWidgetItem(date))
            self.shifts_table.item(row, 0).setTextAlignment(Qt.AlignCenter)

            self.shifts_table.setItem(row, 1, QTableWidgetItem(start_dt.strftime("%H:%M")))
            self.shifts_table.item(row, 1).setTextAlignment(Qt.AlignCenter)

            self.shifts_table.setItem(row, 2, QTableWidgetItem(end_dt.strftime("%H:%M")))
            self.shifts_table.item(row, 2).setTextAlignment(Qt.AlignCenter)

            self.shifts_table.setItem(row, 3, QTableWidgetItem(f"{duration:.2f}"))
            self.shifts_table.item(row, 3).setTextAlignment(Qt.AlignCenter)

    def start_shift(self):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        start_time = now.strftime("%Y-%m-%d %H:%M:%S")

        conn = create_connection()
        c = conn.cursor()

        # بررسی وجود شیفت فعال در همان روز
        c.execute("""
        SELECT id 
        FROM shifts 
        WHERE user_id=? AND date=? AND end_time IS NULL
        """, (self.parent.user_id, date))
        existing_shift = c.fetchone()

        if existing_shift:
            QMessageBox.warning(self, "خطا", "شما در حال حاضر یک شیفت فعال دارید.")
            conn.close()
            return

        # ثبت شیفت جدید
        c.execute("""
        INSERT INTO shifts (user_id, start_time, date)
        VALUES (?, ?, ?)
        """, (self.parent.user_id, start_time, date))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "شروع شیفت", "شیفت شما با موفقیت شروع شد.")
        self.load_shifts()

    def end_shift(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = create_connection()
        c = conn.cursor()

        # یافتن شیفت فعال
        c.execute("""
        SELECT id, start_time 
        FROM shifts 
        WHERE user_id=? AND end_time IS NULL
        """, (self.parent.user_id,))
        active_shift = c.fetchone()

        if not active_shift:
            QMessageBox.warning(self, "خطا", "هیچ شیفت فعالی برای پایان دادن یافت نشد.")
            conn.close()
            return

        shift_id, start_time = active_shift

        # پایان دادن به شیفت
        c.execute("""
        UPDATE shifts 
        SET end_time=?
        WHERE id=?
        """, (now, shift_id))

        conn.commit()
        conn.close()

        # محاسبه مدت زمان شیفت
        start_dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
        duration = (end_dt - start_dt).total_seconds() / 3600

        QMessageBox.information(
            self, "پایان شیفت",
            f"شیفت شما با موفقیت پایان یافت.\nمدت زمان شیفت: {duration:.2f} ساعت"
        )
        self.load_shifts()