#-*- coding:utf-8 -*-

import json


#f = 'data/weibo/69安钢矿粉掺假门717/69安钢矿粉掺假门717.json'


fs = """data/weibo/10雅戈尔水污染/雅戈尔水污染.json
data/weibo/11动车事故/723动车事故.json
data/weibo/12味千拉面骨汤门/味千拉面骨汤门.json
data/weibo/13露笑科技高新企业资质存疑/13露笑科技高新企业资质存疑.json
data/weibo/14紫鑫药业停牌/14紫鑫药业停牌.json
data/weibo/15大连石化又起火灾/15大连石化又起火灾.json
data/weibo/16比亚迪安全气囊不安全/16比亚迪安全气囊不安全.json
data/weibo/17茅台涨价风波/17茅台涨价风波.json
data/weibo/18中华网破产/18中华网破产.json
data/weibo/19中石化漏税门/19中石化漏税门.json
data/weibo/1中石化问题油事件/reposts.json
data/weibo/20中石化漏税门1012/20中石化漏税门1012.json
data/weibo/21中海油环境污染1020/21中海油环境污染1020.json
data/weibo/22健力宝风波/22健力宝风波.json
data/weibo/23电信联通垄断门/23电信联通垄断门.json
data/weibo/24八菱科技关联交易/24八菱科技关联交易.json
data/weibo/25茅台申报奢侈品/25茅台申报奢侈品.json
data/weibo/26中石油路虎车队/26中石油路虎车队.json
data/weibo/27匡威等知名品牌质检上黑榜/27匡威等知名品牌质检上黑榜.json
data/weibo/28soho欠薪门/28soho欠薪门.json
data/weibo/29美的透漏员工社保/29美的透漏员工社保.json
data/weibo/2酷6暴力裁员/reposts.json
data/weibo/30汉王科技立案稽查/30汉王科技立案稽查.json
data/weibo/31茅台经销商捏造涨价信息被罚/31茅台经销商捏造涨价信息被罚.json
data/weibo/32蒙牛纯牛奶检出致癌物质/32蒙牛纯牛奶检出致癌物质.json
data/weibo/33富士康又陷坠楼怪圈/33富士康又陷坠楼怪圈.json
data/weibo/34金龙鱼玉米油/34金龙鱼玉米油.json
data/weibo/35碧生源虚假广告/35碧生源虚假广告.json
data/weibo/37朗玛成创业板IPO失败第一家/37朗玛成创业板IPO失败第一家.json
data/weibo/38五粮液上黑榜/38五粮液上黑榜.json
data/weibo/39苏泊尔质量门再升级/39苏泊尔质量门再升级.json
data/weibo/3雨润过期肉/3雨润过期肉.json
data/weibo/3雨润过期肉/reposts.json
data/weibo/40京客隆购物卡被指缩水/40京客隆购物卡被指缩水.json
data/weibo/41腾讯QQ被注销广东省著名商标/41腾讯QQ被注销广东省著名商标.json
data/weibo/42华晨中华自燃/42华晨中华自燃.json
data/weibo/43攀钢在美被诉/43攀钢在美被诉.json
data/weibo/44思念水饺死苍蝇/44思念水饺死苍蝇.json
data/weibo/45红牛添加剂/45红牛添加剂.json
data/weibo/46万科毒地板/46万科毒地板.json
data/weibo/47茅台高管言论/47茅台高管言论.json
data/weibo/48石化团购奔驰/48石化团购奔驰.json
data/weibo/49万科纸板门/49万科纸板门.json
data/weibo/4哈药污染门/reposts.json
data/weibo/50汤臣倍健铅超标/50汤臣倍健铅超标.json
data/weibo/51中国电信放行垃圾短信/51中国电信放行垃圾短信.json
data/weibo/52富士康违反劳工权益/52富士康违反劳工权益.json
data/weibo/53中石化渗水油/53中石化渗水油.json
data/weibo/54唯品会上市首日破发/54唯品会上市首日破发.json
data/weibo/55茅台葡萄酒侵权/55茅台葡萄酒侵权.json
data/weibo/56如家毛巾门/56如家毛巾门.json
data/weibo/57修正药企等陷入毒胶囊/57修正药企等陷入毒胶囊.json
data/weibo/58王老吉商标案落幕/58王老吉商标案落幕.json
data/weibo/59恰恰陈年瓜子/59恰恰陈年瓜子.json
data/weibo/5骆驼欺诈上市/骆驼欺诈上市.json
data/weibo/60双汇肋排被曝烫出蛆虫/60双汇肋排被曝烫出蛆虫.json
data/weibo/61五粮液机场冠名/61五粮液机场冠名.json
data/weibo/62全聚德废弃鸭油转卖为地沟油/62全聚德废弃鸭油转卖为地沟油.json
data/weibo/63伊利全优奶粉被曝汞含量超标/63伊利全优奶粉被曝汞含量超标.json
data/weibo/64蒙牛代工点被曝脏乱差/64蒙牛代工点被曝脏乱差.json
data/weibo/65光明优倍牛奶混入碱水/65光明优倍牛奶混入碱水.json
data/weibo/66当当被曝出售假表/66当当被曝出售假表.json
data/weibo/67广加王老吉装潢权新纠纷/67广加王老吉装潢权新纠纷.json
data/weibo/68茅台国酒商标引争议/68茅台国酒商标引争议.json
data/weibo/69安钢矿粉掺假门717/69安钢矿粉掺假门717.json
data/weibo/6统一塑化剂危机/统一塑化剂危机.json
data/weibo/70张裕葡萄酒涉嫌农药残留89/70张裕葡萄酒涉嫌农药残留89.json
data/weibo/71旺仔牛奶苍蝇门719/71旺仔牛奶苍蝇门719.json
data/weibo/72汇源商标纠纷案87/72汇源商标纠纷案87.json
data/weibo/73健康元涉嫌地沟油制药829/73健康元涉嫌地沟油制药829.json
data/weibo/74古井贡酒被曝酒精勾兑822/74古井贡酒被曝酒精勾兑822.json
data/weibo/75王老吉加多宝员工群殴事件/75王老吉加多宝员工群殴事件.json
data/weibo/76蒙牛代理商篡改日期/76蒙牛代理商篡改日期.json
data/weibo/77山西汾酒被曝秘密召回827/77山西汾酒被曝秘密召回827.json
data/weibo/78光明牛奶发生酸改/78光明牛奶发生酸改.json
data/weibo/79蒙牛换装遭质疑/79蒙牛换装遭质疑.json
data/weibo/7涪陵天价榨菜/涪陵天价榨菜.json
data/weibo/80光明乳业再陷质量风波/80光明乳业再陷质量风波.json
data/weibo/81民生银行被指霸王条款/81民生银行被指霸王条款.json
data/weibo/82微信密码存在安全漏洞/82微信密码存在安全漏洞.json
data/weibo/9中海油漏油事故/中海油漏油事故.json"""

fs = fs.split('\n')

def get_(f):
    
    #f = 'data/weibo/%s/%s.json' % (name, name)

    data = json.load(open(f,'r'))

    reposts = reduce(lambda z,i: z+i , data.values(), [])

    repost_urls = [i['repost-url'] for i in reposts]
    
    home_urls = ['/'.join(i.split('/')[:-1]) for i in repost_urls]

    return home_urls
