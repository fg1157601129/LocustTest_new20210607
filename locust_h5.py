import json
from locust import HttpUser,task,TaskSet,SequentialTaskSet,between,tag
from locust.contrib.fasthttp import FastHttpUser,ResponseContextManager,FastResponse
import os
import random
import time
from faker import Faker
fake = Faker(locale="zh_CN")
payload_login = {
    "username": "10900190103",
    "password": "a123456",
    "ver": 1
}
# h = {
#     'Host': 'power.medcloud.cn',
#     'Cookie': f'_token={self.token}; _token={self.token}; _refreshToken={self.token}; _tenantId=376; _topParentId=546; _institutionChainType=2; DENTAIL_USER_ID=2279; DENTAL_MEDICAL_INSTITUTION_ID=553',
#     'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
#     'accept': 'application/json, text/plain, */*',
#     'sec-ch-ua-mobile': '?0',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
#     'content-type': 'application/x-www-form-urlencoded',
#     'origin': 'https://power.medcloud.cn',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-dest': 'empty',
#     'referer': f"{self.host}{self.path_add_items}",
#     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
# }

# 随机生成3-10个中文字符
def nickname_random():
    nick_name = ""
    for i in range(random.randint(3,10)):
        val = chr(random.randint(0x4e00, 0x9fbf))
        nick_name += val
    return nick_name


# token = 'd6eba7a8-0492-41ce-a402-93ea11cbf1fd'


