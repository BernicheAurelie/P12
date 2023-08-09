# Generated by Django 4.2.2 on 2023-06-21 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("contracts", "0002_alter_contract_saler_contact_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="contract",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contract_id",
                to="contracts.contract",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="event",
            name="support_contact",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="support_id",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
