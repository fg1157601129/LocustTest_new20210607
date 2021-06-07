# -*- coding: utf-8 -*-

# @File    : KelaEnum.py
# @Date    : 2019-09-23-15:40
# @Author  : DanKeGeGe
# @Version : 1
from enum import Enum


class UrlEnum(Enum):
    # KELA_CLUB_WEB = 'https://api.imkela.com/club-api'  # 俱乐部模块
    # KELA_MCMS_WEB = 'https://api.imkela.com/mcms-api'  # 其他服务
    # KELA_REDPACK_WEB = 'https://api.imkela.com/redpacket-api'  # 红包模块
    # KELA_REPORT_WEB = 'https://api.imkela.com/report-api'  # 报表模块
    # KELA_THIRD_WEB = 'https://api.imkela.com/thrid-api'  # 第三方服务
    # KELA_TRADE_WEB = 'https://api.imkela.com/trade-api'  # 资金交易模块
    # KELA_USER_WEB = 'https://api.imkela.com/user-api'  # 用户模块


    KELA_CLUB_WEB = 'https://devapi.imkela.com/club-api'  # 俱乐部模块
    KELA_MCMS_WEB = 'https://devapi.imkela.com/mcms-api'  # 其他服务
    KELA_REDPACK_WEB = 'https://devapi.imkela.com/redpacket-api'  # 红包模块
    KELA_REPORT_WEB = 'https://devapi.imkela.com/report-api'  # 报表模块
    KELA_THIRD_WEB = 'https://devapi.imkela.com/thrid-api'  # 第三方服务
    KELA_TRADE_WEB = 'https://devapi.imkela.com/trade-api'  # 资金交易模块
    KELA_USER_WEB = 'https://devapi.imkela.com/user-api'  # 用户模块
