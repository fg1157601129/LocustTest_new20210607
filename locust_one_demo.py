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
h = {
    'Host': 'power.medcloud.cn',
    'Cookie': '',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'origin': 'https://power.medcloud.cn',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': "",
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

# 随机生成3-10个中文字符
def nickname_random():
    nick_name = ""
    for i in range(random.randint(3,10)):
        val = chr(random.randint(0x4e00, 0x9fbf))
        nick_name += val
    return nick_name


# token = 'd6eba7a8-0492-41ce-a402-93ea11cbf1fd'


class MyUser(FastHttpUser):
    wait_time = between(1,2)


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
        self.host = "https://pre-power.medcloud.cn"   # 被测主机地址
        self.token = "073740b54da6405a977b5fc6ece63824"
        self.uid = 2681
        self.mtId = 665
        self.tenantId = 452
        self.cmtId = 625
        self.cmtType = 2
        self.tag_str = fake.password(length=6)




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
        self.payerId = 33203    # 切换环境需要变更
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
        self.medicalInstitutionId = 665   # 切换环境需调整
        self.purchaseTotalAmount = ""
        self.beginTimeMillis = "1618243200000"
        self.endTimeMillis = int(time.time()*1000)
        self.createStaffId = self.uid   # 值 同 self.uid = 2681
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
        self.patientId = 33203  # 切换环境需要变更

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
        self.medicalRecordId = 25998    # 切换环境需调整

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
        self.billSerialNo_ordinary = "BO665202103300008"

        # 收欠费 3.6.0新接口
        self.path_charge_and_owe = "/api/his/billing/bill/order/pay-debt"
        self.billSerialNo_cao = "BO665202103300009"

        # 三合一收费计算优惠 @3.6.0新接口
        self.path_calculation_of_preferential = "/api/his/billing/bill/order/pay-one/calc-promotion"

        # 收欠费计算优惠 3.6.0新接口
        self.path_calculation_of_preferential_cao = "/api/his/billing/bill/order/pay-debt/calc-promotion"

        # 查询待处理账单明细 @3.6.0新接口
        self.path_select_processed_bill_detail = "/api/his/billing/bill/order/wait"
        self.billSerialNo_processed = "BO665202103300003"

        # 保存账单或编辑账单 @3.6.0新接口
        self.path_saveOrUpdate_bill = "/api/his/billing/bill/order/saveOrUpdate"

        # 三合一收费 @3.6.0新接口
        self.path_triad_charge = "/api/his/billing/bill/order/pay-one"

        # 查询已收费账单明细 @3.6.0新接口
        self.path_select_has_charge_detail = "/api/his/billing/bill/order/item"
        self.billSerialNo_has_charge = "BO665202104080003"

        # 待处理账单列表
        self.path_Pending_bill_list = "/api/his/billing/bill/order/process/list"
        self.customerId = 1415211

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
        self.settingsChargePackageTypeId = 60

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
        self.customerInfo = ""
        self.visitStatus = 3
        self.planVisitStartTime = "2020-04-01+00:00:00"
        self.planVisitEndTime = "2021-04-19 23:59:59"
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
        self.returnVisitId = 21732

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

        #

        self.headers = {
            'Host': "pre-power.medcloud.cn",
            'Cookie': f'_token={self.token}; _token={self.token}; _refreshToken={self.token}; _tenantId={self.tenantId}; _topParentId=546; _institutionChainType=2; DENTAIL_USER_ID={self.uid}; DENTAL_MEDICAL_INSTITUTION_ID={self.mtId}',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8',
            'origin': "https://pre-power.medcloud.cn",
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': '',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }




    #   可以按照 每个不同的服务，打上tag ；以下是 pay 模块

    @tag("physical_1")
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















# if __name__ == "__main__":
#     import os

    #os.system("locust -f locust_pre_demo.py --host=http://localhost")
    #os.system("locust -f locust_pre_demo.py --host=http://localhost -T physical_1")
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
        # locust - f locustfile.py -- worke

