from PyQt5.QtWidgets import (
    QWidget, QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout,QMessageBox, QTableWidget,
    QTableWidgetItem, QComboBox, QHeaderView, QFormLayout
)
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt

from database_connection import create_connection


class ProductPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # عنوان صفحه
        title_label = QLabel("مدیریت محصولات")
        title_label.setFont(QFont("B Nazanin", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # بخش جستجو
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        search_label = QLabel("جستجو:")
        search_label.setFont(QFont("B Nazanin", 12))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("نام محصول یا دسته‌بندی...")
        self.search_input.textChanged.connect(self.search_products)
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
        search_button.clicked.connect(self.search_products)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        # جدول محصولات
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(6)
        self.products_table.setHorizontalHeaderLabels(
            ["ID", "نام محصول", "دسته‌بندی", "قیمت (تومان)", "موجودی", "عملیات"])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.products_table.verticalHeader().setVisible(False)
        self.products_table.setFont(QFont("B Nazanin", 10))
        self.products_table.setStyleSheet("""
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
        self.products_table.setEditTriggers(QTableWidget.NoEditTriggers)

        main_layout.addWidget(self.products_table)

        # دکمه‌های مدیریت محصولات
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        add_button = QPushButton("افزودن محصول جدید")
        add_button.setIcon(QIcon("add.png"))
        add_button.setFont(QFont("B Nazanin", 12))
        add_button.setMinimumHeight(45)
        add_button.setStyleSheet("background-color: #27ae60; color: white;")
        add_button.clicked.connect(self.add_product)
        buttons_layout.addWidget(add_button)

        if self.parent.role in ['owner', 'admin']:
            edit_button = QPushButton("ویرایش محصول")
            edit_button.setIcon(QIcon("edit.png"))
            edit_button.setFont(QFont("B Nazanin", 12))
            edit_button.setMinimumHeight(45)
            edit_button.setStyleSheet("background-color: #f39c12; color: white;")
            edit_button.clicked.connect(self.edit_product)
            buttons_layout.addWidget(edit_button)

            delete_button = QPushButton("حذف محصول")
            delete_button.setIcon(QIcon("delete.png"))
            delete_button.setFont(QFont("B Nazanin", 12))
            delete_button.setMinimumHeight(45)
            delete_button.setStyleSheet("background-color: #e74c3c; color: white;")
            delete_button.clicked.connect(self.delete_product)
            buttons_layout.addWidget(delete_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def load_products(self):
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        conn.close()

        self.products_table.setRowCount(len(products))

        for row, product in enumerate(products):
            product_id, name, description, category, price, stock = product

            # نمایش اطلاعات محصول
            self.products_table.setItem(row, 0, QTableWidgetItem(str(product_id)))
            self.products_table.item(row, 0).setTextAlignment(Qt.AlignCenter)

            self.products_table.setItem(row, 1, QTableWidgetItem(name))

            self.products_table.setItem(row, 2, QTableWidgetItem(category))

            self.products_table.setItem(row, 3, QTableWidgetItem(f"{price:,.0f}"))
            self.products_table.item(row, 3).setTextAlignment(Qt.AlignCenter)

            self.products_table.setItem(row, 4, QTableWidgetItem(str(stock)))
            self.products_table.item(row, 4).setTextAlignment(Qt.AlignCenter)

            # دکمه جزئیات
            details_button = QPushButton("جزئیات")
            details_button.setFont(QFont("B Nazanin", 10))
            details_button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                    min-width: 80px;
                }
            """)
            details_button.clicked.connect(lambda _, p=product: self.show_product_details(p))
            self.products_table.setCellWidget(row, 5, details_button)

    def search_products(self):
        search_text = self.search_input.text().strip()

        conn = create_connection()
        c = conn.cursor()

        if search_text:
            c.execute("SELECT * FROM products WHERE name LIKE ? OR category LIKE ?",
                      (f"%{search_text}%", f"%{search_text}%"))
        else:
            c.execute("SELECT * FROM products")

        products = c.fetchall()
        conn.close()

        self.products_table.setRowCount(len(products))

        for row, product in enumerate(products):
            product_id, name, description, category, price, stock = product

            self.products_table.setItem(row, 0, QTableWidgetItem(str(product_id)))
            self.products_table.item(row, 0).setTextAlignment(Qt.AlignCenter)

            self.products_table.setItem(row, 1, QTableWidgetItem(name))

            self.products_table.setItem(row, 2, QTableWidgetItem(category))

            self.products_table.setItem(row, 3, QTableWidgetItem(f"{price:,.0f}"))
            self.products_table.item(row, 3).setTextAlignment(Qt.AlignCenter)

            self.products_table.setItem(row, 4, QTableWidgetItem(str(stock)))
            self.products_table.item(row, 4).setTextAlignment(Qt.AlignCenter)

            details_button = QPushButton("جزئیات")
            details_button.setFont(QFont("B Nazanin", 10))
            details_button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                    min-width: 80px;
                }
            """)
            details_button.clicked.connect(lambda _, p=product: self.show_product_details(p))
            self.products_table.setCellWidget(row, 5, details_button)

    def show_product_details(self, product):
        product_id, name, description, category, price, stock = product

        details_dialog = QDialog(self)
        details_dialog.setWindowTitle(f"جزئیات محصول: {name}")
        details_dialog.setFixedSize(400, 300)
        details_dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
            QLabel {
                font-family: 'B Nazanin';
                font-size: 12pt;
                padding: 5px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # نمایش اطلاعات محصول
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)

        info_layout.addWidget(QLabel(f"<b>نام محصول:</b> {name}"))
        info_layout.addWidget(QLabel(f"<b>دسته‌بندی:</b> {category}"))
        info_layout.addWidget(QLabel(f"<b>قیمت:</b> {price:,.0f} تومان"))
        info_layout.addWidget(QLabel(f"<b>موجودی:</b> {stock} عدد"))
        info_layout.addWidget(QLabel(f"<b>توضیحات:</b> {description}"))

        layout.addLayout(info_layout)

        # دکمه بستن
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        close_button = QPushButton("بستن")
        close_button.setFont(QFont("B Nazanin", 11))
        close_button.setMinimumHeight(40)
        close_button.setStyleSheet("background-color: #e74c3c; color: white;")
        close_button.clicked.connect(details_dialog.close)
        buttons_layout.addWidget(close_button)

        layout.addLayout(buttons_layout)

        details_dialog.setLayout(layout)
        details_dialog.exec_()

    def add_product(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("افزودن محصول جدید")
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
        title_label = QLabel("افزودن محصول جدید")
        title_label.setFont(QFont("B Nazanin", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # فیلدهای فرم
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # نام محصول
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("نام محصول را وارد کنید")
        form_layout.addRow("نام محصول:", self.name_input)

        # دسته‌بندی
        self.category_input = QComboBox()
        self.category_input.addItems(["لباس مردانه", "لباس زنانه", "لباس بچگانه", "اکسسوری"])
        form_layout.addRow("دسته‌بندی:", self.category_input)

        # قیمت
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("قیمت به تومان")
        self.price_input.setValidator(QDoubleValidator(0, 999999999, 0))
        form_layout.addRow("قیمت (تومان):", self.price_input)

        # موجودی
        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("تعداد موجودی")
        self.stock_input.setValidator(QIntValidator(0, 999999))
        form_layout.addRow("موجودی:", self.stock_input)

        # توضیحات
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("توضیحات محصول")
        form_layout.addRow("توضیحات:", self.description_input)

        layout.addLayout(form_layout)

        # دکمه‌های فرم
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        save_button = QPushButton("ذخیره محصول")
        save_button.setFont(QFont("B Nazanin", 12))
        save_button.setMinimumHeight(45)
        save_button.setStyleSheet("background-color: #27ae60; color: white;")
        save_button.clicked.connect(lambda: self.save_product(dialog))
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

    def save_product(self, dialog):
        name = self.name_input.text().strip()
        category = self.category_input.currentText()
        price = self.price_input.text().strip()
        stock = self.stock_input.text().strip()
        description = self.description_input.text().strip()

        if not name or not price or not stock:
            QMessageBox.warning(self, "خطا", "پر کردن فیلدهای نام، قیمت و موجودی الزامی است.")
            return

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            QMessageBox.warning(self, "خطا", "قیمت و موجودی باید عددی باشند.")
            return

        conn = create_connection()
        c = conn.cursor()
        c.execute("INSERT INTO products (name, description, category, price, stock) VALUES (?, ?, ?, ?, ?)",
                  (name, description, category, price, stock))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "موفقیت", "محصول جدید با موفقیت اضافه شد.")
        dialog.close()
        self.load_products()

    def edit_product(self):
        selected_row = self.products_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطا", "لطفاً یک محصول را انتخاب کنید.")
            return

        product_id = int(self.products_table.item(selected_row, 0).text())

        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE id=?", (product_id,))
        product = c.fetchone()
        conn.close()

        if not product:
            QMessageBox.warning(self, "خطا", "محصول انتخاب شده یافت نشد.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"ویرایش محصول: {product[1]}")
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
        title_label = QLabel(f"ویرایش محصول: {product[1]}")
        title_label.setFont(QFont("B Nazanin", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # فیلدهای فرم با اطلاعات فعلی
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # نام محصول
        self.name_input = QLineEdit(product[1])
        form_layout.addRow("نام محصول:", self.name_input)

        # دسته‌بندی
        self.category_input = QComboBox()
        categories = ["لباس مردانه", "لباس زنانه", "لباس بچگانه", "اکسسوری"]
        self.category_input.addItems(categories)
        self.category_input.setCurrentText(product[3])
        form_layout.addRow("دسته‌بندی:", self.category_input)

        # قیمت
        self.price_input = QLineEdit(str(product[4]))
        self.price_input.setValidator(QDoubleValidator(0, 999999999, 0))
        form_layout.addRow("قیمت (تومان):", self.price_input)

        # موجودی
        self.stock_input = QLineEdit(str(product[5]))
        self.stock_input.setValidator(QIntValidator(0, 999999))
        form_layout.addRow("موجودی:", self.stock_input)

        # توضیحات
        self.description_input = QLineEdit(product[2])
        form_layout.addRow("توضیحات:", self.description_input)

        layout.addLayout(form_layout)

        # دکمه‌های فرم
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        save_button = QPushButton("ذخیره تغییرات")
        save_button.setFont(QFont("B Nazanin", 12))
        save_button.setMinimumHeight(45)
        save_button.setStyleSheet("background-color: #27ae60; color: white;")
        save_button.clicked.connect(lambda: self.update_product(product_id, dialog))
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

    def update_product(self, product_id, dialog):
        name = self.name_input.text().strip()
        category = self.category_input.currentText()
        price = self.price_input.text().strip()
        stock = self.stock_input.text().strip()
        description = self.description_input.text().strip()

        if not name or not price or not stock:
            QMessageBox.warning(self, "خطا", "پر کردن فیلدهای نام، قیمت و موجودی الزامی است.")
            return

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            QMessageBox.warning(self, "خطا", "قیمت و موجودی باید عددی باشند.")
            return

        conn = create_connection()
        c = conn.cursor()
        c.execute("UPDATE products SET name=?, description=?, category=?, price=?, stock=? WHERE id=?",
                  (name, description, category, price, stock, product_id))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "موفقیت", "تغییرات محصول با موفقیت ذخیره شد.")
        dialog.close()
        self.load_products()

    def delete_product(self):
        selected_row = self.products_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطا", "لطفاً یک محصول را انتخاب کنید.")
            return

        product_id = int(self.products_table.item(selected_row, 0).text())
        product_name = self.products_table.item(selected_row, 1).text()

        reply = QMessageBox.question(self, "تأیید حذف",
                                     f"آیا از حذف محصول '{product_name}' مطمئن هستید؟",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            conn = create_connection()
            c = conn.cursor()
            c.execute("DELETE FROM products WHERE id=?", (product_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "موفقیت", "محصول با موفقیت حذف شد.")
            self.load_products()