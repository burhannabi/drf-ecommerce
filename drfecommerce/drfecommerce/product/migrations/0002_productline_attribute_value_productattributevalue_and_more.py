# Generated by Django 4.2.1 on 2023-06-08 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="productline",
            name="attribute_value",
            field=models.ManyToManyField(
                related_name="product_line_attribute_value",
                through="product.ProductLineAttributeValue",
                to="product.attributevalue",
            ),
        ),
        migrations.CreateModel(
            name="ProductAttributeValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attribute_value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_value_av",
                        to="product.attributevalue",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_value_pl",
                        to="product.product",
                    ),
                ),
            ],
            options={
                "unique_together": {("attribute_value", "product")},
            },
        ),
        migrations.AddField(
            model_name="product",
            name="attribute_value",
            field=models.ManyToManyField(
                related_name="product_attr_value",
                through="product.ProductAttributeValue",
                to="product.attributevalue",
            ),
        ),
    ]
