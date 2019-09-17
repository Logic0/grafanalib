#!/usr/local/bin/python3
#-*- coding:utf-8
from grafanalib.core import *
import sys

DATASOURCE = "Prometheus-CLB"

def generate_graph( title :str, expr :str, alias :str, type :str ):
    global DATASOURCE
    fmt = SHORT_FORMAT
    Y_Max = None
    if( type == "amount" ):                          # 数量型视图
        fmt = SHORT_FORMAT
    elif( type == "rate" ):                          # 比例型视图
        fmt = PERCENT_100_FORMAT                     # 这里用的是自定义的[0,100]区间的百分比
        Y_Max = 100
    else:
        fmt = SHORT_FORMAT
    return Graph( title=title,
                  dataSource=DATASOURCE,
                  targets=[ Target( expr=expr,
                                    legendFormat=alias,
                                    refId='A',),
                  ],
                  yAxes=single_y_axis(format=fmt, max=Y_Max),
                  nullPointMode = NULL_AS_ZERO,
                )

# 属性文件采用四级方式组织属性名
# 主功能--子功能--统计项--属性名, 例如  周边服务--获取天气概览--请求量--xservice_weather_reqnum
# 主功能--子功能--统计项--属性名/属性名, 例如  周边服务--获取天气概览--成功率--xservice_weather_success/xservice_weather_reqnum
def generate_rows( attrfile :str ):
    rows = []
    cnt = 0
    p = []
    for attr in open( attrfile, "r" ).readlines():
        segs = attr.strip().split("--")
        gtype = "amount"
        if( segs[3].find("/") != -1 ):
            l = segs[3].split("/")
            expr = 'sum( increase( %s[5m] ) ) / sum( increase( %s[5m] ) ) * 100' % (l[0], l[1])
            gtype = "rate"
        else:
            expr = 'sum( increase( %s[1m] )  ) ' % segs[3]
            gtype = "amount"
        title = "--".join( segs[0:3] )
        p.append( { "expr": expr, "title": title, "type": gtype } )
        cnt += 1
        if cnt >= 2:
            rows.append( generate_row(p) )
            p.clear()
            cnt = 0
    if cnt != 0:
        rows.append( generate_row( p ) )
    return rows

# generate a row
# param: [{"expr": "", "title": "", "type": ""}, ]
def generate_row( p ):
    return Row( panels = generate_panels( p ) )

def generate_panel( expr :str, title :str, gtype = "amount" ):
    return generate_graph( title, expr, title, gtype )

# param: [{ "expr": "", "title": "", "type": "" }, ]
def generate_panels( p ):
    panels = []
    for i in p:
        panels.append( generate_panel( i["expr"], i["title"], i['type'] ) )
    return panels

def generate_dashborad( title :str, attrfile :str ):
    dashboard = Dashboard( title = title,
                           rows = generate_rows( attrfile ),
                           timezone = "browser",)
    return dashboard

dashboard = generate_dashborad( "dashboard标题", "attr.txt" ).auto_panel_ids()
