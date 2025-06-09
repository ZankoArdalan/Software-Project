import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget,
    QTableWidgetItem,QHeaderView,
    QGroupBox, QInputDialog
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from database_connection import create_connection


class SalesPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # عنوان صفحه
        title_label = QLabel("مدیریت فروش")
        title_label.setFont(QFont("B Nazanin", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # بخش جستجوی محصول
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        search_label = QLabel("جستجوی محصول:")
        search_label.setFont(QFont("B Nazanin", 12))

        self.product_search = QLineEdit()
        self.product_search.setPlaceholderText("نام محصول...")
        self.product_search.textChanged.connect(self.search_products)
        self.product_search.setFont(QFont("B Nazanin", 11))
        self.product_search.setMinimumHeight(40)
        self.product_search.setStyleSheet("""
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
        search_layout.addWidget(self.product_search)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        # جدول محصولات
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["ID", "نام محصول", "دسته‌بندی", "قیمت (تومان)", "موجودی"])
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
        self.products_table.cellDoubleClicked.connect(self.add_to_cart)

        main_layout.addWidget(self.products_table)

        # بخش سبد خرید
        cart_group = QGroupBox("سبد خرید")
        cart_group.setFont(QFont("B Nazanin", 12, QFont.Bold))
        cart_layout = QVBoxLayout()
        cart_layout.setSpacing(15)

        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["ID", "نام محصول", "قیمت واحد", "تعداد", "قیمت کل"])
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cart_table.verticalHeader().setVisible(False)
        self.cart_table.setFont(QFont("B Nazanin", 10))
        self.cart_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #dfe4ea;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.cart_table.setEditTriggers(QTableWidget.NoEditTriggers)

        cart_layout.addWidget(self.cart_table)

        # جمع کل
        self.total_label = QLabel("جمع کل: 0 تومان")
        self.total_label.setFont(QFont("B Nazanin", 14, QFont.Bold))
        self.total_label.setStyleSheet("color: #27ae60;")
        self.total_label.setAlignment(Qt.AlignRight)
        cart_layout.addWidget(self.total_label)

        # دکمه‌های سبد خرید
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.checkout_button = QPushButton("تکمیل فروش")
        self.checkout_button.setIcon(QIcon("checkout.png"))
        self.checkout_button.setFont(QFont("B Nazanin", 12))
        self.checkout_button.setMinimumHeight(45)
        self.checkout_button.setStyleSheet("background-color: #27ae60; color: white;")
        self.checkout_button.clicked.connect(self.complete_sale)
        buttons_layout.addWidget(self.checkout_button)

        clear_button = QPushButton("پاک کردن سبد")
        clear_button.setIcon(QIcon("clear.png"))
        clear_button.setFont(QFont("B Nazanin", 12))
        clear_button.setMinimumHeight(45)
        clear_button.setStyleSheet("background-color: #e74c3c; color: white;")
        clear_button.clicked.connect(self.clear_cart)
        buttons_layout.addWidget(clear_button)

        cart_layout.addLayout(buttons_layout)
        cart_group.setLayout(cart_layout)
        main_layout.addWidget(cart_group)

        self.cart = []  # لیست اقلام سبد خرید

        self.setLayout(main_layout)

    def load_products(self):
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT id, name, category, price, stock FROM products WHERE stock > 0")
        products = c.fetchall()
        conn.close()

        self.products_table.setRowCount(len(products))

        for row, product in enumerate(products):
            product_id, name, category, price, stock = product

            self.products_table.setItem(row, 0, QTableWidgetItem(str(product_id)))
            self.products_table.item(row, 0).setTextAlignment(Qt.AlignCenter)

            self.products_table.setItem(row, 1, QTableWidgetItem(name))

            self.products_table.setItem(row, 2, QTableWidgetItem(category))

            self.products_table.setItem(row, 3, QTableWidgetItem(f"{price:,.0f}"))
            self.products_table.item(row, 3).setTextAlignment(Qt.AlignCenter)

            self.products_table.setItem(row, 4, QTableWidgetItem(str(stock)))
            self.products_table.item(row, 4).setTextAlignment(Qt.AlignCenter)

    def search_products(self):
        search_text = self.product_search.text().strip()

        conn = create_connection()
        c = conn.cursor()

        if search_text:
            c.execute("SELECT id, name, category, price, stock FROM products WHERE name LIKE ? AND stock > 0",
                      (f"%{search_text}%",))
        else:
            c.execute("SELECT id, name, category, price, stock FROM products WHERE stock > 0")

        products = c.fetchall()
        conn.close()

        self.products_table.setRowCount(len(products))

        for row, product in enumerate(products):
            product_id, name, category, price, stock = product

            self.products_table.setItem(row, 0, QTableWidgetItem(str(product_id)))
            self.products_table.item(row, 0).setTextAlignment(Qt.AlignCenter)

            self.products_table.setItem(row, 1, QTableWidgetItem(name))

            self.products_table.setItem(row, 2, QTableWidgetItem(category))

            self.products_table.setItem(row, 3, QTableWidgetItem(f"{price:,.0f}"))
            self.products_table.item(row, 3).setTextAlignment(Qt.AlignCenter)

            self.products_table.setItem(row, 4, QTableWidgetItem(str(stock)))
            self.products_table.item(row, 4).setTextAlignment(Qt.AlignCenter)

    def add_to_cart(self, row):
        product_id = int(self.products_table.item(row, 0).text())
        product_name = self.products_table.item(row, 1).text()
        unit_price = float(self.products_table.item(row, 3).text().replace(",", ""))
        stock = int(self.products_table.item(row, 4).text())

        # دریافت تعداد
        quantity, ok = QInputDialog.getInt(self, "تعداد", f"تعداد '{product_name}' را وارد کنید:", 1, 1, stock)
        if not ok:
            return

        # بررسی وجود محصول در سبد
        for i, item in enumerate(self.cart):
            if item['id'] == product_id:
                # اگر تعداد درخواستی بیشتر از موجودی نباشد
                if item['quantity'] + quantity <= stock:
                    self.cart[i]['quantity'] += quantity
                    self.cart[i]['total_price'] = self.cart[i]['unit_price'] * self.cart[i]['quantity']
                    self.update_cart()
                else:
                    QMessageBox.warning(self, "خطا", "تعداد درخواستی بیشتر از موجودی است.")
                return

        # افزودن محصول جدید به سبد
        self.cart.append({
            'id': product_id,
            'name': product_name,
            'unit_price': unit_price,
            'quantity': quantity,
            'total_price': unit_price * quantity
        })

        self.update_cart()

    def update_cart(self):
        self.cart_table.setRowCount(len(self.cart))
        total = 0

        for row, item in enumerate(self.cart):
            self.cart_table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.cart_table.item(row, 0).setTextAlignment(Qt.AlignCenter)

            self.cart_table.setItem(row, 1, QTableWidgetItem(item['name']))

            self.cart_table.setItem(row, 2, QTableWidgetItem(f"{item['unit_price']:,.0f}"))
            self.cart_table.item(row, 2).setTextAlignment(Qt.AlignCenter)

            self.cart_table.setItem(row, 3, QTableWidgetItem(str(item['quantity'])))
            self.cart_table.item(row, 3).setTextAlignment(Qt.AlignCenter)

            self.cart_table.setItem(row, 4, QTableWidgetItem(f"{item['total_price']:,.0f}"))
            self.cart_table.item(row, 4).setTextAlignment(Qt.AlignCenter)

            total += item['total_price']

        self.total_label.setText(f"جمع کل: {total:,.0f} تومان")

    def clear_cart(self):
        self.cart = []
        self.update_cart()

    def complete_sale(self):
        if not self.cart:
            QMessageBox.warning(self, "خطا", "سبد خرید خالی است!")
            return

        # ثبت فروش در دیتابیس
        conn = create_connection()
        c = conn.cursor()
        sale_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for item in self.cart:
            # ثبت فروش
            c.execute(
                "INSERT INTO sales (product_id, quantity, total_price, sale_date, user_id) VALUES (?, ?, ?, ?, ?)",
                (item['id'], item['quantity'], item['total_price'], sale_date, self.parent.user_id))

            # کاهش موجودی
            c.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (item['quantity'], item['id']))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "موفقیت", "فروش با موفقیت ثبت شد.")
        self.clear_cart()
        self.load_products()