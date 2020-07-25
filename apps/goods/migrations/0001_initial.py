# Generated by Django 3.0.4 on 2020-07-06 13:26

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyGoodsSKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价钱')),
                ('desc', models.CharField(max_length=128, verbose_name='商品描述')),
                ('unit', models.CharField(max_length=10, verbose_name='单位')),
                ('address', models.CharField(max_length=128, verbose_name='商家地址')),
                ('image', models.ImageField(blank=True, upload_to='dailygoods', verbose_name='商品图片')),
                ('stock', models.IntegerField(default=1, verbose_name='商品库存')),
                ('sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('status', models.SmallIntegerField(choices=[('1', '上线'), ('0', '下线')], default=1, verbose_name='是否上线')),
            ],
            options={
                'verbose_name': '日常商品',
                'verbose_name_plural': '日常商品',
                'db_table': 'qb_daily_goods',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=20, verbose_name='商品SPU名称')),
                ('detail', tinymce.models.HTMLField(max_length=256, verbose_name='商品SPU描述详情')),
            ],
            options={
                'verbose_name': '商品总描述',
                'verbose_name_plural': '商品总描述',
                'db_table': 'qb_goods',
            },
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('type', models.CharField(max_length=20, verbose_name='商品分类总名称')),
                ('logo', models.CharField(max_length=120, verbose_name='标识')),
                ('image', models.ImageField(blank=True, upload_to='type', verbose_name='商品图片')),
            ],
            options={
                'verbose_name': '分类商品列表',
                'verbose_name_plural': '分类商品列表',
                'db_table': 'qb_goods_type',
            },
        ),
        migrations.CreateModel(
            name='OrderGoodsSKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价钱')),
                ('desc', models.CharField(max_length=128, verbose_name='商品描述')),
                ('address', models.CharField(max_length=128, verbose_name='地址')),
                ('unit', models.CharField(max_length=10, verbose_name='单位')),
                ('image', models.ImageField(blank=True, upload_to='dailygoods', verbose_name='商品图片')),
                ('stock', models.IntegerField(default=1, verbose_name='商品库存')),
                ('sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('status', models.SmallIntegerField(choices=[('1', '上线'), ('0', '下线')], default=1, verbose_name='是否上线')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='所属SPU')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsType', verbose_name='所属类别')),
            ],
            options={
                'verbose_name': '预定商品',
                'verbose_name_plural': '预定商品',
                'db_table': 'qb_order_goods',
            },
        ),
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('image', models.ImageField(upload_to='goods', verbose_name='图片')),
                ('daily_sku', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.DailyGoodsSKU', verbose_name='日常商品SKU')),
                ('order_sku', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.OrderGoodsSKU', verbose_name='预定商品SKU')),
            ],
            options={
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
                'db_table': 'qb_goods_image',
            },
        ),
        migrations.CreateModel(
            name='GoodsBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('display_type', models.SmallIntegerField(choices=[(0, '标题'), (1, '图片')], default=1, verbose_name='展示类型')),
                ('index', models.SmallIntegerField(default=0, verbose_name='显示顺序')),
                ('daily_sku', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.DailyGoodsSKU', verbose_name='日常商品SKU')),
                ('order_sku', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.OrderGoodsSKU', verbose_name='预定商品SKU')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsType', verbose_name='商品类型')),
            ],
            options={
                'verbose_name': '主页分类展示商品',
                'verbose_name_plural': '主页分类展示商品',
                'db_table': 'qb_banner_goods',
            },
        ),
        migrations.AddField(
            model_name='dailygoodssku',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='所属SPU'),
        ),
        migrations.AddField(
            model_name='dailygoodssku',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsType', verbose_name='所属类别'),
        ),
    ]
