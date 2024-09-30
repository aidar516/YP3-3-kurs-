import csv
from io import StringIO
import codecs
from flask import Response
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from models import *
from flask_admin import Admin

admin = Admin(name='Книжный магазин', template_mode='bootstrap3')


class RoleView(ModelView):
    column_list = ('role_id', 'role_name', 'is_deleted')
    column_labels = {
        'role_id': 'ID Роли',
        'role_name': 'Название роли'
    }
    form_columns = ["role_name", 'is_deleted']
    column_sortable_list = ['role_id', 'role_name']
    column_filters = ['role_id', 'role_name']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~Role.is_deleted)
        roles = query.all()

        # Write rows
        for role in roles:
            row = []
            for column in self.column_list:
                value = getattr(role, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=roles.csv"}
        )
        return response


class PublisherView(ModelView):
    column_list = ('publisher_id', 'publisher_name', 'address', 'phone', 'website', 'is_deleted')
    column_labels = {
        'publisher_id': 'ID Издательства',
        'publisher_name': 'Название издательства',
        'address': 'Адрес издательства',
        'phone': 'Номер телефона',
        'website': 'Сайт издательства'
    }
    form_columns = ["publisher_name", "address", "phone", "website", 'is_deleted']
    column_sortable_list = ['publisher_id', 'publisher_name', 'address', 'phone', 'website']
    column_filters = ['publisher_id', 'publisher_name', 'address', 'phone', 'website']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~Publisher.is_deleted)
        publishers = query.all()

        # Write rows
        for publisher in publishers:
            row = []
            for column in self.column_list:
                value = getattr(publisher, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=publishers.csv"}
        )
        return response


class GenreView(ModelView):
    column_list = ('genre_id', 'genre_name', 'description', 'is_deleted')
    column_labels = {
        'genre_id': 'ID Жанра',
        'genre_name': 'Название жанра',
        'description': 'Описание'
    }
    form_columns = ["genre_name", "description", 'is_deleted']
    column_sortable_list = ['genre_id', 'genre_name']
    column_filters = ['genre_id', 'genre_name']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~Genre.is_deleted)
        genres = query.all()

        # Write rows
        for genre in genres:
            row = []
            for column in self.column_list:
                value = getattr(genre, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=genres.csv"}
        )
        return response


class AuthorView(ModelView):
    column_list = ('author_id', 'author_name', 'author_surname', 'biography', 'is_deleted')
    column_labels = {
        'author_id': 'ID Автора',
        'author_name': 'Имя автора',
        'author_surname': 'Фамилия автора',
        'biography': 'Биография'
    }
    form_columns = ["author_name", "author_surname", "biography", 'is_deleted']
    column_sortable_list = ['author_id', 'author_name', 'author_surname']
    column_filters = ['author_id', 'author_name', 'author_surname']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~Author.is_deleted)
        authors = query.all()

        # Write rows
        for author in authors:
            row = []
            for column in self.column_list:
                value = getattr(author, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=authors.csv"}
        )
        return response


class WarehouseView(ModelView):
    column_list = ('warehouse_id', 'warehouse_name', 'phone', 'is_deleted')
    column_labels = {
        'warehouse_id': 'ID Склада',
        'warehouse_name': 'Название склада',
        'phone': 'Номер телефона'
    }
    form_columns = ["warehouse_name", "phone", 'is_deleted']
    column_sortable_list = ['warehouse_id', 'warehouse_name', 'phone']
    column_filters = ['warehouse_id', 'warehouse_name', 'phone']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~Warehouse.is_deleted)
        warehouses = query.all()

        # Write rows
        for warehouse in warehouses:
            row = []
            for column in self.column_list:
                value = getattr(warehouse, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=warehouses.csv"}
        )
        return response


class SupplierView(ModelView):
    column_list = ('supplier_id', 'supplier_name', 'address', 'phone', 'is_deleted')
    column_labels = {
        'supplier_id': 'ID Поставщика',
        'supplier_name': 'Название поставщика',
        'address': 'Адрес поставщика',
        'phone': 'Номер телефона'
    }
    form_columns = ["supplier_name", "address", "phone", 'is_deleted']
    column_sortable_list = ['supplier_id', 'supplier_name', 'address', 'phone']
    column_filters = ['supplier_id', 'supplier_name', 'address', 'phone']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~Supplier.is_deleted)
        suppliers = query.all()

        # Write rows
        for supplier in suppliers:
            row = []
            for column in self.column_list:
                value = getattr(supplier, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=suppliers.csv"}
        )
        return response


