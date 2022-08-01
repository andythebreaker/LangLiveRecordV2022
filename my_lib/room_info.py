# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility
#TODO:print debug S/W
from asyncio.windows_events import NULL
from enum import Enum
import re
class Color(Enum):
    live_id = 1
    live_key = 2
    live_url = 3
    hot_val=4
def exe(roominfo,ccc):
    rg =[ r"\"live_id\":\"([a-zA-Z0-9]+)\"",r"\"live_key\":\"([a-zA-Z0-9]+)\"",r"\"live_url\":\"([a-zA-Z0-9]+)\"",r"\"hot_val\":\"([a-zA-Z0-9]+)\""]
    regex=rg[ccc.value-1]
    test_str=roominfo
    #test_str = ("{\"ret_code\":\"0\",\"ret_msg\":\"ok\",\"data\":{\"live_info\":{\"pfid\":3652550,\"pretty_id\":\"3652550\",\"pretty_type\":0,\"headimg\":\"https:\\/\\/assets.lang.live\\/user\\/3652550\\/40a6e3f40122f4ce15e73a0a1ef11b51\",\"nickname\":\"陳詩雅\",\"fans\":6167,\"follow\":42,\"follows\":42,\"anchor_lvl\":40,\"anchor_gid\":2,\"anchor_glvl\":100,\"anchor_tlvl\":1,\"anchor_gtype\":2,\"grade_id\":1,\"grade_lvl\":29,\"ugid\":1,\"uglv\":21,\"birthday\":\"1995-04-24\",\"talent_info\":{\"icon\":\"http:\\/\\/blob.ufile.ucloud.com.cn\\/8033fc537d4e81dacad20572f825ef1d\",\"name\":\"認證: 藝人\",\"user_desc\":\"AKB48 Team TP  \n"
    #    "成員\"},\"isVip\":0,\"vip_lvl\":1,\"lang_vip\":{\"is_vip\":0,\"expire_date\":1639321317,\"expire_ts\":0,\"start_date\":1636642917,\"growth\":0,\"vip_lvl\":1,\"is_open\":1,\"v_type\":1,\"act_st\":0,\"n_time\":1659368723,\"next_growth\":300},\"vip_member_expire_date\":\"2021-12-12 23:01:57\",\"sign\":\"IG➡️chen4ya_akb48teamtp\\nみやび\\nAKB48TeamTP隊長\\nTrust+passion=TeamTP\",\"sex\":2,\"vip_info\":{\"exp:ire\":0,\"exp\":0,\"lvl\":0,\"intimacy\":0,\"ts\":1659368723000,\"vip_fan_nameplate\":{\"content\":\"大胸膛\",\"color\":\"1\"}},\"vip_fans_count\":66,\"rank_month_hide\":1,\"rank_total_hide\":1,\"live_status\":0,\"live_id\":\"P3652550H5GBfkE\",\"live_key\":\"j36Tad\"},\"user_info\":null,\"last_time\":{\"st\":0,\"sec\":0,\"group\":\"3\",\"rank_l\":0,\"rank_n\":0,\"group_name\":\"當紅\",\"distance_l\":0,\"distance_n\":0,\"hourrank\":0},\"top_fight\":{\"st\":0,\"stage\":0,\"sec\":0,\"rank\":0,\"flag\":0,\"distance_l\":0},\"income_day\":269571,\"red_pay_st\":0,\"anchor_diamond_day\":269571,\"sticker_info\":null,\"pendant\":null,\"golden_scholar_pendant_id\":805,\"time_list\":{\"st\":0,\"type\":2,\"sec\":0,\"group_id\":3,\"group_name\":\"潛力組\",\"ts\":1659369600},\"hour_rank\":[],\"lf_type\":0,\"lf_times\":0}}")

    matches = re.finditer(regex, test_str, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        
        print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            
            print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
            return match.group(groupNum)
    # Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
    print("not found anything")
    return NULL