import re

from django.contrib.auth import login, logout
from rest_framework import generics, views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import LoginSerializer
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.views.generic import View
from django.template import loader
from inspection.models import InspectRecord, InspectSchedule, OrderStatus, WorkingRecord, OtherEvents, Matter
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from apiv1.serializers import InspectSerializer
from rest_framework import status
from django.db import connection


class LoginView(generics.GenericAPIView):
    """ログインAPIクラス"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'detail': "ログインが成功しました。"})


class LogoutView(views.APIView):
    """ログアウトAPIクラス"""

    def post(self, request):
        logout(request)
        return Response({'detail': "ログアウトが成功しました。"})

    def get(self, request):
        logout(request)
        return Response({"detail": "ログアウトが成功しました。"})


class AuthenticateView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {
            'user': str(request.user),
            'is_staff': str(request.user.is_staff),
        }
        return Response(content)


class InputInspectView(View):
    def get(self, request, executedate):
        queryset = InspectRecord.objects.filter(inspect_date=executedate)
        queryset = queryset.order_by('created_at')
        template = loader.get_template('inputform/inspectresult.html')
        context = {
            'execute_date': executedate,
            'record_list': queryset,
        }

        return HttpResponse(template.render(context, request))


class FixInspectView(View):
    def get(self, request, recordid):
        template = loader.get_template('fixform/fixinspect.html')
        try:
            queryset = InspectRecord.objects.get(id=recordid)
            context = {
                'inspect_date': queryset.inspect_date,
                'operator': queryset.operator.operator_name,
                'customer_name': queryset.customer.customer_name,
                'description': queryset.item.description,
                'inspect_qty': queryset.inspect_qty,
                'defective_qty': queryset.defective_qty,
                'shipping_qty': queryset.shipping_qty,
                'record_id': recordid,
                'operator_id': queryset.operator.id,
                'customer_id': queryset.customer.id,
                'item_number': queryset.item.item_number,
            }

        except ObjectDoesNotExist:
            print("The record doesn't exist.")

        return HttpResponse(template.render(context, request))


class FixInspectScheduleView(View):
    def get(self, request, recordid):
        template = loader.get_template('fixform/fixinspectschedule.html')
        try:
            queryset = InspectSchedule.objects.get(id=recordid)
            context = {
                'inspect_date': queryset.scheduled_inspect_date,
                'operator': queryset.operator.operator_name,
                'description': queryset.item.description,
                'record_id': recordid,
                'operator_id': queryset.operator.id,
                'item_number': queryset.item.item_number,
            }

        except ObjectDoesNotExist:
            print("The record doesn't exist.")

        return HttpResponse(template.render(context, request))


class FixOrderStatusView(View):
    def get(self, request, recordid):
        template = loader.get_template('fixform/fixorderstatus.html')
        try:
            queryset = OrderStatus.objects.get(id=recordid)
            context = {
                'inspect_date': queryset.scheduled_shipping_date,
                'description': queryset.item.description,
                'record_id': recordid,
                'item_number': queryset.item.item_number,
                'customer_name': queryset.customer.customer_name,
                'inspect_qty': queryset.order_qty,
                'item_id': queryset.item.id,
                'customer_id': queryset.customer.id,
            }

        except ObjectDoesNotExist:
            print("The record doesn't exist.")

        return HttpResponse(template.render(context, request))


class InputScheduleView(View):
    def get(self, request, executedate):
        template = loader.get_template('inputform/inspectschedule.html')
        context = {
            'execute_date': executedate,
        }

        return HttpResponse(template.render(context, request))


class InputOrderView(View):
    def get(self, request, executedate):
        template = loader.get_template('inputform/inputorder.html')
        context = {
            'execute_date': executedate,
        }

        return HttpResponse(template.render(context, request))


class WorkingRecordView(View):
    def get(self, request, executedate):
        queryset = WorkingRecord.objects.filter(working_date=executedate).order_by('created_at')
        template = loader.get_template('inputform/inputworking.html')
        context = {
            'execute_date': executedate,
            'record_list': queryset,
        }

        return HttpResponse(template.render(context, request))


class ShowThisDayView(View):
    def get(self, request, executedate):
        template = loader.get_template('showthisday.html')
        context = {
            'execute_date': executedate,
        }

        return HttpResponse(template.render(context, request))


class FixWorkingRecordView(View):
    def get(self, request, recordid):
        template = loader.get_template('fixform/fixworkingrecord.html')
        try:
            queryset = WorkingRecord.objects.get(id=recordid)
            context = {
                'inspect_date': queryset.working_date,
                'operator': queryset.operator.operator_name,
                'customer_name': queryset.customer.customer_name,
                'working_contents': queryset.working_contents,
                'working_minutes': queryset.working_minutes,
                'record_id': recordid,
                'operator_id': queryset.operator.id,
                'customer_id': queryset.customer.id,
            }

        except ObjectDoesNotExist:
            print("The record doesn't exist.")

        return HttpResponse(template.render(context, request))


class OtherEventsView(View):
    def get(self, request, executedate):
        template = loader.get_template('inputform/inputevent.html')
        context = {
            'execute_date': executedate,
        }

        return HttpResponse(template.render(context, request))


class FixOtherEventsView(View):
    def get(self, request, recordid):
        template = loader.get_template('fixform/fixevent.html')
        try:
            queryset = OtherEvents.objects.get(id=recordid)
            context = {
                'record_id': recordid,
                'inspect_date': queryset.event_date,
                'working_contents': queryset.event_title,
            }

        except ObjectDoesNotExist:
            print("The record doesn't exist.")

        return HttpResponse(template.render(context, request))


class FixMattersView(View):
    def get(self, request, recordid):
        template = loader.get_template('matterform/fix-matters.html')
        try:
            queryset = Matter.objects.get(id=recordid)
            context = {
                'record_id': recordid,
                'sheet_matter_id': "" if queryset.sheet_matter_id is None else queryset.sheet_matter_id,
                'entry_date': queryset.entry_date,
                'sales_person': "" if queryset.sales_person is None else queryset.sales_person,
                'matter_item_number': queryset.matter_item_number,
                'item_description': "" if queryset.item_description is None else queryset.item_description,
                'item_receive_date': "" if queryset.item_receive_date is None else queryset.item_receive_date,
                'first_action_date': "" if queryset.first_action_date is None else queryset.first_action_date,
                'first_action': "" if queryset.first_action is None else queryset.first_action,
                'is_inspect_item': queryset.is_inspect_item,
                'is_registered': queryset.is_registered,
                'is_sample_supplied': queryset.is_sample_supplied,
                'sample_handling': "" if queryset.sample_handling is None else queryset.sample_handling,
                'return_handling': "" if queryset.return_handling is None else queryset.return_handling,
                'complaint_number': "" if queryset.complaint_number < 1 else queryset.complaint_number,
                'complaint_open_date': "" if queryset.complaint_open_date is None else queryset.complaint_open_date,
                'ltd_shipping_date': "" if queryset.ltd_shipping_date is None else queryset.ltd_shipping_date,
                'ltd_answer_date': "" if queryset.ltd_answer_date is None else queryset.ltd_answer_date,
                'ltd_answer': "" if queryset.ltd_answer is None else queryset.ltd_answer,
                'closed_date': "" if queryset.closed_date is None else queryset.closed_date,
                'remark': "" if queryset.remark is None else queryset.remark,
                'is_closed': queryset.is_closed,
                'customer_name': "" if queryset.customer.customer_name is None else queryset.customer.customer_name,
                'customer_id': queryset.customer.id,
            }

        except ObjectDoesNotExist:
            print("The record doesn't exist.")

        return HttpResponse(template.render(context, request))


class AggregateView(View):
    def get(self, request, executedate):
        template = loader.get_template('inputform/aggregate.html')
        context = {
            'execute_date': executedate,
        }

        return HttpResponse(template.render(context, request))


class AggregateThisMonthInspectMinutesAPIView(views.APIView):

    def get(self, request):
        startDate = ''
        endDateNext = ''
        if "start_date" not in request.GET:
            pass
        else:
            startDate = request.GET.get("start_date")

        if "end_date_next" not in request.GET:
            pass
        else:
            endDateNext = request.GET.get("end_date_next")

        try:
            if (re.search(r'^\d{4}-\d{2}-\d{2}$', startDate) is None) | (re.search(r'^\d{4}-\d{2}-\d{2}$',
                                                                                   endDateNext) is None):
                raise ValidationError('引数が不正です')

            sql = ""
            sql += " SELECT Inspect.operator_id, C.district_id, C.customer_name, Inspect.cnt_item, Inspect.total_i, "
            sql += " Inspect.total_d, Inspect.total_minutes "
            sql += " FROM ("
            sql += " SELECT Isp.cnt_item, Isp.total_i, Isp.total_d, W.total_minutes, "
            sql += " Isp.customer_id, Isp.operator_id "
            sql += " FROM ("
            sql += " SELECT "
            sql += " COUNT(*) AS cnt_item, SUM(It.itm_i) AS total_i, SUM(It.itm_d) AS total_d, "
            sql += " It.customer_id, It.operator_id "
            sql += " FROM ("
            sql += " SELECT "
            sql += " SUM(inspect_qty) AS itm_i, SUM(defective_qty) AS itm_d , customer_id, "
            sql += " mod(item_id, 10000000) AS item_number, operator_id "
            sql += " FROM inspect_record "
            sql += " WHERE inspect_date >= '" + startDate + "'"
            sql += " AND inspect_date < '" + endDateNext + "'"
            sql += " AND inspect_qty > 0 "
            sql += " GROUP BY customer_id, item_number, operator_id "
            sql += " ) AS It "
            sql += " GROUP BY It.customer_id, It.operator_id "
            sql += " ) AS Isp INNER JOIN "
            sql += " ("
            sql += " SELECT SUM(working_minutes) AS total_minutes, customer_id, operator_id "
            sql += " FROM working_record "
            sql += " WHERE working_date >= '" + startDate + "'"
            sql += " AND working_date < '" + endDateNext + "'"
            sql += " AND working_contents = '出荷前検査'"
            sql += " GROUP BY customer_id, operator_id "
            sql += " ) AS W ON Isp.customer_id = W.customer_id AND Isp.operator_id = W.operator_id "
            sql += " ) AS Inspect INNER JOIN customer C "
            sql += " ON Inspect.customer_id = C.id "
            sql += " ORDER BY Inspect.operator_id, C.district_id, C.customer_name "
            sql += ";"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                sql_result = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
        except():
            print("error")

        return Response(sql_result, status.HTTP_200_OK)


class AggregateThisMonthWorkingAPIView(views.APIView):

    def get(self, request):
        startDate = ''
        endDateNext = ''
        if "start_date" not in request.GET:
            pass
        else:
            startDate = request.GET.get("start_date")

        if "end_date_next" not in request.GET:
            pass
        else:
            endDateNext = request.GET.get("end_date_next")

        try:
            if (re.search(r'^\d{4}-\d{2}-\d{2}$', startDate) is None) | (re.search(r'^\d{4}-\d{2}-\d{2}$',
                                                                                   endDateNext) is None):
                raise ValidationError('引数が不正です')

            sql = ""
            sql += "SELECT WC.operator_id, WC.district_id, WC.customer_name, SUM(WC.working_minutes) "
            sql += "AS total_minutes "
            sql += "FROM ("
            sql += "SELECT C.district_id, W.customer_id, C.customer_name, W.working_contents, "
            sql += "W.working_minutes, W.operator_id "
            sql += "FROM working_record W "
            sql += "INNER JOIN customer C "
            sql += "ON W.customer_id = C.id WHERE W.working_date >= '" + startDate + "'"
            sql += "AND W.working_date < '" + endDateNext + "' "
            sql += "AND W.working_contents <> '出荷前検査'"
            sql += ") AS WC "
            sql += "GROUP BY WC.district_id, WC.customer_name, WC.operator_id "
            sql += "order by WC.operator_id, WC.district_id, WC.customer_name "
            sql += ";"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                sql_result = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
        except():
            print("error")

        return Response(sql_result, status.HTTP_200_OK)


class DummyCrossTabulationMonthlyInspectAPIView(views.APIView):

    def get(self, request):
        startDate = ''
        endDateNext = ''
        if "start_date" not in request.GET:
            pass
        else:
            startDate = request.GET.get("start_date")

        if "end_date_next" not in request.GET:
            pass
        else:
            endDateNext = request.GET.get("end_date_next")

        try:
            if (re.search(r'^\d{4}-\d{2}-\d{2}$', startDate) is None) | (re.search(r'^\d{4}-\d{2}-\d{2}$',
                                                                                   endDateNext) is None):
                raise ValidationError('引数が不正です')

            sql = ""
            sql += " SELECT IT.description, IT.producer_id, sum(IRC.inspect_qty) AS inspect_total,"
            sql += " sum(IRC.defective_qty) AS defective_total, IRC.customer_name"
            sql += " FROM "
            sql += "( "
            sql += "( "
            sql += " SELECT IR.item_id, IR.inspect_qty, IR.defective_qty, C.customer_name"
            sql += " FROM "
            sql += " (SELECT item_id, inspect_qty, defective_qty, customer_id"
            sql += " FROM inspect_record) AS IR"
            sql += " INNER JOIN "
            sql += " (SELECT id, customer_name FROM customer WHERE customer_name = '水島機工') AS C"
            sql += " ON IR.customer_id = C.id"
            sql += ") AS IRC"
            sql += " INNER JOIN "
            sql += " (SELECT id, producer_id, description FROM item) AS IT"
            sql += " ON IRC.item_id = IT.id"
            sql += ") "
            sql += " GROUP BY IT.description, IT.producer_id, IRC.customer_name"
            sql += " ORDER BY IT.description"
            sql += " ;"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                sql_result = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
        except():
            print("error")

        return Response(sql_result, status.HTTP_200_OK)


class CrossTabulationMonthlyInspectAPIView(views.APIView):

    def get(self, request):
        startDate = ''
        endDateNext = ''
        if "start_date" not in request.GET:
            pass
        else:
            startDate = request.GET.get("start_date")

        if "end_date_next" not in request.GET:
            pass
        else:
            endDateNext = request.GET.get("end_date_next")

        try:
            if (re.search(r'^\d{4}-\d{2}-\d{2}$', startDate) is None) | (re.search(r'^\d{4}-\d{2}-\d{2}$',
                                                                                   endDateNext) is None):
                raise ValidationError('引数が不正です')

            sql = ""
            sql += " SELECT Aggr.item_id, Aggr.district_id, Aggr.customer_name, Aggr.description, Aggr.operator_name, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '01' THEN Aggr.inspect_qty ELSE 0 END) AS JAN, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '01' THEN Aggr.defective_qty ELSE 0 END) AS JAN_def, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '02' THEN Aggr.inspect_qty ELSE 0 END) AS FEB, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '02' THEN Aggr.defective_qty ELSE 0 END) AS FEB_def, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '03' THEN Aggr.inspect_qty ELSE 0 END) AS MAR, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '03' THEN Aggr.defective_qty ELSE 0 END) AS MAR_def, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '04' THEN Aggr.inspect_qty ELSE 0 END) AS APR, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '04' THEN Aggr.defective_qty ELSE 0 END) AS APR_def, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '05' THEN Aggr.inspect_qty ELSE 0 END) AS MAY, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '05' THEN Aggr.defective_qty ELSE 0 END) AS MAY_def, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '06' THEN Aggr.inspect_qty ELSE 0 END) AS JUN, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '06' THEN Aggr.defective_qty ELSE 0 END) AS JUN_def, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '07' THEN Aggr.inspect_qty ELSE 0 END) AS JUL, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '07' THEN Aggr.defective_qty ELSE 0 END) AS JUL_def, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '08' THEN Aggr.inspect_qty ELSE 0 END) AS AUG, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '08' THEN Aggr.defective_qty ELSE 0 END) AS AUG_def, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '09' THEN Aggr.inspect_qty ELSE 0 END) AS SEP, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '09' THEN Aggr.defective_qty ELSE 0 END) AS SEP_def, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '10' THEN Aggr.inspect_qty ELSE 0 END) AS OCT, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '10' THEN Aggr.defective_qty ELSE 0 END) AS OCT_def, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '11' THEN Aggr.inspect_qty ELSE 0 END) AS NOV, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '11' THEN Aggr.defective_qty ELSE 0 END) AS NOV_def, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '12' THEN Aggr.inspect_qty ELSE 0 END) AS DEC, "
            sql += " SUM(CASE WHEN Aggr.inspect_month = '12' THEN Aggr.defective_qty ELSE 0 END) AS DEC_def "
            sql += " FROM "
            sql += "("
            sql += " SELECT IIC.item_id, IIC.description, IIC.inspect_month, IIC.inspect_qty, IIC.defective_qty, "
            sql += " IIC.operator_id, Op.operator_name, IIC.customer_name, IIC.district_id "
            sql += " FROM "
            sql += "("
            sql += " SELECT II.item_id, II.description, II.inspect_month, II.inspect_qty, II.defective_qty, "
            sql += " II.operator_id, C.customer_name, C.district_id "
            sql += " FROM "
            sql += "("
            sql += " SELECT Ir.item_id, It.description, Ir.inspect_month, Ir.inspect_qty, Ir.defective_qty, "
            sql += " Ir.operator_id, Ir.customer_id "
            sql += " FROM "
            sql += "("
            sql += " SELECT item_id, to_char(inspect_date, 'MM') AS inspect_month, "
            sql += " inspect_qty, defective_qty, operator_id, customer_id FROM inspect_record "
            sql += " WHERE inspect_date >= '"
            sql += startDate[:4] + "-01-01' AND inspect_date < '" + endDateNext + "'"
            sql += " AND inspect_qty > 0 "
            sql += ") AS Ir INNER JOIN item It ON Ir.item_id = It.id "
            sql += ") AS II INNER JOIN customer C ON II.customer_id = C.id "
            sql += ") AS IIC INNER JOIN operator Op ON IIC.operator_id = Op.id "
            sql += ") AS Aggr "
            sql += " GROUP BY Aggr.item_id, Aggr.district_id, Aggr.customer_name, Aggr.operator_id, "
            sql += " Aggr.description, Aggr.operator_name "
            sql += " ORDER BY Aggr.district_id, Aggr.customer_name, Aggr.description, Aggr.operator_id "

            sql += " ;"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                sql_result = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
        except():
            print("error")

        return Response(sql_result, status.HTTP_200_OK)


class CrossTabulationMonthlyShippingAPIView(views.APIView):

    def get(self, request):
        startDate = ''
        endDateNext = ''
        if "start_date" not in request.GET:
            pass
        else:
            startDate = request.GET.get("start_date")

        if "end_date_next" not in request.GET:
            pass
        else:
            endDateNext = request.GET.get("end_date_next")

        try:
            if (re.search(r'^\d{4}-\d{2}-\d{2}$', startDate) is None) | (re.search(r'^\d{4}-\d{2}-\d{2}$',
                                                                                   endDateNext) is None):
                raise ValidationError('引数が不正です')

            sql = ""
            sql += " SELECT Aggr.district_id, Aggr.customer_name, Aggr.ord_description, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '01' THEN Aggr.shipping_qty ELSE 0 END) AS JAN, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '02' THEN Aggr.shipping_qty ELSE 0 END) AS FEB, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '03' THEN Aggr.shipping_qty ELSE 0 END) AS MAR, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '04' THEN Aggr.shipping_qty ELSE 0 END) AS APR, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '05' THEN Aggr.shipping_qty ELSE 0 END) AS MAY, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '06' THEN Aggr.shipping_qty ELSE 0 END) AS JUN, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '07' THEN Aggr.shipping_qty ELSE 0 END) AS JUl, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '08' THEN Aggr.shipping_qty ELSE 0 END) AS AUG, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '09' THEN Aggr.shipping_qty ELSE 0 END) AS SEP, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '10' THEN Aggr.shipping_qty ELSE 0 END) AS OCT, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '11' THEN Aggr.shipping_qty ELSE 0 END) AS NOV, "
            sql += " SUM(CASE WHEN Aggr.shipping_month = '12' THEN Aggr.shipping_qty ELSE 0 END) AS DEC "
            sql += " FROM "
            sql += "("
            sql += " SELECT REGEXP_REPLACE(II.description, '(-R$)|(-B8$)', '') AS ord_description, "
            sql += " II.shipping_month, II.shipping_qty, C.customer_name, C.district_id "
            sql += " FROM "
            sql += "("
            sql += " SELECT It.description, Ir.shipping_month, Ir.shipping_qty, Ir.customer_id "
            sql += " FROM "
            sql += "("
            sql += " SELECT item_id, to_char(inspect_date, 'MM') AS shipping_month, "
            sql += " shipping_qty, customer_id FROM inspect_record "
            sql += " WHERE inspect_date >= '"
            sql += startDate[:4] + "-01-01' AND inspect_date < '" + endDateNext + "'"
            sql += " AND shipping_qty > 0 "
            sql += ") AS Ir INNER JOIN item It ON Ir.item_id = It.id "
            sql += ") AS II INNER JOIN customer C ON II.customer_id = C.id "
            sql += ") AS Aggr "
            sql += " GROUP BY Aggr.district_id, Aggr.customer_name, Aggr.ord_description "
            sql += " ORDER BY Aggr.district_id, Aggr.customer_name, Aggr.ord_description "
            sql += " ;"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                sql_result = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
        except():
            print("error")

        return Response(sql_result, status.HTTP_200_OK)
