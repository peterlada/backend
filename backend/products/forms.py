# -*- coding: utf-8 -*-
"""
    backend.products.forms
    ~~~~~~~~~~~~~~~~~~~~~~~

    Product forms
"""

from flask.ext.wtf import Form
from wtforms import TextField, SelectMultipleField
from wtforms.validators import Required, Optional

from ..services import products

__all__ = ['NewProductForm', 'UpdateProductForm']


class ProductFormMixin(object):

    def __init__(self, *args, **kwargs):
        super(ProductFormMixin, self).__init__(*args, **kwargs)
        self.categories.choices = [(c.id, c.name) for c in products.categories.all()]


class NewProductForm(ProductFormMixin, Form):
    name = TextField('Name', validators=[Required()])
    categories = SelectMultipleField(
        'Categories', coerce=int, validators=[Required()])


class UpdateProductForm(ProductFormMixin, Form):
    name = TextField('Name', validators=[Optional()])
    categories = SelectMultipleField(
        'Categories', coerce=int, validators=[Optional()])
