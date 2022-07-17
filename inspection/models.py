from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Customized User Model"""
    pass


class Operator(models.Model):
    """担当者"""

    class Meta:
        db_table = 'operator'

    id = models.IntegerField(primary_key=True, verbose_name='担当者ID')
    operator_name = models.CharField(verbose_name='担当者名', max_length=10)
    is_delete = models.BooleanField(verbose_name='削除', default=False)
    is_working = models.BooleanField(verbose_name='在籍', default=True)

    def __str__(self):
        return self.operator_name


class Item(models.Model):
    """アイテムリスト"""

    class Meta:
        db_table = 'item'

    id = models.IntegerField(primary_key=True, verbose_name='アイテムid')
    producer_id = models.IntegerField(verbose_name='メーカー', default=1)
    item_number = models.IntegerField(verbose_name='アイテム番号')
    description = models.CharField(verbose_name='型番', max_length=30)
    short_name = models.CharField(verbose_name='略称', max_length=16)
    inspected_qty = models.IntegerField(verbose_name='検査済み数', default=0)
    is_delete = models.BooleanField(verbose_name='削除', default=False)

    def __str__(self):
        return self.description


class District(models.Model):
    """地区コード"""

    class Meta:
        db_table = 'district'

    district_code = models.IntegerField(primary_key=True, verbose_name='地区コード')
    district_name = models.CharField(verbose_name='地区', max_length=20)
    is_delete = models.BooleanField(verbose_name='削除', default=False)


class Customer(models.Model):
    """ユーザーリスト"""

    class Meta:
        db_table = 'customer'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(verbose_name='ユーザー名', max_length=20)
    district = models.ForeignKey(District, verbose_name='地区コード', on_delete=models.PROTECT)
    is_delete = models.BooleanField(verbose_name='削除', default=False)

    def __str__(self):
        return self.customer_name


class OrderStatus(models.Model):
    """オーダー履歴"""

    class Meta:
        db_table = 'order_status'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, verbose_name='アイテム番号', on_delete=models.PROTECT)
    scheduled_shipping_date = models.DateField(verbose_name='出荷予定日')
    order_qty = models.IntegerField(verbose_name='出荷予定数量', default=0)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    customer = models.ForeignKey(Customer, verbose_name='ユーザー名', on_delete=models.PROTECT)


class InspectSchedule(models.Model):
    """検査予定"""

    class Meta:
        db_table = 'inspect_schedule'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, verbose_name='アイテム番号', on_delete=models.PROTECT)
    operator = models.ForeignKey(Operator, verbose_name='検査担当', on_delete=models.PROTECT)
    scheduled_inspect_date = models.DateField(verbose_name='検査予定日')
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)


class InspectRecord(models.Model):
    """検査履歴"""

    class Meta:
        db_table = 'inspect_record'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, verbose_name='アイテム', on_delete=models.PROTECT)
    inspect_date = models.DateField(verbose_name='検査日')
    inspect_qty = models.IntegerField(verbose_name='検査数量', default=0)
    defective_qty = models.IntegerField(verbose_name='出荷不可数', default=0)
    shipping_qty = models.IntegerField(verbose_name='出荷数量', default=0)
    operator = models.ForeignKey(Operator, verbose_name='検査担当', on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, verbose_name='ユーザー名', on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)


class WorkingRecord(models.Model):
    """作業履歴"""

    class Meta:
        db_table = 'working_record'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    working_date = models.DateField(verbose_name='作業日')
    working_contents = models.CharField(verbose_name='作業内容', max_length=128)
    working_minutes = models.IntegerField(verbose_name='作業時間(分)', default=0)
    operator = models.ForeignKey(Operator, verbose_name='作業担当', on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, verbose_name='ユーザー名', on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)


class OtherEvents(models.Model):
    """その他イベント記入用モデル"""

    class Meta:
        db_table = 'other_events'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_date = models.DateField(verbose_name='予定日')
    event_title = models.CharField(verbose_name='イベント名', max_length=30)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)


class Distributor(models.Model):
    """代理店リスト用モデル"""

    class Meta:
        db_table = 'distributor'

    distributor_code = models.IntegerField(primary_key=True, verbose_name='代理店コード')
    short_name = models.CharField(verbose_name='代理店記号', max_length=32)
    long_name = models.CharField(verbose_name='代理店名', max_length=64)


class Branch(models.Model):
    """支店コード用モデル"""

    class Meta:
        db_table = 'branch'

    branch_code = models.IntegerField(primary_key=True, verbose_name='支店コード')
    branch_name = models.CharField(verbose_name='支店名', max_length=10)


class NeedInspection(models.Model):
    """要検査品リスト用モデル"""

    class Meta:
        db_table = 'need_inspection'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dealer = models.CharField(verbose_name='販売店名', max_length=32)
    end_user = models.CharField(verbose_name='ユーザー名', max_length=32)
    comment = models.CharField(verbose_name='備考', max_length=128)
    is_expire = models.BooleanField(verbose_name='検査終了', default=False)
    item = models.ForeignKey(Item, verbose_name='アイテム', on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, verbose_name='支店名', on_delete=models.PROTECT)
    distributor = models.ForeignKey(Distributor, verbose_name='代理店名', on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)


class Matter(models.Model):
    """Complaint 案件モデル"""

    class Meta:
        db_table = 'matter'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sheet_matter_id = models.CharField(verbose_name='管理番号', max_length=20)
    entry_date = models.DateField(verbose_name='登録日')
    sales_person = models.CharField(verbose_name='営業担当', max_length=32)
    matter_item_number = models.IntegerField(verbose_name='アイテム番号', default=0)
    item_description = models.CharField(verbose_name='型番', max_length=32)
    item_receive_date = models.DateField(verbose_name='アイテム受取日', null=True)
    first_action_date = models.DateField(verbose_name='初動日', null=True)
    first_action = models.CharField(verbose_name='初動内容', max_length=128, null=True)
    is_inspect_item = models.BooleanField(verbose_name='要検査品', default=False)
    is_registered = models.BooleanField(verbose_name='要検査登録済み', default=False)
    is_sample_supplied = models.BooleanField(verbose_name='サンプル提出あり', default=False)
    sample_handling = models.CharField(verbose_name='サンプル処理', max_length=64, null=True)
    return_handling = models.CharField(verbose_name='返品処理', max_length=64, null=True)
    complaint_number = models.IntegerField(verbose_name='コンプレイント番号', default=0)
    complaint_open_date = models.DateField(verbose_name='コンプレイントオープン日', null=True)
    ltd_shipping_date = models.DateField(verbose_name='LTD出荷日', null=True)
    ltd_answer_date = models.DateField(verbose_name='LTD回答日', null=True)
    ltd_answer = models.CharField(verbose_name='LTD回答', max_length=32, null=True)
    closed_date = models.DateField(verbose_name='完了日', null=True)
    remark = models.CharField(verbose_name='処理結果', max_length=128, null=True)
    is_closed = models.BooleanField(verbose_name='完了', default=False)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    customer = models.ForeignKey(Customer, verbose_name='ユーザーid', on_delete=models.PROTECT)
