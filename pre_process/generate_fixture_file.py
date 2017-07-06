import json
import re


def main():
    input_file = input("Enter the json file you want to modify: ")
    shop_list = []
    comment_list = []
    with open(input_file, 'r') as fin:
        shop_list = json.load(fin)

    shop_model = input("Enter shop model's path(e.g. app_name.model): ")
    comment_model = input("Enter comment model's path: ")
    for shop in shop_list:
        shop_fields = {}
        for key, value in shop.items():
            if key == 'shopurl':
                continue
            elif key == 'tel' and not value:
                shop_fields['tel'] = ""
            elif key == 'avgcost':
                avgcost = re.findall(r'\d+', value)
                if len(avgcost) > 0:
                    shop_fields['avgcost'] = int(avgcost[0])
                else:
                    shop_fields['avgcost'] = 0
            elif key == 'ID':
                shop_fields['urlID'] = value
            elif not key == 'comments':
                shop_fields[key] = value
            else:
                comment_list_temp = value
                for comment_temp in comment_list_temp:
                    comment_fields = {}
                    if not comment_temp:
                        comment_fields['content'] = ""
                    else:
                        comment_fields['content'] = "".join(re.compile(u"[\u4e00-\u9fa5A\w，。！？：\"\",.!?\"\"\'\']+").findall(comment_temp))
                    comment_fields['shop'] = [shop['ID']]
                    comment_fields['user'] = ['大众点评网友']  # all comments captured from web belongs to the user named '匿名用户'
                    comment_fields['username'] = '大众点评网友'
                    comment  = {}
                    comment['model'] = comment_model
                    comment['fields'] = comment_fields
                    comment_list.append(comment)
        shop.clear()
        shop['fields'] = shop_fields
        shop['model'] = shop_model
    shops_output_file = input("Enter the json file of shops you want to output to: ")
    with open(shops_output_file, 'w') as sfout:
        json.dump(shop_list, sfout)
    comments_output_file = input("Enter the json file of comments you want to output to: ")
    with open(comments_output_file, 'w') as cfout:
        json.dump(comment_list, cfout)

    print("OK.")

main()