class MyUser(FastHttpUser):
    wait_time = between(0.1, 0.2)


    # def login(self):
    #     # 用户登录,已经过期
    #     with self.client.post(path='/v1/student/login', data=json.dumps(payload_login), headers=headers,
    #                           verify=False) as response:
    #         try:
    #             assert 'token' in response.json()
    #         except Exception:
    #             pass
    #         return response.json()['data']['token']

    def on_start(self):
        #headers['Authorization'] = self.login()

        #   公共参数
        self.host = "https://power.medcloud.cn"   # 被测主机地址
        self.token = "da19920c88ef447d9eb7f9faa6326a88"
        self.uid = 2279
        self.mtId = 553
        self.tenantId = 376
        self.cmtId = 546
        self.cmtType = 2
        self.tag_str = fake.password(length=6)

        self.headers = {
            'Host': 'power.medcloud.cn',
            'Cookie': f'_token={self.token}; _token={self.token}; _refreshToken={self.token}; _tenantId=376; _topParentId=546; _institutionChainType=2; DENTAIL_USER_ID=2279; DENTAL_MEDICAL_INSTITUTION_ID=553',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://power.medcloud.cn',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': '',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }


        #   查询支付渠道列表
        self.path_pay_transaction_channel = '/api/his/pay/settings/pay-transaction-channel/list'

        #   查询支付商列表
        self.path_pay_merchant_info = '/api/his/pay/merchant-info/list'

        #   根据支付单号查询支付单信息
        self.payBatchNo = "MP1135317825489994752"   # 切换环境需要变更
        self.business_no = "BO553202104160002"      # 切换环境需要变更
        self.orderType = 1
        self.path_pay_slect_order_info = "/api/his/pay/pay-order/select-by-pay-batch-no-and-business-no"

        #   查询支付记录列表
        self.payerId = 322653    # 切换环境需要变更
        self.current = 1
        self.size = 100
        self.path_payment_records = "/api/his/pay/pay-order/page-by-payer-id"

        #   根据支付单号查询支付单信息 or 查询账单明细
        self.path_select_bill_detail = "/api/his/pay/pay-order/select-order-item-by-business-no"
        # self.business_no = "RO665202103300006"     # 该接口也用到 business_no

        # 根据商品类型查询查询商品列表(新)
        self.path_merchandise_list_select = "/api/his/physical/merchandise/list-select"
        self.merchandiseInfo = ""
        self.startMerchandiseId = 0

        # 查询【商品类型】 列表
        self.path_merchandise_type = "/api/his/physical/merchandise/list/merchandise-type"

        # 采购单分页 or 【采购管理】
        self.path_procurement_management = "/api/his/physical/inventory/purchase/page"
        self.orderNo = ""
        self.medicalInstitutionId = 553
        self.purchaseTotalAmount = ""
        self.beginTimeMillis = "1618243200000"
        self.endTimeMillis = int(time.time()*1000)
        self.createStaffId = 2279   # 值 同 self.uid = 2681
        # self.current = 1  # 该接口也用到 self.current
        # self.size = 100   # 该接口也用到 self.size

        # 物品领用分页 or 经销存 -> 领用申请
        self.path_item_requisition_record = "/api/his/physical/merchandise/receive/page"
        self.receiveOrderNo = ""
        # self.beginTime = "1609430400000"   # 值 同 self.beginTimeMillis
        # self.endTime = "1617292800000"     # 值 同 self.endTimeMillis
        # self.current = 1  # 该接口也用到 self.current
        # self.size = 100   # 该接口也用到 self.size

        # 库存管理分页 or 【经销存 -> 仓储 -> 入库管理】
        self.path_warehouse_management = "/api/his/physical/inventory/input/page"
        # self.medicalInstitutionId = 553   # 该接口也用到 self.medicalInstitutionId
        self.inputInventoryOrderNo = ""
        self.returnSource = ""
        # self.beginTimeMillis = "1609430400000"    # 该接口也用到 self.beginTimeMillis
        # self.endTimeMillis = "1617292800000"    # 该接口也用到 self.endTimeMillis
        # self.current = 1  # 该接口也用到 self.current
        # self.size = 100   # 该接口也用到 self.size

        # 出库单分页 or 【经销存 -> 仓储 -> 出库管理】
        self.path_out_inventory = "/api/his/physical/inventory/output/page"
        # self.medicalInstitutionId = 553   # 该接口也用到 self.medicalInstitutionId
        self.outputInventoryOrderNo = ""
        # self.beginTimeMillis = "1609430400000"    # 该接口也用到 self.beginTimeMillis
        # self.endTimeMillis = "1617292800000"    # 该接口也用到 self.endTimeMillis
        # self.current = 1  # 该接口也用到 self.current
        # self.size = 100   # 该接口也用到 self.size

        # 库存盘点信息分页 or 【经销存 -> 仓储 -> 盘点管理】
        self.path_stock_taking = "/api/his/physical/inventory/check/page"
        # self.medicalInstitutionId = 553   # 该接口也用到 self.medicalInstitutionId
        self.searchForItems = ""
        self.merchandiseInputInventoryOrderNo = ""
        # self.beginTimeMillis = "1609430400000"    # 该接口也用到 self.beginTimeMillis
        # self.endTimeMillis = "1617292800000"    # 该接口也用到 self.endTimeMillis
        # self.current = 1  # 该接口也用到 self.current
        # self.size = 100   # 该接口也用到 self.size

        # 报损/报溢单分页 or 【经销存 -> 仓储 -> 报损报溢】
        self.path_loss_or_redundant = "/api/his/physical/inventory/increase-decrease/page"
        # self.beginTimeMillis = "1609430400000"    # 该接口也用到 self.beginTimeMillis
        # self.endTimeMillis = "1617292800000"    # 该接口也用到 self.endTimeMillis
        # self.current = 1  # 该接口也用到 self.current
        # self.size = 100   # 该接口也用到 self.size

        # 物品分页 or 【经销存 -> 基础配置 -> 物品管理】
        self.path_items_management = "/api/his/physical/merchandise/page"
        # self.current = 1  # 该接口也用到 self.current
        # self.size = 100   # 该接口也用到 self.size

        # 物品信息配置 or 【经销存 -> 基础配置 -> 物品信息配置】
        self.path_items_info_config = "/api/his/physical/settings/merchandise-message/page"
        self.merchandiseMessage = ""
        # self.current = 1  # 该接口也用到 self.current
        # self.size = 100   # 该接口也用到 self.size

        # 供应商分页 or 【经销存 -> 基础配置 -> 供应商管理】
        self.path_supplier_management = "/api/his/physical/merchandise/supplier/page"
        # self.queryBeginTimeStamp = "1609430400000"    # 值 同 self.beginTimeMillis
        # self.queryEndTimeStamp = "1617292800000"      # 值 同 self.endTimeMillis
        # self.current = 1  # 该接口也用到 self.current
        # self.size = 100   # 该接口也用到 self.size

        # 物品新增
        self.path_add_items = "/api/his/physical/merchandise/create"

        # 电子病历管理分页 or 【医疗业务】 -> 【病历管理】
        self.path_medical_records = "/api/his/diagnosis/medical-record/management/page"

        # 治疗记录列表-包含预约 or 患者详情 -> 就诊记录
        self.path_see_doctor_record = "/api/his/diagnosis/dental-record/v2/list"
        self.patientId = 322653  # 切换环境需要变更

        # 今日工作今日就诊分页(前台)
        self.path_today_seedoctor_reception = "/api/his/diagnosis/register/page-receptionist"
        self.patientSearchKey = ""
        self.charged = True
        self.hasCancel = False
        self.sortName = ""
        self.sort = ""
        # self.current = 1  # 该接口也用到 self.current
        # self.size = 100   # 该接口也用到 self.size
        # self.beginTime = "1609430400000"   # 值 同 self.beginTimeMillis
        # self.endTime = "1617292800000"     # 值 同 self.endTimeMillis

        # 今日工作今日就诊分页(医生)
        self.path_today_seedoctor_doctor = "/api/his/diagnosis/register/page-doctor"
        self.hasNotSpecified = False
        # self.current = 1  # 该接口也用到 self.current
        # self.size = 100   # 该接口也用到 self.size
        # self.beginTime = "1609430400000"   # 值 同 self.beginTimeMillis
        # self.endTime = "1617292800000"     # 值 同 self.endTimeMillis

        # 今日工作全局统计接口
        self.path_today_work_global_statistical = "/api/his/diagnosis/register-global/today-count"

        # 今日工作统计
        self.path_today_work_statistical = "/api/his/diagnosis/register-stat/today-work"

        # 电子病历详情
        self.path_electronic_medical_records_details = "/api/his/diagnosis/medical-record/detail"
        self.medicalRecordId = 25969    # 切换环境需调整

        # 前台-今日就诊(全部、已到、未到)统计
        self.path_today_seedoctor_reception_statistical = "/api/his/diagnosis/register/page-type-count"
        # self.patientSearchKey = "" 该接口也用到 self.patientSearchKey
        # self.charged = True 该接口也用到 self.charged
        # self.hasCancel = False 该接口也用到 self.hasCancel
        # self.sortName = "" 该接口也用到 self.sortName
        # self.sort = "" 该接口也用到 self.sort

        # （就诊）诊所资源 列表
        self.path_clinic_resources_list = "/api/his/diagnosis/register-resource/list"
        self.registerResourceType = 2

        # 患者ID 查询就诊记录 or 患者详情 -> 电子病历
        self.path_select_electronic_medical_records_patientId = "/api/his/diagnosis/register/list-patient"

        # 查询电子病历列表
        self.path_select_electronic_medical_records_list = "/api/his/diagnosis/medical-record/list"

        # 查询患者就诊次数
        self.path_select_see_doctor_count = "/api/his/diagnosis/register/list-patient/count"
        self.currentInstitution = True
        # 收费单打印
        self.path_bill_print = "/api/his/billing/pay/order/select"
        # 切换环境需要修改 账单号
        self.paySerialNos = "MP1123006132621673472,MP1123006132621673473,MP1123006132621673474"

        # 查询机构已收费列表 or 【今日工作】 -> 【已收费】
        self.path_today_has_charge_list = "/api/his/billing/bill/order/institution/pay-success-order-page"
        # self.createTimeStart = 1618243200000
        # self.createTimeEnd = 1618329599999
        self.patientMessage = ""
        # self.sortName = ""
        # self.sort = ""

        # 子账单复制明细列表
        self.path_copy_bill = "/api/his/billing/bill/order/copy"
        self.billSerialNo_ordinary = "BO553202103300013"

        # 收欠费 3.6.0新接口
        self.path_charge_and_owe = "/api/his/billing/bill/order/pay-debt"
        self.billSerialNo_cao = "BO553202103300012"

        # 三合一收费计算优惠 @3.6.0新接口
        self.path_calculation_of_preferential = "/api/his/billing/bill/order/pay-one/calc-promotion"

        # 收欠费计算优惠 3.6.0新接口
        self.path_calculation_of_preferential_cao = "/api/his/billing/bill/order/pay-debt/calc-promotion"

        # 查询待处理账单明细 @3.6.0新接口
        self.path_select_processed_bill_detail = "/api/his/billing/bill/order/wait"
        self.billSerialNo_processed = "BO553202103300006"

        # 保存账单或编辑账单 @3.6.0新接口
        self.path_saveOrUpdate_bill = "/api/his/billing/bill/order/saveOrUpdate"

        # 三合一收费 @3.6.0新接口
        self.path_triad_charge = "/api/his/billing/bill/order/pay-one"

        # 查询已收费账单明细 @3.6.0新接口
        self.path_select_has_charge_detail = "/api/his/billing/bill/order/item"
        self.billSerialNo_has_charge = "BO553202103300011"

        # 待处理账单列表
        self.path_Pending_bill_list = "/api/his/billing/bill/order/process/list"
        self.customerId = 3585075

        # 账单列表
        self.path_bill_list = "/api/his/billing/bill/order/page"

        # 机构收费列表
        self.path_institution_charge_list = "/api/his/billing/bill/order/institution/page"
        self.billStatus = 1

        # 收费项目下拉列表搜索查询
        self.path_select_charge_project_list = "/api/his/billing/settings/charge-item/select-list/fuzzy"
        self.searchValue = ""

        # 查询收费套餐类型类目列表(三级列表)
        self.path_select_package_type = "/api/his/billing/settings/charge-package-type/category-list"

        # 根据收费套餐类型ID查询套餐项目明细
        self.path_select_package_detail_by_typeid = "/api/his/billing/settings/charge-package-item/selectByTypeId"
        self.settingsChargePackageTypeId = 280

        # 收费套餐项目列表
        self.path_charge_package_list = "/api/his/billing/settings/charge-package-item/select"

        # 优惠券列表 @3.6.0新接口
        self.path_coupons_list = "/api/his/billing/new/coupon/select-coupon-list-by-user-id"

        # 发券
        self.path_create_promotion = "/api/his/billing/promotion/create"

        # 报表中心-报表下载 分页/列表数据
        self.path_stat_filerecord_page = "/api/his/patient/stat/filerecord/page"
        self.fileName = ""

        # 查询医嘱二级词条
        self.path_select_doctor_advice_entry = "/api/his/patient/settings/medical-record/doctor-advice-dict/select/secondLevel"

        # 查询处置二级词条
        self.path_select_disposal_entry = "/api/his/patient/settings/medical-record/dispose-dict/select/secondLevel"

        # 查询既往史二级词条
        self.path_select_past_illness_history_entry = "/api/his/patient/settings/medical-record/past-illness-history-dict/select/secondLevel"

        # 查询主诉二级词条
        self.path_select_chief_complaint_entry = "/api/his/patient/settings/medical-record/chief-complaint-dict/select/secondLevel"

        # 查询现病史二级词条
        self.path_select_present_illness_history_entry = "/api/his/patient/settings/medical-record/present-illness-history-dict/select/secondLevel"

        # 查询检查二级词条
        self.path_select_examination_entry = "/api/his/patient/settings/medical-record/examination-dict/select/secondLevel"

        # 查询治疗计划二级词条
        self.path_select_treatment_plan_entry = "/api/his/patient/settings/medical-record/treatment-plan-dict/select/secondLevel"

        # 根据患者id查询初诊信息
        self.path_first_visit_info = "/api/his/patient/patient/first-visit/info"

        # 查询所有患者来源
        self.path_patient_source_list_all = "/api/his/patient/settings/patient/source/list/all"

        # 该患者是否绑定过粉丝, true 已经绑定过 false 未绑定过
        self.path_has_bind = "/api/his/patient/official-account/has-bind"

        # 查询病例模板类型
        self.path_select_medical_record_template_type = "/api/his/patient/settings/medical-record/template-type/select"

        # 患者类型列表
        self.path_patient_type_list = "/api/his/patient/settings/type/list/regular"

        # 机构下全部患者数量
        self.path_patient_count_mtId = "/api/his/patient/patient/patient-count"

        # 全身检查列表展示
        self.path_body_check_one = "/api/his/patient/body-check/one"

        # 获取患者序列号
        self.path_obtain_patient_serial_num = "/api/his/patient/serial/medical-record/serial"
        self.patientType = 27

        # 查询病例号规则列表
        self.path_select_medical_record_num_rules = "/api/his/patient/serial/medical-record/list"

        # 分页/列表数据(包含详细) or 营收报表 -> 预约日报表
        self.path_appointment_day_report = "/api/his/patient/stat/operating/appointment-analysis/page"

        # 客户关系列表展示
        self.path_customer_relationship = "/api/his/patient/customer/relation/one"

        # 通过机构id查询所有客户标签/患者画像
        self.path_all_patient_tags = "/api/his/patient/patient/list/patient-tags"

        # 编辑回访
        self.path_update_visit = "/api/his/patient/return/visit/update"

        # 患者回访记录页面
        self.path_select_visit_record = "/api/his/patient/return/visit/patient/page"

        # 更新病例号规则
        self.path_update_case_num_rules = "/api/his/patient/serial/medical-record/update"

        # 报表中心-运营报表-就诊周期分析 分页/列表数据
        self.path_stat_operating_diagnosis = "/api/his/patient/stat/operating/diagnosis-period/page"

        # 客户回访页面:客户回访分页查询
        self.path_return_visit_customer_page = "/api/his/patient/return/visit/customer/page"
        self.customerInfo = "新能"
        self.visitStatus = 3
        self.planVisitStartTime = "2020-04-01+00:00:00"
        self.planVisitEndTime = "2021-04-14+23:59:59"
        self.p_sort = False

        # 预约分检分页查询
        self.path_institution_check = "/api/his/patient/institution/check/page"
        self.condition = ""
        # self.temperatureStartDate = "2020-04-01+00:00:00"
        # self.temperatureEndDate = "2021-04-14+23:59:59"
        self.judgement = 3
        self.temperature = 37.2

        # 回访详情
        self.path_return_visit_detail = "/api/his/patient/return/visit/detail"
        self.returnVisitId = 69735

        # 获取选择的地单子病历模板
        self.path_select_get_record_template = "/api/his/patient/settings/medical-record/get-select-patient-record-template"

        # 根据生日分页查询患者列表
        self.path_select_birthday_reminder = "/api/his/patient/patient/page/birthday-reminder"
        self.birthdayAmount = 0
        self.birthdayBegin = "04-15"
        self.birthdayEnd = "04-15"

        # 根据患者名称、拼音、手机号模糊查询患者
        self.path_fuzzy_query_patient = "/api/his/patient/patient/v2/home/list/regular"
        self.regularParam = 1

        # 根据机构id查询今日扫码患者数量
        self.path_select_today_scan_patient = "/api/his/patient/patient/today-scan/page"

        # 新增患者
        self.path_create_patient = "/api/his/patient/patient/create/with/patient-contact"

        # 编辑患者
        self.path_update_patient = "/api/his/patient/patient/update/with/patient-contact"

    #   可以按照 每个不同的服务，打上tag ；以下是 pay 模块
    @tag("pay")
    @task(1)
    #   查询支付渠道列表
    def pay_transaction_channel(self):

        # self.path_pay_transaction_channel =
        # '/api/his/pay/settings/pay-transaction-channel/list'

        with self.client.get(path=f'{self.host}{self.path_pay_transaction_channel}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN', headers=None,catch_response=True,name="查询支付渠道列表") as res:
            if res.status_code == 200:

                if (json.loads(res.text))["code"] == 0:
                    res.success()
                else:
                    res.failure(res.text)
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_pay_transaction_channel)

            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_pay_transaction_channel)

    @tag("pay")
    @task(1)
    #   查询支付商列表
    def pay_merchant_info(self):

        # self.path_pay_merchant_info =
        # '/api/his/pay/merchant-info/list'

        with self.client.get(
            path=f'{self.host}{self.path_pay_merchant_info}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None,catch_response=True,name="查询支付商列表") as res:
            if res.status_code == 200:

                if (json.loads(res.text))["code"] == 0:
                    res.success()
                else:
                    res.failure(res.text)
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_pay_merchant_info)

            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_pay_merchant_info)


    @tag("pay")
    @task(1)
    # 根据businessNo 编辑支付账单
    def pay_redact_oder(self):

        # self.path_pay_slect_order_info =
        # "/api/his/pay/pay-order/select-by-pay-batch-no-and-business-no"

        with self.client.get(path=f'{self.host}{self.path_pay_slect_order_info}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&payBatchNo={self.payBatchNo}&orderType={self.orderType}&businessNo={self.business_no}',
                        headers=None, catch_response=True,name="编辑支付账单") as res:
            if res.status_code == 200:

                if (json.loads(res.text))["code"] == 0:
                    res.success()
                else:
                    res.failure(res.text)
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_pay_slect_order_info)

            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_pay_slect_order_info)

    @tag("pay")
    @task(1)
    # 查询支付记录列表
    def payment_records(self):

        # self.path_payment_records =
        # "/api/his/pay/pay-order/page-by-payer-id"

        with self.client.get(
            path=f'{self.host}{self.path_payment_records}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&payerId={self.payerId}&current={self.current}&size={self.size}',
            headers=None, catch_response=True,name="查询支付记录列表") as res:
            if res.status_code == 200:

                if (json.loads(res.text))["code"] == 0:
                    res.success()
                else:
                    res.failure(res.text)
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_payment_records)

            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_payment_records)


    @tag("pay")
    @task(1)
    # 查询账单明细 （展开账单的子账单）
    def select_bill_detail(self):

        # self.path_select_bill_detail =
        # "/api/his/pay/pay-order/select-order-item-by-business-no"

        with self.client.get(
            path=f'{self.host}{self.path_select_bill_detail}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&businessNo={self.business_no}',
            headers=None, catch_response=True,name="查询账单明细") as res:
            if res.status_code == 200:

                if (json.loads(res.text))["code"] == 0:
                    res.success()
                else:
                    res.failure(res.text)
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_bill_detail)

            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_bill_detail)


    @tag("physical")
    @task(1)
    # 根据商品类型查询查询商品列表(新)
    def select_sales_goods_list(self):

        # self.path_merchandise_list_select =
        # "/api/his/physical/merchandise/list-select"

        with self.client.get(
            path=f'{self.host}{self.path_merchandise_list_select}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&merchandiseInfo=&startMerchandiseId={self.startMerchandiseId}',
            headers=None, catch_response=True,name="根据商品类型查询查询商品列表(新)") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_merchandise_list_select)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_merchandise_list_select)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_merchandise_list_select)


    @tag("physical")
    @task(1)
    # 查询【商品类型】 列表
    def func_select_goods_type(self):

        # self.path_merchandise_type =
        # "/api/his/physical/merchandise/list/merchandise-type"

        with self.client.get(
            path=f'{self.host}{self.path_merchandise_type}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="查询【商品类型】 列表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_merchandise_type)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_merchandise_type)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_merchandise_type)


    @tag("physical")
    @task(1)
    # 采购单分页 or 【经销存 -> 采购管理】
    def select_procurement_management(self):

        # self.path_procurement_management =
        # "/api/his/physical/inventory/purchase/page"

        with self.client.get(
            path=f'{self.host}{self.path_procurement_management}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&orderNo={self.orderNo}&medicalInstitutionId={self.medicalInstitutionId}&purchaseTotalAmount={self.purchaseTotalAmount}&beginTimeMillis={self.beginTimeMillis}&endTimeMillis={self.endTimeMillis}&createStaffId={self.createStaffId}&current={self.current}&size={self.size}',
            headers=None, catch_response=True,name="采购单分页") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_procurement_management)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_procurement_management)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_procurement_management)


    @tag("physical")
    @task(1)
    # 物品领用分页 or 经销存 -> 领用申请
    def item_requisition_record(self):

        # self.path_item_requisition_record =
        # "/api/his/physical/merchandise/receive/page"

        with self.client.get(
            path=f'{self.host}{self.path_item_requisition_record}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&receiveOrderNo={self.receiveOrderNo}&beginTime={self.beginTimeMillis}&endTime={self.endTimeMillis}&current={self.current}&size={self.size}',
            headers=None, catch_response=True,name="物品领用分页") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_item_requisition_record)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_item_requisition_record)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_item_requisition_record)
        # try:
        #     assert (json.loads(res.text))["code"] == 0
        #
        #     #print(res.text)
        #     print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "通过")
        # except Exception as err:
        #
        #     print(res.text)
        #     print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",self.path_item_requisition_record)

    @tag("physical")
    @task(1)
    # 库存管理分页 or 【经销存 -> 仓储 -> 入库管理】
    def select_warehouse_management(self):

        # self.path_warehouse_management =
        # "/api/his/physical/inventory/input/page"

        with self.client.get(
            path=f'{self.host}{self.path_warehouse_management}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&medicalInstitutionId={self.medicalInstitutionId}&inputInventoryOrderNo={self.inputInventoryOrderNo}&beginTimeMillis={self.beginTimeMillis}&endTimeMillis={self.endTimeMillis}&returnSource={self.returnSource}&current={self.current}&size={self.size}',
            headers=None, catch_response=True,name="库存管理分页") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_warehouse_management)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_warehouse_management)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_warehouse_management)


    @tag("physical")
    @task(1)
    # 出库单分页 or 【经销存 -> 仓储 -> 出库管理】
    def select_out_inventory(self):

        # self.path_out_inventory =
        # "/api/his/physical/inventory/output/page"

        with self.client.get(
            path=f'{self.host}{self.path_out_inventory}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&medicalInstitutionId={self.medicalInstitutionId}&outputInventoryOrderNo={self.outputInventoryOrderNo}&beginTimeMillis={self.beginTimeMillis}&endTimeMillis={self.endTimeMillis}&current={self.current}&size={self.size}',
            headers=None, catch_response=True,name="出库单分页") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_out_inventory)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_out_inventory)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_out_inventory)

    @tag("physical")
    @task(1)
    # 库存盘点信息分页 or 【经销存 -> 仓储 -> 盘点管理】
    def select_stock_taking(self):

        # self.path_stock_taking =
        # "/api/his/physical/inventory/check/page"

        with self.client.get(
            path=f'{self.host}{self.path_stock_taking}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&medicalInstitutionId={self.medicalInstitutionId}&searchForItems={self.searchForItems}&merchandiseInputInventoryOrderNo={self.merchandiseInputInventoryOrderNo}&beginTimeMillis={self.beginTimeMillis}&endTimeMillis={self.endTimeMillis}&current={self.current}&size={self.size}',
            headers=None, catch_response=True,name="库存盘点信息分页") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_stock_taking)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_stock_taking)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_stock_taking)


    @tag("physical")
    @task(1)
    # 报损/报溢单分页 or 【经销存 -> 仓储 -> 报损报溢】
    def select_loss_or_redundant(self):

        # self.path_loss_or_redundant =
        # "/api/his/physical/inventory/increase-decrease/page"

        with self.client.get(
            path=f'{self.host}{self.path_loss_or_redundant}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&beginTimeMillis={self.beginTimeMillis}&endTimeMillis={self.endTimeMillis}&current={self.current}&size={self.size}',
            headers=None, catch_response=True,name="报损/报溢单分页") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_loss_or_redundant)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_loss_or_redundant)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_loss_or_redundant)

    @tag("physical")
    @task(1)
    # 物品分页 or 【经销存 -> 基础配置 -> 物品管理】

    def select_merchandise_type(self):

        # self.path_items_management =
        # "/his/physical/merchandise/page"

        with self.client.get(
            path=f'{self.host}{self.path_items_management}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&current={self.current}&size={self.size}',
            headers=None, catch_response=True,name="物品分页") as res:
            # print(res.text)
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_items_management)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_items_management)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_items_management)


            # if res.status_code != 200:
            #     res.failure(res.text)
            #     print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_items_management)
            # elif (json.loads(res.text))["code"] != 0:
            #     res.failure(res.text)
            #     print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_items_management)
            # else:
            #     res.success()



    @tag("physical")
    @task(1)
    # 物品信息配置 or 【经销存 -> 基础配置 -> 物品信息配置】

    def items_info_config(self):

        # self.path_items_info_config =
        # "/api/his/physical/settings/merchandise-message/page"

        with self.client.get(
            path=f'{self.host}{self.path_items_info_config}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&merchandiseMessage={self.merchandiseMessage}&current={self.current}&size={self.size}',
            headers=None, catch_response=True,name="物品信息配置") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_items_info_config)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_items_info_config)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_items_info_config)


    @tag("physical")
    @task(1)
    # 供应商分页 or 【经销存 -> 基础配置 -> 供应商管理】

    def supplier_management(self):

        # self.path_supplier_management =
        # "/api/his/physical/merchandise/supplier/page"

        with self.client.get(
            path=f'{self.host}{self.path_supplier_management}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&queryBeginTimeStamp={self.beginTimeMillis}&queryEndTimeStamp={self.endTimeMillis}&current={self.current}&size={self.size}',
            headers=None, catch_response=True,name="供应商分页") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_supplier_management)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_supplier_management)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_supplier_management)




    @tag("physical")
    @task(1)
    # 物品新增

    def func_add_items(self):
        # self.path_add_items =
        # "/physical/merchandise/create"
        payload_data = {
            "_token":self.token,
            "_uid": self.uid,
            "_ut": 1,
            "_t": 1,
            "_s": 11,
            "_mtId": 546,
            "_tenantId": 376,
            "_cmtId": 546,
            "_cmtType": 2,
            "_lang": "zh_CN",
            "merchandiseCategoryId":6956,
            "merchandiseCategoryOneId": 6571,
            "merchandiseCategoryTwoId": 6946,
            "merchandiseCategoryThreeId": 6956,
            "merchandiseType": 1,
            "commonName": "LOCUST",
            "merchandiseName": fake.password(length=6),
            "aliasName": fake.password(length=6),
            "barCode": "TXMBH_" + str(random.randint(0,9999)),
            "manufacturer": "上海",
            "brandId": 6,
            "dosageFrom": 2,
            "purchaseUnitId": 3798,
            "inventoryUnitId": 3798,
            "unitSystem": 1,
            "specifications": 1,
            "isSale": True,
            "retailAmount": random.randint(0,9999),
            "prescriptionDrugUsage": 1,
            "prescriptionFrequency": 2,
            "prescriptionDosageUnit": 2,
            "prescriptionTotalUnit": 1,
            "merchandiseQualificationInformationArrayStr": ""
        }




        with self.client.post(
            path=f'{self.host}{self.path_add_items}',
            headers=None, data=payload_data ,catch_response=True, name="物品新增:/physical/merchandise/create") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_add_items)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_add_items)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_add_items)





    @tag("diagnosis")
    @task(1)
    # 电子病历管理分页 or 【医疗业务】-> 【病历管理】

    def func_medical_records_management(self):

        # self.path_medical_records =
        # "/api/his/diagnosis/medical-record/management/page"

        with self.client.get(
            path=f'{self.host}{self.path_medical_records}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&current={self.current}&size={self.size}',
            headers=None, catch_response=True,name="电子病历管理分页") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_medical_records)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_medical_records)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_medical_records)


    @tag("diagnosis")
    @task(1)
    # 治疗记录列表-包含预约 or 患者详情 -> 就诊记录

    def func_see_doctor_record(self):

        # self.path_see_doctor_record =
        # "/api/his/diagnosis/dental-record/v2/list"

        with self.client.get(
            path=f'{self.host}{self.path_see_doctor_record}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}',
            headers=None, catch_response=True, name="今日工作全局统计接口") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_see_doctor_record)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_see_doctor_record)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_see_doctor_record)


    @tag("diagnosis")
    @task(1)
    # 今日工作今日就诊分页(前台)

    def func_today_seedoctor_reception(self):

        # self.path_today_seedoctor_reception =
        # "/api/his/diagnosis/register/page-receptionist"

        with self.client.get(
            path=f'{self.host}{self.path_today_seedoctor_reception}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientSearchKey={self.patientSearchKey}&beginTime={self.beginTimeMillis}&endTime={self.endTimeMillis}&charged={self.charged}&hasCancel={self.hasCancel}&sortName={self.sortName}&sort={self.sort}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="今日工作今日就诊分页(前台)") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_seedoctor_reception)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_seedoctor_reception)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_seedoctor_reception)

    @tag("diagnosis")
    @task(1)
    # 今日工作今日就诊分页(医生)

    def func_today_seedoctor_doctor(self):

        # self.path_today_seedoctor_doctor =
        # "/api/his/diagnosis/register/page-doctor"

        with self.client.get(
            path=f'{self.host}{self.path_today_seedoctor_doctor}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientSearchKey={self.patientSearchKey}&beginTime={self.beginTimeMillis}&endTime={self.endTimeMillis}&hasNotSpecified={self.hasNotSpecified}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="今日工作今日就诊分页(医生)") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_today_seedoctor_doctor)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_seedoctor_doctor)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_seedoctor_doctor)




    @tag("diagnosis")
    @task(1)
    # 今日工作全局统计接口

    def func_today_work_global_statistical(self):

        # self.path_today_work_global_statistical =
        # "/api/his/diagnosis/register-global/today-count"

        with self.client.get(
            path=f'{self.host}{self.path_today_work_global_statistical}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True, name="今日工作全局统计接口") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_today_work_global_statistical)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_work_global_statistical)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_work_global_statistical)






    @tag("diagnosis")
    @task(1)
    # 今日工作统计

    def func_today_work_statistical(self):

        # self.path_today_work_statistical =
        # "/api/his/diagnosis/register-stat/today-work"

        with self.client.get(
            path=f'{self.host}{self.path_today_work_statistical}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&beginTimestamp={self.beginTimeMillis}&endTimestamp={self.endTimeMillis}',
            headers=None, catch_response=True, name="今日工作统计") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_today_work_statistical)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_work_statistical)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_work_statistical)





    @tag("diagnosis")
    @task(1)
    # 电子病历详情

    def func_electronic_medical_records_details(self):

        # self.path_electronic_medical_records_details =
        # "/api/his/diagnosis/medical-record/detail"

        with self.client.get(
            path=f'{self.host}{self.path_electronic_medical_records_details}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&medicalRecordId={self.medicalRecordId}',
            headers=None, catch_response=True, name="电子病历详情") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_electronic_medical_records_details)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_electronic_medical_records_details)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_electronic_medical_records_details)

    @tag("diagnosis")
    @task(1)
    # 前台-今日就诊(全部、已到、未到)统计

    def func_today_seedoctor_reception_statistical(self):
        # self.path_today_seedoctor_reception_statistical =
        # "/api/his/diagnosis/register/page-type-count"

        with self.client.get(
            path=f'{self.host}{self.path_today_seedoctor_reception_statistical}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientSearchKey={self.patientSearchKey}&beginTime={self.beginTimeMillis}&endTime={self.endTimeMillis}&charged={self.charged}&hasCancel={self.hasCancel}&sortName={self.sortName}&sort={self.sort}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="前台-今日就诊(全部、已到、未到)统计") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_seedoctor_reception_statistical)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_seedoctor_reception_statistical)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_today_seedoctor_reception_statistical)





    @tag("diagnosis")
    @task(1)
    # （就诊）诊所资源 列表
    def func_clinic_resources_list(self):
        # self.path_clinic_resources_list =
        # "/api/his/diagnosis/register-resource/list"

        with self.client.get(
            path=f'{self.host}{self.path_clinic_resources_list}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&registerResourceType={self.registerResourceType}',
            headers=None, catch_response=True, name="（就诊）诊所资源 列表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_clinic_resources_list)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_clinic_resources_list)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_clinic_resources_list)

    @tag("diagnosis")
    @task(1)
    # 患者ID 查询就诊记录 or 患者详情 -> 电子病历

    def func_select_electronic_medical_records_patientId(self):
        # self.path_select_electronic_medical_records_patientId =
        # "/api/his/diagnosis/register/list-patient"

        with self.client.get(
            path=f'{self.host}{self.path_select_electronic_medical_records_patientId}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}',
            headers=None, catch_response=True, name="患者ID 查询就诊记录") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_select_electronic_medical_records_patientId)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_electronic_medical_records_patientId)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_electronic_medical_records_patientId)


    @tag("diagnosis")
    @task(1)
    # 查询电子病历列表

    def func_select_electronic_medical_records_list(self):
        # self.path_select_electronic_medical_records_list =
        # "/api/his/diagnosis/medical-record/list"

        with self.client.get(
            path=f'{self.host}{self.path_select_electronic_medical_records_list}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}',
            headers=None, catch_response=True, name="查询电子病历列表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_select_electronic_medical_records_list)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_select_electronic_medical_records_list)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_select_electronic_medical_records_list)




    @tag("diagnosis")
    @task(1)
    # 查询患者就诊次数

    def func_select_see_doctor_count(self):
        # self.path_select_see_doctor_count =
        # "/api/his/diagnosis/register/list-patient/count"

        with self.client.get(
            path=f'{self.host}{self.path_select_see_doctor_count}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}&currentInstitution={self.currentInstitution}',
            headers=None, catch_response=True, name="查询患者就诊次数") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_select_see_doctor_count)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_select_see_doctor_count)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_select_see_doctor_count)

    @tag("billing_demo")
    @task(1)
    # 收费单打印

    def func_bill_print(self):
        # self.path_bill_print =
        # "/api/his/billing/pay/order/select"

        with self.client.get(
            path=f'{self.host}{self.path_bill_print}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&paySerialNos={self.paySerialNos}',
            headers=None, catch_response=True, name="收费单打印") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_bill_print)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_bill_print)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_bill_print)





    @tag("billing_demo")
    @task(1)
    # 查询机构已收费列表 or 【今日工作】 -> 【已收费】

    def func_today_has_charge_list(self):
        # self.path_today_has_charge_list =
        # "/api/his/billing/bill/order/institution/pay-success-order-page"

        with self.client.get(
            path=f'{self.host}{self.path_today_has_charge_list}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&createTimeStart={self.beginTimeMillis}&createTimeEnd={self.endTimeMillis}&charged={self.charged}&patientMessage={self.patientMessage}&sortName={self.sortName}&sort={self.sort}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="查询机构已收费列表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_today_has_charge_list)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_today_has_charge_list)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_today_has_charge_list)




    @tag("billing_demo")
    @task(1)
    # 子账单复制明细列表

    def func_copy_bill(self):
        # self.path_copy_bill =
        # "/api/his/billing/bill/order/copy"

        with self.client.get(
            path=f'{self.host}{self.path_copy_bill}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&billSerialNo={self.billSerialNo_ordinary}',
            headers=None, catch_response=True, name="子账单复制明细列表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_copy_bill)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_copy_bill)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_copy_bill)


    @tag("billing_demo")
    @task(1)
    # 收欠费 3.6.0新接口

    def func_charge_and_owe(self):
        # self.path_charge_and_owe =
        # "/api/his/billing/bill/order/pay-debt"

        with self.client.get(
            path=f'{self.host}{self.path_charge_and_owe}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}&billSerialNo={self.billSerialNo_cao}',
            headers=None, catch_response=True, name="收欠费 3.6.0新接口") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_charge_and_owe)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_charge_and_owe)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_charge_and_owe)






    @tag("billing_demo")
    @task(1)
    # 三合一收费计算优惠 @3.6.0新接口

    def func_calculation_of_preferential(self):
        # self.path_calculation_of_preferential =
        # "/api/his/billing/bill/order/pay-one/calc-promotion"
        payload_data ={
            "billType": 1,
            "cashierStaffId": 2279,
            "cashierTime": 1618285261227,
            "mainOrderDiscount": 100,
            "mainOrderDiscountIsMember": False,
            "receivableAmount": 3333,
            "payChannelList": [
                {
                    "paymentAmount": 3333,
                    "transactionChannelId": 178
                }
            ],
            "orderPayItemList": [
                {
                    "pageSerialNo": 1,
                    "salesList": [

                    ],
                    "deductSign": True,
                    "allBillDiscount": False,
                    "isSingleDiscount": False,
                    "singleDiscountLimit": 0,
                    "itemCode": "8791270195514",
                    "itemName": "肛拭子1C",
                    "itemNum": 1,
                    "itemType": 5,
                    "parentItemCode": 0,
                    "singleDiscount": 100,
                    "totalAmount": 3333,
                    "singleDiscountAfterAmount": 3333,
                    "receivableAmount": 3333,
                    "unitAmount": 3333,
                    "unit": "单位A_1"
                }
            ],
            "salesList": [

            ],
            "promotionVOList": [

            ],
            "mainDiscountPromotionAmount": 0,
            "patientId": self.patientId
        }

        with self.client.post(
            path=f'{self.host}{self.path_calculation_of_preferential}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=self.headers, data=json.dumps(payload_data) ,catch_response=True, name="三合一收费计算优惠 @3.6.0新接口") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_calculation_of_preferential)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_calculation_of_preferential)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_calculation_of_preferential)




    @tag("billing_demo")
    @task(1)
    # 收欠费计算优惠 3.6.0新接口

    def func_calculation_of_preferential_cao(self):
        # self.path_calculation_of_preferential_cao =
        # "/api/his/billing/bill/order/pay-debt/calc-promotion"
        payload_data ={
    "cashierStaffId":2279,
    "cashierTime":1618297120102,
    "mainOrderDiscountIsMember":False,
    "receivableAmount":5,
    "payChannelList":[
        {
            "transactionChannelId":178,
            "paymentAmount":5
        }
    ],
    "orderPayItemList":[

    ],
    "salesList":[

    ],
    "promotionVOList":[

    ],
    "patientId":self.patientId,
    "debtDiscount":100,
    "billOrderVOList":[
        {
            "billFistPayTime":1617107982000,
            "billOrderId":643054,
            "billSerialNo":"BO553202103300012",
            "billType":1,
            "customerId":self.customerId,
            "debtAmount":5,
            "medicalInstitutionName":"李俊测试直营机构3-简称李俊hmaf",
            "orderItemVOList":[
                {
                    "allBillDiscount":True,
                    "billOrderId":643054,
                    "billOrderItemId":1167021,
                    "billSerialNo":"BO553202103300012",
                    "deductSign":False,
                    "isSingleDiscount":True,
                    "itemCode":"I202007180003",
                    "itemId":60,
                    "itemName":"西药",
                    "itemNum":1,
                    "itemType":13,
                    "pageSerialNo":"1167021",
                    "paymentAmount":21,
                    "promotionAmount":0,
                    "receivableAmount":5,
                    "refundAmount":0,
                    "singleDiscountAfterAmount":0,
                    "totalAmount":26,
                    "unit":"盒",
                    "unitAmount":26
                }
            ],
            "patientId":self.patientId,
            "patientName":"新能",
            "paymentAmount":21,
            "promotionAmount":0,
            "receiptAmount":21,
            "receivableAmount":26,
            "refundAmount":0,
            "totalAmount":26
        }
    ]
}

        with self.client.post(
            path=f'{self.host}{self.path_calculation_of_preferential_cao}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=self.headers, data=json.dumps(payload_data) ,catch_response=True, name="收欠费计算优惠 3.6.0新接口") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_calculation_of_preferential_cao)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_calculation_of_preferential_cao)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_calculation_of_preferential_cao)






    @tag("billing_demo")
    @task(1)
    # 查询待处理账单明细 @3.6.0新接口

    def func_select_processed_bill_detail(self):
        # self.path_select_processed_bill_detail =
        # "/api/his/billing/bill/order/wait"

        with self.client.get(
            path=f'{self.host}{self.path_select_processed_bill_detail}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&billSerialNo={self.billSerialNo_processed}',
            headers=None, catch_response=True, name="查询待处理账单明细 @3.6.0新接口") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_select_processed_bill_detail)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_select_processed_bill_detail)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_select_processed_bill_detail)





    @tag("billing_demo_1")
    @task(1)
    # 保存账单或编辑账单 @3.6.0新接口

    def func_saveOrUpdate_bill(self):
        # self.path_saveOrUpdate_bill =
        # "/api/his/billing/bill/order/saveOrUpdate"
        payload_data = {
    "billType":1,
    "cashierStaffId":2279,
    "cashierTime":1618298243731,
    "mainOrderDiscount":100,
    "mainOrderDiscountIsMember":False,
    "memo":"locust",
    "receivableAmount":3333,
    "payChannelList":[
        {
            "paymentAmount":3333,
            "transactionChannelId":178
        }
    ],
    "orderPayItemList":[
        {
            "pageSerialNo":1,
            "salesList":[

            ],
            "deductSign":True,
            "allBillDiscount":False,
            "isSingleDiscount":False,
            "singleDiscountLimit":0,
            "itemCode":"8791270195514",
            "itemName":"肛拭子1C",
            "itemNum":1,
            "itemType":5,
            "parentItemCode":0,
            "singleDiscount":100,
            "totalAmount":3333,
            "singleDiscountAfterAmount":3333,
            "receivableAmount":3333,
            "unitAmount":3333,
            "unit":"单位A_1"
        }
    ],
    "salesList":[

    ],
    "promotionVOList":[

    ],
    "mainDiscountPromotionAmount":0,
    "patientId":self.patientId
}

        with self.client.post(
            path=f'{self.host}{self.path_saveOrUpdate_bill}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=self.headers, data=json.dumps(payload_data) ,catch_response=True, name="保存账单或编辑账单 @3.6.0新接口") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_saveOrUpdate_bill)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_saveOrUpdate_bill)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_saveOrUpdate_bill)




    @tag("billing_demo")
    @task(1)
    # 三合一收费 @3.6.0新接口

    def func_triad_charge(self):
        # self.path_triad_charge =
        # "/api/his/billing/bill/order/pay-one"
        payload_data = {
    "billType":1,
    "cashierStaffId":2279,
    "cashierTime":1618299286795,
    "mainOrderDiscount":100,
    "mainOrderDiscountIsMember":False,
    "receivableAmount":3333,
    "payChannelList":[
        {
            "paymentAmount":3333,
            "transactionChannelId":178
        }
    ],
    "orderPayItemList":[
        {
            "pageSerialNo":1,
            "salesList":[

            ],
            "deductSign":True,
            "allBillDiscount":False,
            "isSingleDiscount":False,
            "singleDiscountLimit":0,
            "itemCode":"8791270195514",
            "itemName":"肛拭子1C",
            "itemNum":1,
            "itemType":5,
            "parentItemCode":0,
            "singleDiscount":100,
            "totalAmount":3333,
            "singleDiscountAfterAmount":3333,
            "receivableAmount":3333,
            "unitAmount":3333,
            "unit":"单位A_1"
        }
    ],
    "salesList":[

    ],
    "promotionVOList":[

    ],
    "mainDiscountPromotionAmount":0,
    "patientId":self.patientId
}

        with self.client.post(
            path=f'{self.host}{self.path_triad_charge}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=self.headers, data=json.dumps(payload_data) ,catch_response=True, name="三合一收费 @3.6.0新接口") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_triad_charge)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_triad_charge)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_triad_charge)





    @tag("billing_demo")
    @task(1)
    # 查询已收费账单明细 @3.6.0新接口

    def func_select_has_charge_detail(self):
        # self.path_select_has_charge_detail =
        # "/api/his/billing/bill/order/item"

        with self.client.get(
            path=f'{self.host}{self.path_select_has_charge_detail}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&billSerialNo={self.billSerialNo_has_charge}',
            headers=None, catch_response=True, name="查询已收费账单明细 @3.6.0新接口") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_select_has_charge_detail)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_select_has_charge_detail)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_select_has_charge_detail)





    @tag("billing_demo")
    @task(1)
    # 待处理账单列表

    def func_Pending_bill_list(self):
        # self.path_Pending_bill_list =
        # "/api/his/billing/bill/order/process/list"

        with self.client.get(
            path=f'{self.host}{self.path_Pending_bill_list}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}&customerId={self.customerId}',
            headers=None, catch_response=True, name="待处理账单列表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_Pending_bill_list)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_Pending_bill_list)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_Pending_bill_list)



    @tag("billing_demo")
    @task(1)
    # 账单列表

    def func_bill_list(self):
        # self.path_bill_list =
        # "/api/his/billing/bill/order/page"

        with self.client.get(
            path=f'{self.host}{self.path_bill_list}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}&customerId={self.customerId}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="账单列表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_bill_list)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_bill_list)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_bill_list)






    @tag("billing_demo")
    @task(1)
    # 机构收费列表

    def func_institution_charge_list(self):
        # self.path_institution_charge_list =
        # "/api/his/billing/bill/order/institution/page"

        with self.client.get(
            path=f'{self.host}{self.path_institution_charge_list}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&createTimeStart={self.beginTimeMillis}&createTimeEnd={self.endTimeMillis}&billStatus={self.billStatus}&charged={self.charged}&patientMessage={self.patientMessage}&sortName={self.sortName}&sort={self.sort}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="查询机构已收费列表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_institution_charge_list)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_institution_charge_list)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_institution_charge_list)




    @tag("billing_demo")
    @task(1)
    # 收费项目下拉列表搜索查询
    def func_select_charge_project_list(self):

        # self.path_select_charge_project_list =
        # "/api/his/billing/settings/charge-item/select-list/fuzzy"

        with self.client.get(
            path=f'{self.host}{self.path_select_charge_project_list}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&searchValue={self.searchValue}',
            headers=None, catch_response=True,name="收费项目下拉列表搜索查询") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_charge_project_list)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_charge_project_list)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_charge_project_list)





    @tag("billing_demo")
    @task(1)
    # 查询收费套餐类型类目列表(三级列表)
    def func_select_package_type(self):

        # self.path_select_package_type =
        # "/api/his/billing/settings/charge-package-type/category-list"

        with self.client.get(
            path=f'{self.host}{self.path_select_package_type}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="查询收费套餐类型类目列表(三级列表)") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_package_type)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_package_type)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_package_type)



    @tag("billing_demo")
    @task(1)
    # 根据收费套餐类型ID查询套餐项目明细
    def func_select_package_detail_by_typeid(self):

        # self.path_select_package_detail_by_typeid =
        # "/api/his/billing/settings/charge-package-item/selectByTypeId"

        with self.client.get(
            path=f'{self.host}{self.path_select_package_detail_by_typeid}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&settingsChargePackageTypeId={self.settingsChargePackageTypeId}',
            headers=None, catch_response=True,name="根据收费套餐类型ID查询套餐项目明细") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_package_detail_by_typeid)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_package_detail_by_typeid)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_package_detail_by_typeid)






    @tag("billing_demo")
    @task(1)
    # 收费套餐项目列表
    def func_charge_package_list(self):

        # self.path_charge_package_list =
        # "/api/his/billing/settings/charge-package-item/select"

        with self.client.get(
            path=f'{self.host}{self.path_charge_package_list}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&settingsChargePackageTypeId={self.settingsChargePackageTypeId}',
            headers=None, catch_response=True,name="收费套餐项目列表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_charge_package_list)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_charge_package_list)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_charge_package_list)




    @tag("billing_demo")
    @task(1)
    # 优惠券列表 @3.6.0新接口
    def func_coupons_list(self):

        # self.path_coupons_list =
        # "/api/his/billing/new/coupon/select-coupon-list-by-user-id"

        with self.client.get(
            path=f'{self.host}{self.path_coupons_list}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&customerId={self.customerId}',
            headers=None, catch_response=True,name="优惠券列表 @3.6.0新接口") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_coupons_list)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_coupons_list)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_coupons_list)



    @tag("billing_demo")
    @task(1)
    # 发券

    def func_create_promotion(self):
        # self.path_create_promotion =
        # "/api/his/billing/promotion/create"

        payload_data = {
            "couponDefinitionId": 1093,
            "memo": "locust" + self.tag_str,
            "patientId": self.patientId,
            "customerId": self.customerId,
            "chargeWay": 1
        }
        with self.client.post(
            path=f'{self.host}{self.path_create_promotion}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=self.headers, data=json.dumps(payload_data) ,catch_response=True, name="发券") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_create_promotion)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_create_promotion)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_create_promotion)




    @tag("patient")
    @task(1)
    # 报表中心-报表下载 分页/列表数据

    def func_stat_filerecord_page(self):
        # self.path_stat_filerecord_page =
        # "/api/his/patient/stat/filerecord/page"

        with self.client.get(
            path=f'{self.host}{self.path_stat_filerecord_page}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&fileName={self.fileName}&createStartDate={self.beginTimeMillis}&createEndDate={self.endTimeMillis}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="报表中心-报表下载 分页/列表数据") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_stat_filerecord_page)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_stat_filerecord_page)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_stat_filerecord_page)





    @tag("patient")
    @task(1)
    # 查询医嘱二级词条
    def func_select_doctor_advice_entry(self):

        # self.path_select_doctor_advice_entry =
        # "/api/his/patient/settings/medical-record/doctor-advice-dict/select/secondLevel"

        with self.client.get(
            path=f'{self.host}{self.path_select_doctor_advice_entry}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="查询医嘱二级词条") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_doctor_advice_entry)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_doctor_advice_entry)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_doctor_advice_entry)





    @tag("patient")
    @task(1)
    # 查询处置二级词条
    def func_select_disposal_entry(self):

        # self.path_select_disposal_entry =
        # "/api/his/patient/settings/medical-record/dispose-dict/select/secondLevel"

        with self.client.get(
            path=f'{self.host}{self.path_select_disposal_entry}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="查询处置二级词条") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_disposal_entry)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_disposal_entry)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_disposal_entry)



    @tag("patient")
    @task(1)
    # 查询既往史二级词条
    def func_select_past_illness_history_entry(self):

        # self.path_select_past_illness_history_entry =
        # "/api/his/patient/settings/medical-record/past-illness-history-dict/select/secondLevel"

        with self.client.get(
            path=f'{self.host}{self.path_select_past_illness_history_entry}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="查询既往史二级词条") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_past_illness_history_entry)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_past_illness_history_entry)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_past_illness_history_entry)





    @tag("patient")
    @task(1)
    # 查询主诉二级词条
    def func_select_chief_complaint_entry(self):

        # self.path_select_chief_complaint_entry =
        # "/api/his/patient/settings/medical-record/chief-complaint-dict/select/secondLevel"

        with self.client.get(
            path=f'{self.host}{self.path_select_chief_complaint_entry}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="查询主诉二级词条") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_chief_complaint_entry)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_chief_complaint_entry)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_chief_complaint_entry)




    @tag("patient")
    @task(1)
    # 查询现病史二级词条
    def func_select_present_illness_history_entry(self):

        # self.path_select_present_illness_history_entry =
        # "/api/his/patient/settings/medical-record/present-illness-history-dict/select/secondLevel"

        with self.client.get(
            path=f'{self.host}{self.path_select_present_illness_history_entry}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="查询现病史二级词条") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_present_illness_history_entry)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_present_illness_history_entry)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_present_illness_history_entry)



    @tag("patient")
    @task(1)
    # 查询检查二级词条
    def func_select_examination_entry(self):

        # self.path_select_examination_entry =
        # "/api/his/patient/settings/medical-record/examination-dict/select/secondLevel"

        with self.client.get(
            path=f'{self.host}{self.path_select_examination_entry}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="查询检查二级词条") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_examination_entry)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_examination_entry)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_examination_entry)




    @tag("patient")
    @task(1)
    # 查询治疗计划二级词条
    def func_select_treatment_plan_entry(self):

        # self.path_select_treatment_plan_entry =
        # "/api/his/patient/settings/medical-record/treatment-plan-dict/select/secondLevel"

        with self.client.get(
            path=f'{self.host}{self.path_select_treatment_plan_entry}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="查询治疗计划二级词条") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_treatment_plan_entry)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_treatment_plan_entry)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_treatment_plan_entry)



    @tag("patient")
    @task(1)
    # 根据患者id查询初诊信息
    def func_first_visit_info(self):

        # self.path_first_visit_info =
        # "/api/his/patient/patient/first-visit/info"

        with self.client.get(
            path=f'{self.host}{self.path_first_visit_info}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}',
            headers=None, catch_response=True,name="根据患者id查询初诊信息") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_first_visit_info)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_first_visit_info)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_first_visit_info)





    @tag("patient")
    @task(1)
    # 查询所有患者来源
    def func_patient_source_list_all(self):

        # self.path_patient_source_list_all =
        # "/api/his/patient/settings/patient/source/list/all"

        with self.client.get(
            path=f'{self.host}{self.path_patient_source_list_all}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}',
            headers=None, catch_response=True,name="查询所有患者来源") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_patient_source_list_all)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_patient_source_list_all)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_patient_source_list_all)





    @tag("patient")
    @task(1)
    # 该患者是否绑定过粉丝, true 已经绑定过 false 未绑定过
    def func_has_bind(self):

        # self.path_has_bind =
        # "/api/his/patient/official-account/has-bind"

        with self.client.get(
            path=f'{self.host}{self.path_has_bind}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}',
            headers=None, catch_response=True,name="该患者是否绑定过粉丝, true 已经绑定过 false 未绑定过") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_has_bind)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_has_bind)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_has_bind)




    @tag("patient")
    @task(1)
    # 查询病例模板类型
    def func_select_medical_record_template_type(self):

        # self.path_select_medical_record_template_type =
        # "/api/his/patient/settings/medical-record/template-type/select"

        with self.client.get(
            path=f'{self.host}{self.path_select_medical_record_template_type}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="查询病例模板类型") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_medical_record_template_type)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_medical_record_template_type)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_medical_record_template_type)




    @tag("patient")
    @task(1)
    # 患者类型列表
    def func_patient_type_list(self):

        # self.path_patient_type_list =
        # "/api/his/patient/settings/type/list/regular"

        with self.client.get(
            path=f'{self.host}{self.path_patient_type_list}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&medicalInstitutionId={self.medicalInstitutionId}',
            headers=None, catch_response=True,name="患者类型列表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_patient_type_list)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_patient_type_list)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_patient_type_list)





    @tag("patient")
    @task(1)
    # 机构下全部患者数量
    def func_patient_count_mtId(self):

        # self.path_patient_count_mtId =
        # "/api/his/patient/patient/patient-count"

        with self.client.get(
            path=f'{self.host}{self.path_patient_count_mtId}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="机构下全部患者数量") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_patient_count_mtId)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_patient_count_mtId)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_patient_count_mtId)




    @tag("patient")
    @task(1)
    # 全身检查列表展示
    def func_body_check_one(self):

        # self.path_body_check_one =
        # "/api/his/patient/body-check/one"

        with self.client.get(
            path=f'{self.host}{self.path_body_check_one}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}',
            headers=None, catch_response=True,name="全身检查列表展示") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_body_check_one)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_body_check_one)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_body_check_one)




    @tag("patient")
    @task(1)
    # 获取患者序列号
    def func_obtain_patient_serial_num(self):

        # self.path_obtain_patient_serial_num =
        # "/api/his/patient/serial/medical-record/serial"

        with self.client.get(
            path=f'{self.host}{self.path_obtain_patient_serial_num}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=5&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientType={self.patientType}',
            headers=None, catch_response=True,name="获取患者序列号") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_obtain_patient_serial_num)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_obtain_patient_serial_num)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_obtain_patient_serial_num)





    @tag("patient")
    @task(1)
    # 查询病例号规则列表
    def func_select_medical_record_num_rules(self):

        # self.path_select_medical_record_num_rules =
        # "/api/his/patient/serial/medical-record/list"

        with self.client.get(
            path=f'{self.host}{self.path_select_medical_record_num_rules}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=5&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="查询病例号规则列表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_medical_record_num_rules)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_medical_record_num_rules)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_medical_record_num_rules)





    @tag("patient")
    @task(1)
    # 分页/列表数据(包含详细) or 营收报表 -> 预约日报表

    def func_appointment_day_report(self):
        # self.path_appointment_day_report =
        # "/api/his/patient/stat/operating/appointment-analysis/page"

        with self.client.get(
            path=f'{self.host}{self.path_appointment_day_report}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&appointmentStartDate={self.beginTimeMillis}&appointmentEndDate={self.endTimeMillis}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="分页/列表数据(包含详细) or 营收报表 -> 预约日报表") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_appointment_day_report)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_appointment_day_report)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_appointment_day_report)




    @tag("patient")
    @task(1)
    # 客户关系列表展示
    def func_customer_relationship(self):

        # self.path_customer_relationship =
        # "/api/his/patient/customer/relation/one"

        with self.client.get(
            path=f'{self.host}{self.path_customer_relationship}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}',
            headers=None, catch_response=True,name="客户关系列表展示:/api/his/patient/customer/relation/one") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_customer_relationship)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_customer_relationship)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_customer_relationship)






    @tag("patient")
    @task(1)
    # 通过机构id查询所有客户标签/患者画像
    def func_all_patient_tags(self):

        # self.path_all_patient_tags =
        # "/api/his/patient/patient/list/patient-tags"

        with self.client.get(
            path=f'{self.host}{self.path_all_patient_tags}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="通过机构id查询所有客户标签/患者画像:/api/his/patient/patient/list/patient-tags") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_all_patient_tags)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_all_patient_tags)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_all_patient_tags)



    @tag("patient_1")
    @task(1)
    # 编辑回访

    def func_update_visit(self):
        # self.path_update_visit =
        # "/api/his/patient/return/visit/update"


        payload_data = {
            "customerReturnVisitId": 19605,
            "visitStatus": 3,
            "planVisitComment": "locust_" + self.tag_str,
            "planVisitTime": "2021-04-14T01:00:00.000Z",
            "planVisitorId": 2279,
            "planVisitorName": "李俊",
            "visitType": 2
        }
        with self.client.post(
            path=f'{self.host}{self.path_update_visit}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=self.headers, data=json.dumps(payload_data) ,catch_response=True, name="编辑回访:/api/his/patient/return/visit/update") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_update_visit)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_update_visit)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_update_visit)



    @tag("patient")
    @task(1)
    # 患者回访记录页面

    def func_select_visit_record(self):
        # self.path_select_visit_record =
        # "/api/his/patient/return/visit/patient/page"

        with self.client.get(
            path=f'{self.host}{self.path_select_visit_record}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&patientId={self.patientId}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="患者回访记录页面：/api/his/patient/return/visit/patient/page") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_select_visit_record)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_select_visit_record)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_select_visit_record)


    @tag("patient")
    @task(1)
    # 更新病例号规则

    def func_update_case_num_rules(self):
        # self.path_update_case_num_rules =
        # "/api/his/patient/serial/medical-record/update"

        payload_data = {
            "serialConfigId": 14,
            "systemInner": 1,
            "patientType": 16,
            "patientTypeName": "临时",
            "prefix": "FG" + self.tag_str,
            "cycleType": 4,
            "serialLength": 5,
            "startValue": 1,
            "cycleClear": 0
        }
        with self.client.post(
            path=f'{self.host}{self.path_update_case_num_rules}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=5&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=self.headers, data=json.dumps(payload_data) ,catch_response=True, name="更新病例号规则:/api/his/patient/serial/medical-record/update") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_update_case_num_rules)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_update_case_num_rules)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_update_case_num_rules)




    @tag("patient")
    @task(1)
    # 报表中心-运营报表-就诊周期分析 分页/列表数据

    def func_stat_operating_diagnosis(self):
        # self.path_stat_operating_diagnosis =
        # "/api/his/patient/stat/operating/diagnosis-period/page"

        with self.client.get(
            path=f'{self.host}{self.path_stat_operating_diagnosis}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&diagnosisStartDate={self.beginTimeMillis}&diagnosisEndDate={self.endTimeMillis}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="报表中心-运营报表-就诊周期分析 分页/列表数据:/api/his/patient/stat/operating/diagnosis-period/page") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_stat_operating_diagnosis)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_stat_operating_diagnosis)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_stat_operating_diagnosis)





    @tag("patient")
    @task(1)
    # 客户回访页面:客户回访分页查询

    def func_return_visit_customer_page(self):
        # self.path_return_visit_customer_page =
        # "/api/his/patient/return/visit/customer/page"

        with self.client.get(
            path=f'{self.host}{self.path_return_visit_customer_page}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&customerInfo={self.customerInfo}&visitStatus={self.visitStatus}&planVisitStartTime={self.planVisitStartTime}&planVisitEndTime={self.planVisitEndTime}&sortName={self.sortName}&sort={self.p_sort}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="客户回访页面:客户回访分页查询:/api/his/patient/return/visit/customer/page") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_return_visit_customer_page)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_return_visit_customer_page)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_return_visit_customer_page)





    @tag("patient")
    @task(1)
    # 预约分检分页查询

    def func_institution_check(self):
        # self.path_institution_check =
        # "/api/his/patient/institution/check/page"

        with self.client.get(
            path=f'{self.host}{self.path_institution_check}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&condition={self.condition}&temperatureStartDate={self.planVisitStartTime}&temperatureEndDate={self.planVisitEndTime}&judgement={self.judgement}&temperature={self.temperature}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="# 预约分检分页查询:/api/his/patient/institution/check/page") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_institution_check)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_institution_check)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_institution_check)






    @tag("patient")
    @task(1)
    # 回访详情
    def func_return_visit_detail(self):

        # self.path_return_visit_detail =
        # "/api/his/patient/return/visit/detail"

        with self.client.get(
            path=f'{self.host}{self.path_return_visit_detail}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&returnVisitId={self.returnVisitId}',
            headers=None, catch_response=True,name="回访详情:/api/his/patient/return/visit/detail") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_return_visit_detail)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_return_visit_detail)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_return_visit_detail)




    @tag("patient")
    @task(1)
    # 获取选择的地单子病历模板
    def func_select_get_record_template(self):

        # self.path_select_get_record_template =
        # "/api/his/patient/settings/medical-record/get-select-patient-record-template"

        with self.client.get(
            path=f'{self.host}{self.path_select_get_record_template}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN',
            headers=None, catch_response=True,name="获取选择的地单子病历模板:/api/his/patient/settings/medical-record/get-select-patient-record-template") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_get_record_template)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_get_record_template)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_get_record_template)






    @tag("patient")
    @task(1)
    # 根据生日分页查询患者列表

    def func_select_birthday_reminder(self):
        # self.path_select_birthday_reminder =
        # "/api/his/patient/patient/page/birthday-reminder"

        with self.client.get(
            path=f'{self.host}{self.path_select_birthday_reminder}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&birthdayAmount={self.birthdayAmount}&birthdayBegin={self.birthdayBegin}&birthdayEnd={self.birthdayEnd}&charged={self.charged}&sortName={self.sortName}&sort={self.sort}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="根据生日分页查询患者列表：/api/his/patient/patient/page/birthday-reminder") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_birthday_reminder)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_birthday_reminder)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_birthday_reminder)





    @tag("patient")
    @task(1)
    # 根据患者名称、拼音、手机号模糊查询患者
    def func_fuzzy_query_patient(self):

        # self.path_fuzzy_query_patient =
        # "/api/his/patient/patient/v2/home/list/regular"

        with self.client.get(
            path=f'{self.host}{self.path_fuzzy_query_patient}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=5&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&regularParam={self.regularParam}',
            headers=None, catch_response=True,name="根据患者名称、拼音、手机号模糊查询患者:/api/his/patient/patient/v2/home/list/regular") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_fuzzy_query_patient)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_fuzzy_query_patient)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_fuzzy_query_patient)




    @tag("patient")
    @task(1)
    # 根据机构id查询今日扫码患者数量

    def func_select_today_scan_patient(self):

        # self.path_select_today_scan_patient =
        # "/api/his/patient/patient/today-scan/page"

        with self.client.get(
            path=f'{self.host}{self.path_select_today_scan_patient}?_token={self.token}&_uid={self.uid}&_ut=1&_t=1&_s=11&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang=zh_CN&sortName={self.sortName}&sort={self.sort}&current={self.current}&size={self.size}',
            headers=None, catch_response=True, name="根据机构id查询今日扫码患者数量:/api/his/patient/patient/today-scan/page") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_today_scan_patient)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_today_scan_patient)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_select_today_scan_patient)




    @tag("patient_demo1")
    @task(1)
    # 新增患者

    def func_create_patient(self):
        # self.path_create_patient =
        # "/api/his/patient/patient/create/with/patient-contact"

        patient_num = random.randint(1000000000000,9999999999999)

        payload_data = {
            "patientName": "locust" + fake.password(length=6),
            "gender": 1,
            "settingsTypeId": 27,
            "birthday": "",
            "fixedTelephone": "",
            "settingsPatientSourceId": "",
            "sourceValue": "",
            "certificatesNo": "",
            "memo": f"FG_{patient_num}",
            "nickName": "",
            "isFamilyDecision": 2,
            "responsibleDoctorStaffId": "",
            "exclusiveCSStaffId": "",
            "firstDiagnosisMilliSecond": "",
            "firstVisitDoctorId": "",
            "nationality": "",
            "medicalInsuranceCardNo": "",
            "medicalRecordNo": patient_num,
            "patientNo": patient_num,
            "tagIds": 1011960,
            "patientContactStr":[{"contactLabel":-1,"address":""}],
            "certificates": 1,
            "_uid": self.uid,
            "_token": self.token,
            "_ut": 1,
            "_t": 1,
            "_s":5,
            "_lang":"zh_CN",
            "_mtId":553,
            "_cmtType":2,
            "_tenantId": 376,
            "_cmtId": 546
        }
        with self.client.post(
            path=f'{self.host}{self.path_create_patient}',
            headers=None, data=payload_data,catch_response=True, name="新增患者:/api/his/patient/patient/create/with/patient-contact") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                              self.path_create_patient)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_create_patient)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_create_patient)



    @tag("patient_demo1")
    @task(1)
    # 编辑患者

    def func_update_patient(self):
        # self.path_update_patient =
        # "/api/his/patient/patient/update/with/patient-contact"

        patient_num = random.randint(15400000000,15499999999)

        payload_data = {

        "_token":self.token,
        "_uid":self.uid,
        "_ut":1,
        "_t":1,
        "_s":11,
        "_mtId":self.mtId,
        "_tenantId":self.tenantId,
        "_cmtId":self.cmtId,
        "_cmtType": self.cmtType,
        "_lang": "zh_CN",
        "archive": False,
        "arrearsFlag": True,
        "birthday": "",
        "certificates": 1,
        "createStaffId": 2279,
        "customerId": self.customerId,
        "firstVisitDoctorId":"",
        "gender":2,
        "institutionChainType":2,
        "isFamilyDecision":2,
        "isMember":1,
        "isMemberExpire":False,
        "isShareMember":False,
        "isShowMemberVip":1,
        "medicalInstitutionId": self.medicalInstitutionId,
        "medicalRecordNo": 2021033000213,
        "memberCardNo": "ZY55320210330024895",
        "memberCardShortName": "VIP12",
        "memberId": 92843,
        "patientId": self.patientId,
        "patientName": "新能",
        "patientNo": 2021033000213,
        "settingsTypeId":27,
        "settingsTypeName":"患者类型",
        "mobile": patient_num,
        "visType":2,
        "patientContactStr":[{"contactLabel":-1,"mobile":patient_num,"patientContactsId":400919,"province":150000,"city":150300,"area":150303}],
        "memo":"locust_update" ,
        "firstDiagnosisMilliSecond":1618325803000
        }
        with self.client.post(
            path=f'{self.host}{self.path_update_patient}',
            headers=None, data=payload_data,catch_response=True, name="编辑患者:/api/his/patient/patient/update/with/patient-contact") as res:
            if res.status_code == 200:

                if (json.loads(res.text))["code"] == 0:
                    res.success()
                else:
                    res.failure(res.text)
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                          self.path_update_patient)

            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------",
                      self.path_update_patient)


