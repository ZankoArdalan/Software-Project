import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget,QLabel,QPushButton,
    QVBoxLayout, QMessageBox,
    QGroupBox, QFileDialog
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class BackupPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)

        # عنوان
        title_label = QLabel("پشتیبان‌گیری و بازیابی")
        title_label.setFont(QFont("B Nazanin", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # بخش پشتیبان‌گیری
        backup_group = QGroupBox("پشتیبان‌گیری از سیستم")
        backup_group.setFont(QFont("B Nazanin", 12, QFont.Bold))
        backup_layout = QVBoxLayout()
        backup_layout.setSpacing(20)
        backup_layout.setContentsMargins(20, 30, 20, 30)

        backup_label = QLabel("با استفاده از این بخش می‌توانید از تمامی اطلاعات سیستم نسخه پشتیبان تهیه کنید.")
        backup_label.setFont(QFont("B Nazanin", 11))
        backup_label.setWordWrap(True)
        backup_layout.addWidget(backup_label)

        backup_button = QPushButton("ایجاد نسخه پشتیبان")
        backup_button.setIcon(QIcon("backup.png"))
        backup_button.setFont(QFont("B Nazanin", 12))
        backup_button.setMinimumHeight(50)
        backup_button.setStyleSheet("background-color: #3498db; color: white;")
        backup_button.clicked.connect(self.create_backup)
        backup_layout.addWidget(backup_button, alignment=Qt.AlignCenter)

        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)

        # بخش بازیابی
        restore_group = QGroupBox("بازیابی از نسخه پشتیبان")
        restore_group.setFont(QFont("B Nazanin", 12, QFont.Bold))
        restore_layout = QVBoxLayout()
        restore_layout.setSpacing(20)
        restore_layout.setContentsMargins(20, 30, 20, 30)

        restore_label = QLabel(
            "توجه: بازیابی از نسخه پشتیبان، اطلاعات فعلی سیستم را با اطلاعات نسخه پشتیبان جایگزین می‌کند.")
        restore_label.setFont(QFont("B Nazanin", 11))
        restore_label.setWordWrap(True)
        restore_label.setStyleSheet("color: red;")
        restore_layout.addWidget(restore_label)

        restore_button = QPushButton("بازیابی از نسخه پشتیبان")
        restore_button.setIcon(QIcon("restore.png"))
        restore_button.setFont(QFont("B Nazanin", 12))
        restore_button.setMinimumHeight(50)
        restore_button.setStyleSheet("background-color: #e74c3c; color: white;")
        restore_button.clicked.connect(self.restore_backup)
        restore_layout.addWidget(restore_button, alignment=Qt.AlignCenter)

        restore_group.setLayout(restore_layout)
        layout.addWidget(restore_group)

        self.setLayout(layout)

    def create_backup(self):
        # انتخاب محل ذخیره پشتیبان
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "ذخیره نسخه پشتیبان", "", "Backup Files (*.db);;All Files (*)", options=options)

        if not file_path:
            return

        # اگر مسیر فایل پسوند نداشت، اضافه کردن
        if not file_path.endswith('.db'):
            file_path += '.db'

        try:
            # کپی فایل دیتابیس
            shutil.copyfile('clothing_store.db', file_path)
            QMessageBox.information(self, "موفقیت", f"نسخه پشتیبان با موفقیت در مسیر زیر ذخیره شد:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ایجاد نسخه پشتیبان:\n{str(e)}")

    def restore_backup(self):
        # تأییدیه از کاربر
        reply = QMessageBox.question(
            self, "هشدار",
            "آیا از بازیابی اطلاعات از نسخه پشتیبان مطمئن هستید؟\nتمامی اطلاعات فعلی سیستم با اطلاعات نسخه پشتیبان جایگزین خواهد شد.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # انتخاب فایل پشتیبان
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "انتخاب نسخه پشتیبان", "", "Backup Files (*.db);;All Files (*)", options=options)

        if not file_path:
            return

        try:
            # بستن اتصال فعلی به دیتابیس
            QApplication.processEvents()

            # جایگزینی دیتابیس فعلی با نسخه پشتیبان
            shutil.copyfile(file_path, 'clothing_store.db')

            QMessageBox.information(self, "موفقیت", "اطلاعات سیستم با موفقیت از نسخه پشتیبان بازیابی شد.")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بازیابی نسخه پشتیبان:\n{str(e)}")