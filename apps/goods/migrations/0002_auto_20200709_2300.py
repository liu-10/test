# Generated by Django 3.0.4 on 2020-07-09 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailygoodssku',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '上线'), (0, '下线')], default=1, verbose_name='是否上线'),
        ),
        migrations.AlterField(
            model_name='goodsbanner',
            name='daily_sku',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.DailyGoodsSKU', verbose_name='日常商品SKU'),
        ),
        migrations.AlterField(
            model_name='goodsbanner',
            name='order_sku',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.OrderGoodsSKU', verbose_name='预定商品SKU'),
        ),
        migrations.AlterField(
            model_name='ordergoodssku',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '上线'), (0, '下线')], default=1, verbose_name='是否上线'),
        ),
    ]
