import datetime
import os
from coffee.src.core.extensions import db
from flask.views import MethodView
from . import models
from flask import request, jsonify, current_app, url_for


class VIndex(MethodView):

    def get(self):
        product_id = request.args.get("id", None)
        response_dict = dict()
        if not product_id:
            all_data = models.MProducts.query.all()
            for data in all_data:
                response_dict[data.get_id()] = {
                    "name": data.name,
                    "image_url": data.image_url,
                    "description": data.description,
                    "price": data.price,
                    "discount": data.discount,
                    "off_price": data.off_price
                }
        else:
            single_data = models.MProducts.query.filter_by(_id=product_id).first_or_404()
            response_dict[single_data.get_id()] = {
                "name": single_data.name,
                "image_url": single_data.image_url,
                "description": single_data.description,
                "price": single_data.price,
                "discount": single_data.discount,
                "off_price": single_data.off_price
            }

        return jsonify(response_dict)

    def post(self):
        massage = None
        info_data = request.get_json()
        image_file = request.files.get("image", None)
        filename = str(datetime.datetime.now()) + " - " + info_data["name"]
        name = info_data["name"]
        description = info_data["description"]
        price = info_data["price"]
        discount = info_data["discount"]
        off_price = info_data["off_price"]
        url = url_for("uploads.uploaded", filename=filename)

        if name is None or description is None or price is None or discount is None or off_price is None:
            return jsonify({"massage": "Info is not complete !", "code": 4})

        product = models.MProducts(name, url, description, price, off_price, discount)
        try:
            db.session.add(product)
            massage = "The Product is saved"
            code = 1
        except:
            massage = "The Product is not saved"
            code = 4

        return jsonify(dict(massage=massage, code=code))