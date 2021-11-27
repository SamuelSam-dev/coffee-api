from coffee.src.core.extensions import db
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
class MProducts(db.Model):
    _id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(collation='utf8_bin'), nullable=False)
    image_url = db.Column(db.VARCHAR(), nullable=False)
    description = db.Column(db.Unicode(collation='utf8_bin'), nullable=False)
    price = db.Column(db.INTEGER(), nullable=False)
    discount = db.Column(db.INTEGER(), nullable=False, default=False)
    off_price = db.Column(db.INTEGER(), nullable=False, default=0)

    def __init__(self, name, url, description, price, off_price, discount):
        self.name = name
        self.image_url = url
        self. description = description
        self.price = price
        self.off_price = off_price
        self.discount = discount

    def get_id(self):
        return self._id
