import pytest

pytestmark = pytest.mark.django_db
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from drfecommerce.product.models import (
    AttributeValue,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductType,
    ProductTypeAttribute,
)


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange

        # Act
        obj = category_factory(name="test_cat")

        # Assert
        assert obj.__str__() == "test_cat"

    def test_name_max_length(self, category_factory):
        name = "x" * 236
        obj = category_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, category_factory):
        slug = "x" * 256
        obj = category_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_name_unique_field(self, category_factory):
        category_factory(name="test_cat")
        with pytest.raises(IntegrityError):
            category_factory(name="test_cat")

    def test_slug_unique_field(self, category_factory):
        category_factory(slug="test_slug")
        with pytest.raises(IntegrityError):
            category_factory(slug="test_slug")

    def test_is_active_false_default(self, category_factory):
        obj = category_factory()
        assert obj.is_active is False

    def test_parent_category_on_delete_protect(self, category_factory):
        obj1 = category_factory()
        category_factory(parent=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_parent_field_null(self, category_factory):
        obj1 = category_factory()
        assert obj1.parent is None

    def test_return_category_active_only_true(self, category_factory):
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.is_active().count()
        assert qs == 1

    def test_return_category_active_only_false(self, category_factory):
        category_factory(is_active=False)
        category_factory(is_active=True)
        category_factory(is_active=True)
        qs = Category.objects.filter(is_active=False).count()
        assert qs == 1


class TestProductModel:
    def test_str_method(self, product_factory):
        obj = product_factory(name="test_product")
        assert obj.__str__() == "test_product"

    def test_name_max_length(self, product_factory):
        name = "x" * 236
        obj = product_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, product_factory):
        slug = "x" * 256
        obj = product_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_pid_max_length(self, product_factory):
        pid = "x" * 11
        obj = product_factory(pid=pid)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_is_digital_default_false(self, product_factory):
        obj = product_factory()
        assert obj.is_digital == False

    def test_fk_category_on_delete_protect(self, product_factory, category_factory):
        obj1 = category_factory()
        product_factory(category=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_fk_product_type_on_delete_protect(
        self, product_factory, product_type_factory
    ):
        obj1 = product_type_factory()
        product_factory(product_type=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_return_product_active_only_true(self, product_factory):
        product_factory(is_active=False)
        product_factory(is_active=True)
        qs = Product.objects.is_active().count()
        assert qs == 1

    def test_return_product_active_only_false(self, product_factory):
        product_factory(is_active=False)
        product_factory(is_active=True)
        product_factory(is_active=True)
        qs = Product.objects.filter(is_active=False).count()
        assert qs == 1


class TestProductLineModel:
    def test_duplicate_attribute_insert(
        self,
        product_line_factory,
        attribute_factory,
        attribute_value_factory,
        product_line_attribute_value_factory,
    ):
        obj1 = attribute_factory(name="shoe=color")
        obj2 = attribute_value_factory(attribute_value="red", attribute=obj1)
        obj3 = attribute_value_factory(attribute_value="blue", attribute=obj1)
        obj4 = product_line_factory()
        product_line_attribute_value_factory(attribute_value=obj2, product_line=obj4)
        with pytest.raises(ValidationError):
            product_line_attribute_value_factory(
                attribute_value=obj3, product_line=obj4
            )

    def test_str_method(self, product_line_factory):
        obj = product_line_factory(sku="12345")
        assert obj.__str__() == "12345"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()

    def test_field_decimal_places(self, product_line_factory):
        price = 1.001
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_field_price_max_digits(self, product_line_factory):
        price = 1000.00
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_field_sku_max_length(self, product_line_factory):
        sku = "x" * 11
        with pytest.raises(ValidationError):
            product_line_factory(sku=sku)

    def test_is_active_default_false(self, product_line_factory):
        obj = product_line_factory()
        assert obj.is_active is False

    def test_fk_category_on_delete_protect(self, product_line_factory, product_factory):
        obj1 = product_factory()
        product_line_factory(product=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_fk_product_type_on_delete_protect(
        self, product_line_factory, product_type_factory
    ):
        obj1 = product_type_factory()
        product_line_factory(product_type=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_return_product_line_active_only_true(self, product_line_factory):
        product_line_factory(is_active=False)
        product_line_factory(is_active=True)
        qs = ProductLine.objects.is_active().count()
        assert qs == 1

    def test_return_product_line_active_only_false(self, product_line_factory):
        product_line_factory(is_active=False)
        product_line_factory(is_active=True)
        product_line_factory(is_active=True)
        qs = ProductLine.objects.filter(is_active=False).count()
        assert qs == 1


class TestProductImageModel:
    def test_str_method(self, product_image_factory, product_line_factory):
        obj1 = product_line_factory(sku="12345")
        obj2 = product_image_factory(order=1, product_line=obj1)
        assert obj2.__str__() == "12345_img"

    def test_alternative_text_field_length(self, product_image_factory):
        alternative_text = "x" * 101
        with pytest.raises(ValidationError):
            product_image_factory(alternative_text=alternative_text)

    def test_duplicate_order_values(self, product_image_factory, product_line_factory):
        obj = product_line_factory()
        product_image_factory(order=1, product_line=obj)
        with pytest.raises(ValidationError):
            product_image_factory(order=1, product_line=obj).clean()


# class TestProductTypeModel:
#     def test_str_method(self, product_type_factory):
#         obj = product_type_factory(name="test_type")
#         assert obj.__str__() == "test_type"


class TestProductTypeModel:
    @pytest.fixture
    def product_type_factory(self, product_type_factory):
        counter = 0

        def factory_func(**kwargs):
            nonlocal counter
            if "name" not in kwargs:
                kwargs["name"] = f"test_product_type_name_{counter}"
                counter += 1
            return product_type_factory(**kwargs)

        return factory_func

    def test_str_method(self, product_type_factory):
        obj1 = product_type_factory()
        obj2 = product_type_factory(name="test_type")
        obj3 = product_type_factory()

        assert obj1.__str__() == "test_product_type_name_0"
        assert obj2.__str__() == "test_type"
        assert obj3.__str__() == "test_product_type_name_1"

    def test_name_field_max_length(self, product_type_factory):
        name = "x" * 101
        obj = product_type_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        obj = attribute_factory(name="test_attribute")
        assert obj.__str__() == "test_attribute"

    def test_name_field_max_length(self, attribute_factory):
        name = "x" * 101
        obj = attribute_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory, attribute_factory):
        obj_a = attribute_factory(name="test_attribute")
        obj_b = attribute_value_factory(attribute_value="test_value", attribute=obj_a)
        assert obj_b.__str__() == "test_attribute-test_value"

    def test_value_field_max_length(self, attribute_value_factory):
        attribute_value = "x" * 101
        obj = attribute_value_factory(attribute_value=attribute_value)
        with pytest.raises(ValidationError):
            obj.full_clean()
