import datetime
import os
from coffee.src.core.extensions import db
from flask.views import MethodView
from . import models
from flask import request, jsonify, current_app, url_for


class VIndex(MethodView):

    def get(self):
        db.create_all()
        product_id = request.args.get("id", None)
        response_list = list()
        if not product_id:
            all_data = models.MProducts.query.all()
            for data in all_data:
                response_list.append({
                    "id": data.get_id(),
                    "name": data.name,
                    "image_url": data.image_url,
                    "description": data.description,
                    "price": data.price,
                    "discount": data.discount,
                    "off_price": data.off_price
                })
        else:
            single_data = models.MProducts.query.filter_by(_id=product_id).first_or_404()
            response_list.append({
                "id": single_data.get_id(),
                "name": single_data.name,
                "image_url": single_data.image_url,
                "description": single_data.description,
                "price": single_data.price,
                "discount": single_data.discount,
                "off_price": single_data.off_price
            })

        return jsonify(response_list)

    def post(self):
        info_data = request.form
        image_file = request.files.get("image", None)
        filename = str(datetime.datetime.now()) + "-" + image_file.filename
        name = info_data["name"]
        description = info_data["description"]
        price = info_data["price"]
        discount = info_data["discount"]
        off_price = info_data["off_price"]
        url = "https://api-coffee-flask.herokuapp.com/uploads/" + filename

        if name is None or description is None or price is None or discount is None or off_price is None:
            return jsonify({"massage": "Info is not complete !", "code": 4})

        product = models.MProducts(name, url, description, price, off_price, discount)
        try:
            db.session.add(product)
            db.session.commit()
            image_file.save(os.path.join(current_app.config["UPLOADS_DIR"], filename))
            massage = "The Product is saved"
            code = 1
        except Exception as w:
            massage = "The Product is not saved :" + str(w)
            code = 4

        return jsonify(dict(massage=massage, code=code))

    def delete(self):
        item_id = request.get_json()["item_id"]
        product = models.MProducts.query.filter_by(_id=item_id).first()
        if product is not None:
            product.delete()
            db.session.commit()
            return jsonify(dict(massage="Item Deleted", code=1))
        else:
            return jsonify(dict(massage="This item is not exists", code=4))