if __name__ == "__main__":
    import os
    """
    @tag修饰符主要是用例管理测试方法的执行，在测试方法上加上一个或者多个@tag修饰符，就可以在执行测试时通过@tag修饰符运行指定测试集合，而且它不会影响全局的任务收集。

    在执行测试时，使用 -T 或者 -E 来挑选测试集合

    -T 选中的集合

    -E 排除选中的集合
    """

    # os模块执行系统命令，相当于在cmd切换到当前脚本目录，执行locust -f locust_login.py
    #os.system("locust -f locust_demo1.py --web-host=127.0.0.1")
    # os.system("locust -f locust_h5.py --host=http://localhost")
    os.system("locust -f locust_h5.py --host=http://localhost -T billing_demo_1")

    #os.system("locust -f locust_zadan.py --host=192.168.90.164")


       # 单机分布式
       # 先启动一个master节点，mater节点不执行任务
        #
        # locust -f locustfile.py --master
        # 开多个窗口，启动多个slave节点，比如我开四个窗口，依次执行以下命令
        #
        # locust - f locustfile.py -- worke


#     """
#     @tag修饰符主要是用例管理测试方法的执行，在测试方法上加上一个或者多个@tag修饰符，就可以在执行测试时通过@tag修饰符运行指定测试集合，而且它不会影响全局的任务收集。
#
#     在执行测试时，使用 -T 或者 -E 来挑选测试集合
#
#     -T 选中的集合
#
#     -E 排除选中的集合
#     """

    # os模块执行系统命令，相当于在cmd切换到当前脚本目录，执行locust -f locust_login.py
    #os.system("locust -f locust_demo1.py --web-host=127.0.0.1")
    #os.system("locust -f locust_pre_demo.py --host=http://localhost")


    #os.system("locust -f locust_zadan.py --host=192.168.90.164")


       # 单机分布式
       # 先启动一个master节点，mater节点不执行任务
        #
        # locust -f locustfile.py --master
        # 开多个窗口，启动多个slave节点，比如我开四个窗口，依次执行以下命令
        #
        # locust -f locustfile.py --worke