class UserView(ModelView):
    column_list = ('user_id', 'first_name', 'last_name', 'email', 'role', 'password_hash', 'token', 'is_deleted')
    column_labels = {
        'user_id': 'ID Пользователя',
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'email': 'Электронная почта',
        'role': 'Роль',
        'password_hash': 'Хэш пароля',
        'token': 'Токен'
    }
    form_columns = ["first_name", "last_name", "email", "password_hash", "token", "role", 'is_deleted']
    column_sortable_list = ['user_id', 'first_name', 'last_name', 'email', 'role']
    column_filters = ['user_id', 'first_name', 'last_name', 'email', 'role']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~User.is_deleted)
        users = query.all()

        # Write rows
        for user in users:
            row = []
            for column in self.column_list:
                value = getattr(user, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=users.csv"}
        )
        return response


class BookView(ModelView):
    column_list = ('book_id', 'book_name', 'author', 'genre', 'publisher', 'price', 'year', 'description', 'image', 'is_deleted')
    column_labels = {
        'book_id': 'ID Книги',
        'book_name': 'Название книги',
        'author': 'Автор',
        'genre': 'Жанр',
        'publisher': 'Издательство',
        'price': 'Цена',
        'year': 'Год издания',
        'description': 'Описание',
        'image': 'Изображение'
    }
    form_columns = ["book_name", "author", "genre", "publisher", "price", "year", "description", "image", 'is_deleted']
    column_sortable_list = ['book_id', 'book_name', 'author', 'genre', 'publisher', 'price', 'year']
    column_filters = ['book_id', 'book_name', 'author', 'genre', 'publisher', 'price', 'year']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~Book.is_deleted)
        books = query.all()

        # Write rows
        for book in books:
            row = []
            for column in self.column_list:
                value = getattr(book, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=books.csv"}
        )
        return response


class TransactionView(ModelView):
    column_list = ('transaction_id', 'order_id', 'transaction_date', 'transaction_amount', 'transaction_type', 'is_deleted')
    column_labels = {
        'transaction_id': 'ID Транзакции',
        'order_id': 'ID Заказа',
        'transaction_date': 'Дата транзакции',
        'transaction_amount': 'Сумма транзакции',
        'transaction_type': 'Тип транзакции'
    }
    form_columns = ["order_id", "transaction_date", "transaction_amount", "transaction_type", 'is_deleted']
    column_sortable_list = ['transaction_id', 'order_id', 'transaction_date', 'transaction_amount', 'transaction_type']
    column_filters = ['transaction_id', 'order_id', 'transaction_date', 'transaction_amount', 'transaction_type']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~Transaction.is_deleted)
        transactions = query.all()

        # Write rows
        for transaction in transactions:
            row = []
            for column in self.column_list:
                value = getattr(transaction, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=transactions.csv"}
        )
        return response


class BookWarehouseView(ModelView):
    column_list = ('book_warehouse_id', 'warehouse', 'book', 'book_amount', 'is_deleted')
    column_labels = {
        'book_warehouse_id': 'ID Книги на складе',
        'warehouse': 'Склад',
        'book': 'Книга',
        'book_amount': 'Количество книг'
    }
    form_columns = ["warehouse", "book", "book_amount", 'is_deleted']
    column_sortable_list = ['book_warehouse_id', 'warehouse', 'book', 'book_amount']
    column_filters = ['book_warehouse_id', 'warehouse', 'book', 'book_amount']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~BookWarehouse.is_deleted)
        book_warehouses = query.all()

        # Write rows
        for book_warehouse in book_warehouses:
            row = []
            for column in self.column_list:
                value = getattr(book_warehouse, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=book_warehouses.csv"}
        )
        return response


