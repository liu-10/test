# 定义索引类
from haystack import indexes
# 导入模型类
from goods.models import DailyGoodsSKU, OrderGoodsSKU


# 索引类名固定格式：模型类名+Index
class DailyGoodsSKUIndex(indexes.SearchIndex,indexes.Indexable):
    # 索引字段 use_template根据表中那些字段建立索引文件的说明放在一个文件中
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        # 返回模型类
        return DailyGoodsSKU

    # 建立索引的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()


# 索引类名固定格式：模型类名+Index
class OrderGoodsSKUIndex(indexes.SearchIndex,indexes.Indexable):
    # 索引字段 use_template根据表中那些字段建立索引文件的说明放在一个文件中
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        # 返回模型类
        return OrderGoodsSKU

    # 建立索引的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()