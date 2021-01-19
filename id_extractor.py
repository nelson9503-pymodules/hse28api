from .web_requests import requests_text
import threading


def ExtractID(ids: list, propertyType: str = "rent", numOfThread: int = 32):
    global idlist
    global results
    idlist = ids
    results = {}

    def extract_page():
        global idlist
        global results
        while len(idlist) > 0:
            id = ids.pop()
            url = "https://www.28hse.com/{}-property-{}.html".format(
                propertyType, id)
            lines = requests_text(url).split("\n")
            result = page_parser(lines)
            results[id] = result

    threads = []
    for _ in range(numOfThread):
        threads.append(threading.Thread(target=extract_page))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return results


def page_parser(lines: list) -> dict:
    result = {}  # create dictionary to store results
    for i in range(len(lines)):
        if lines[i][:1] == "#" and "廣告標題" not in result:
            x = lines[i]
            x = x.replace("#", "")
            x = clean_method_removeSpaces(x)
            result["廣告標題"] = x
        elif "28HSE 樓盤編號" in lines[i] and "28HSE編號" not in result:
            x = lines[i]
            x = safe_split_method(x)
            x = clean_method_extractNumbers(x)
            result["28HSE編號"] = int(x)
        elif "樓盤狀態" in lines[i] and "樓盤狀態" not in result:
            x = lines[i]
            x = safe_split_method(x)
            x = clean_method_removeSpaces(x)
            x = x.split(" ")[0]
            result["樓盤狀態"] = x
        elif lines[i][:3] == "出租價" and "價錢" not in result:
            x = lines[i+2]
            x = clean_method_extractNumbers(x)
            result["價錢"] = x
        elif lines[i][:2] == "售價" and "價錢" not in result:
            x = lines[i+2]
            result["價錢"] = x
        elif lines[i][:5] == "座數及單位" and "單位" not in result:
            x = lines[i]
            x = safe_split_method(x)
            x = clean_method_removeSpaces(x)
            result["單位"] = x
        elif lines[i][:2] == "層數" and "層數" not in result:
            x = lines[i]
            x = safe_split_method(x)
            x = clean_method_removeSpaces(x)
            result["層數"] = x
        elif lines[i][:2] == "房間" and "房間" not in result:
            x = lines[i]
            x = safe_split_method(x)
            x = clean_method_removeSpaces(x)
            result["房間"] = x
        elif lines[i][:4] == "建築面積" and "建築面積" not in result:
            x = lines[i]
            x = safe_split_method(x)
            x = clean_method_extractNumbers(x)
            result["建築面積"] = x
        elif lines[i][:4] == "實用面積" and "實用面積" not in result:
            x = lines[i]
            x = safe_split_method(x)
            x = clean_method_extractNumbers(x)
            result["實用面積"] = x
        elif lines[i][:4] == "物業地址" and "物業地址" not in result:
            x = lines[i+2]
            x = clean_method_removeSpaces(x)
            result["物業地址"] = x
        elif lines[i][:6] == "刊登或續期日" and "刊登或續期日" not in result:
            x = lines[i]
            x = safe_split_method(x)
            x = clean_method_removeSpaces(x)
            result["刊登或續期日"] = x.replace(".", "-")
        elif lines[i][:5] == "放盤到期日" and "放盤到期日" not in result:
            x = lines[i]
            x = safe_split_method(x)
            x = clean_method_removeSpaces(x)
            result["放盤到期日"] = x
        elif lines[i][:4] == "單位特色" and "租務類型" not in result:
            # 租務類型
            i2 = i + 2
            x = lines[i2]
            x = clean_method_removeSpaces(x)
            result["租務類型"] = x.replace(" ", ",")
            # 地區, 屋苑大廈
            i2 += 2
            x = lines[i2]
            x = clean_method_removeSpaces(x)
            x = x.split(" ")
            result["地區"] = x[0]
            result["屋苑大廈"] = x[1]
            # 描述標題
            i2 += 2
            x = lines[i2]
            x = clean_method_removeSpaces(x)
            result["描述標題"] = x
            # 描述內容
            i2 += 2
            x = ""
            while not lines[i2] == "聯絡方法":
                line = lines[i2]
                line = clean_method_removeSpaces(line)
                if not line in [" ", "\n", " \n ", " \n", "\n "]:
                    x += line + "\n"
                i2 += 1
            result["描述內容"] = x
        elif lines[i][:4] == "聯絡方法" and "聯絡方法" not in result:
            i2 = i + 1
            x = ""
            while not "溫馨提示" in lines[i2]:
                line = lines[i2]
                line = clean_method_removeSpaces(line)
                if not line in [" ", "\n", " \n ", " \n", "\n "]:
                    x += line + "\n"
                i2 += 1
            while "![](" in x:
                y = x.split("![](", 1)
                x = y[0] + y[1].split(")", 1)[1]
            while "(http" in x:
                y = x.split("(http", 1)
                x = y[0] + y[1].split(")", 1)[1]
            result["聯絡方法"] = x
        elif lines[i][:5] == "會員留言板" and "photolinks" not in result:
            i2, links = i, []
            while not "你可能有興趣的樓盤" in lines[i2]:
                if "* [![  ]" in lines[i2]:
                    x = lines[i2].split("(")[1]
                    x = x.split(")")[0].replace(" ", "")
                    links.append(x)
                i2 += 1
            result["photolinks"] = links
    return result


def clean_method_removeSpaces(x: str) -> str:
    """
    1. remove duoble spaces: "  " -> " "
    2. remove space at position 1
    3. remove space at position -1
    """
    while "  " in x:
        x = x.replace("  ", " ")
    while len(x) > 0 and x[0] == " ":
        x = x[1:]
    while len(x) > 0 and x[-1] == " ":
        x = x[:-1]
    return x


def clean_method_extractNumbers(x: str) -> float:
    """
    1. remove $
    2. remove ,
    3. remove spaces
    4. try float(x) and return it
    5. if fail, return ""
    """
    if "![]" in x:
        x = x.split("![]")[0]
    x = x.replace("$", "")
    x = x.replace(",", "")
    x = x.replace(" ", "")
    try:
        x = float(x)
    except:
        x = ""
    return x


def safe_split_method(x: str) -> str:
    """
    This method split the |,
    and try to get values from right side.
    """
    x = x.split("|", 1)
    if len(x) > 1:
        return x[1]
    else:
        return ""
