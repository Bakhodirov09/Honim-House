import sqlalchemy
from main.database_set import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("full_name", sqlalchemy.String),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("lang", sqlalchemy.String),
    sqlalchemy.Column("phone_number", sqlalchemy.String),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger)
)

menu = sqlalchemy.Table(
    "menu",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("menu_name", sqlalchemy.String),
    sqlalchemy.Column("lang", sqlalchemy.String),
)

foods_menu = sqlalchemy.Table(
    "foods_menu",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("menu", sqlalchemy.String),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Integer),
    sqlalchemy.Column('is_have', sqlalchemy.Integer),
    sqlalchemy.Column("photo", sqlalchemy.String),
    sqlalchemy.Column("lang", sqlalchemy.String),
)

admins = sqlalchemy.Table(
    'admins',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('chat_id', sqlalchemy.BigInteger),
    sqlalchemy.Column('name', sqlalchemy.String)
)

curers = sqlalchemy.Table(
    "curers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("is_working", sqlalchemy.Boolean, nullable=True)
)

logo = sqlalchemy.Table(
    'logo',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('photo', sqlalchemy.String)
)

basket = sqlalchemy.Table(
    "basket",
    metadata,
    sqlalchemy.Column("product", sqlalchemy.String),
    sqlalchemy.Column("menu_name", sqlalchemy.String),
    sqlalchemy.Column("miqdor", sqlalchemy.Integer),
    sqlalchemy.Column("narx", sqlalchemy.BigInteger),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger)
)

locations = sqlalchemy.Table(
    "locations",
    metadata,
    sqlalchemy.Column("location_name", sqlalchemy.String),
    sqlalchemy.Column("latitude", sqlalchemy.String),
    sqlalchemy.Column("longitude", sqlalchemy.String),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger)
)

payments = sqlalchemy.Table(
    'payments',
    metadata,
    sqlalchemy.Column("payment_name", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.Boolean)
)

history_buys = sqlalchemy.Table(
    "history_buys",
    metadata,
    sqlalchemy.Column("number", sqlalchemy.BigInteger),
    sqlalchemy.Column("product", sqlalchemy.String),
    sqlalchemy.Column("miqdor", sqlalchemy.Integer),
    sqlalchemy.Column("price", sqlalchemy.Integer),
    sqlalchemy.Column("bought_at", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String),
    sqlalchemy.Column("payment_method", sqlalchemy.String),
    sqlalchemy.Column("payment_status", sqlalchemy.String),
    sqlalchemy.Column("go_or_order", sqlalchemy.String),
    sqlalchemy.Column("which_filial", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger)
)

curer_orders = sqlalchemy.Table(
    'curer_orders',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('number', sqlalchemy.BigInteger),
    sqlalchemy.Column('chat_id', sqlalchemy.BigInteger),
    sqlalchemy.Column('latitude', sqlalchemy.String),
    sqlalchemy.Column('longitude', sqlalchemy.String)
)

order_number = sqlalchemy.Table(
    'order_number',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('number', sqlalchemy.BigInteger),
    sqlalchemy.Column('chat_id', sqlalchemy.BigInteger),
)

about_we = sqlalchemy.Table(
    'about_we',
    metadata,
    sqlalchemy.Column('about_we', sqlalchemy.String),
    sqlalchemy.Column('lang', sqlalchemy.String)
)

socials = sqlalchemy.Table(
    'socials',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('social_name', sqlalchemy.String),
    sqlalchemy.Column('link', sqlalchemy.String),
)

card_model = sqlalchemy.Table(
    'card_model',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('card_number', sqlalchemy.String),
    sqlalchemy.Column('owner', sqlalchemy.String)
)