class DeliveryView(ModelView):
    column_list = ('delivery_id', 'supplier', 'warehouse', 'book', 'book_amount', 'delivery_date', 'is_deleted')
    column_labels = {
        'delivery_id': 'ID Поставки',
        'supplier': 'Поставщик',
        'warehouse': 'Склад',
        'book': 'Книга',
        'book_amount': 'Количество книг',
        'delivery_date': 'Дата поставки'
    }
    form_columns = ["supplier", "warehouse", "book", "book_amount", 'is_deleted']
    column_sortable_list = ['delivery_id', 'supplier', 'warehouse', 'book', 'book_amount', 'delivery_date']
    column_filters = ['delivery_id', 'supplier', 'warehouse', 'book', 'book_amount', 'delivery_date']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~Delivery.is_deleted)
        deliveries = query.all()

        # Write rows
        for delivery in deliveries:
            row = []
            for column in self.column_list:
                value = getattr(delivery, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=deliveries.csv"}
        )
        return response


class OrderDetailView(ModelView):
    column_list = ('order_detail_id', 'order', 'book', 'book_amount', 'unit_price', 'is_deleted')
    column_labels = {
        'order_detail_id': 'ID Детали заказа',
        'order': 'Заказ',
        'book': 'Книга',
        'book_amount': 'Количество книг',
        'unit_price': 'Цена за единицу'
    }
    form_columns = ["order", "book", "book_amount", 'unit_price', 'is_deleted']
    column_sortable_list = ['order_detail_id', 'order', 'book', 'book_amount', 'unit_price']
    column_filters = ['order_detail_id', 'order', 'book', 'book_amount', 'unit_price']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~OrderDetail.is_deleted)
        order_details = query.all()

        # Write rows
        for order_detail in order_details:
            row = []
            for column in self.column_list:
                value = getattr(order_detail, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=order_details.csv"}
        )
        return response


class OrderView(ModelView):
    column_list = ('order_id', 'user', 'order_date', 'status', 'total_price', 'is_deleted')
    column_labels = {
        'order_id': 'ID Заказа',
        'user': 'Пользователь',
        'order_date': 'Дата заказа',
        'status': 'Статус',
        'total_price': 'Общая цена'
    }
    form_columns = ["user", "order_date", "status", "total_price", 'is_deleted']
    column_sortable_list = ['order_id', 'user', 'order_date', 'status', 'total_price']
    column_filters = ['order_id', 'user', 'order_date', 'status', 'total_price']
    can_set_page_size = True
    page_size = 10

    @action('export_csv', 'Экспорт CSV', 'Вы уверены, что хотите экспортировать данные в CSV?')
    def export_csv(self, ids):
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=';', quotechar='"', lineterminator='\n')

        # Write headers
        headers = [self.column_labels.get(column, column) for column in self.column_list]
        writer.writerow([header for header in headers])

        # Query data
        query = self.get_query().filter(~Order.is_deleted)
        orders = query.all()

        # Write rows
        for order in orders:
            row = []
            for column in self.column_list:
                value = getattr(order, column)
                if isinstance(value, bool):
                    value = 'Да' if value else 'Нет'
                if value is None:
                    value = ''
                row.append(str(value))
            writer.writerow([item for item in row])

        # Reset the buffer position and return the response
        output.seek(0)
        response = Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=orders.csv"}
        )
        return response




admin.add_view(RoleView(Role, db.session, name="Роли"))
admin.add_view(SupplierView(Supplier, db.session, name="Поставщики"))
admin.add_view(UserView(User, db.session, name="Пользователи"))
admin.add_view(BookView(Book, db.session, name="Книги"))
admin.add_view(BookWarehouseView(BookWarehouse, db.session, name="Книги на складе"))
admin.add_view(WarehouseView(Warehouse, db.session, name="Склады"))
admin.add_view(PublisherView(Publisher, db.session, name="Издательства"))
admin.add_view(GenreView(Genre, db.session, name="Жанры"))
admin.add_view(OrderView(Order, db.session, name="Заказы"))
admin.add_view(OrderDetailView(OrderDetail, db.session, name="Детали заказов"))
admin.add_view(TransactionView(Transaction, db.session, name="Транзакции"))
admin.add_view(AuthorView(Author, db.session, name="Авторы"))
admin.add_view(DeliveryView(Delivery, db.session, name="Поставки"))