import requests
import html2text

class PropertyExtractor:

    def __init__(self):
        pass

    def extract(self, id: int) -> dict:
        url = "https://www.28hse.com/buy/residential/property-{}".format(id)
        self.id = id
        self.lines = self.__request_page(url)
        self.result = {}
        self.__check_photo_urls()
        self.__cut_main_info_part()
        self.__check_url()
        self.__check_is_agent()
        self.__check_room()
        self.__check_living()
        self.__check_bathroom()
        self.__check_build_area()
        self.__check_real_area()
        self.__check_post_date()
        self.__check_post_update()
        self.__check_price()
        self.__check_address()
        self.__check_estate()
        self.__check_contact()
        if len(self.result) == 1:
            return False
        return self.result
    
    def __request_page(self, url) -> list:
        r = requests.get(url)
        lines = html2text.html2text(r.text).split("\n")
        return lines
    
    def __check_photo_urls(self):
        urls = []
        for line in self.lines:
            if "https://i1.28hse.com/" in line and ".jpg" in line:
                txt = line.split("https://i1.28hse.com/")[1]
                txt = txt.split(".jpg")[0]
                url = "https://i1.28hse.com/" + txt + ".jpg"
                if not url in urls:
                    urls.append(url)
        if len(urls) > 0:
            self.result["photo_urls"] = urls

    def __cut_main_info_part(self):
        newlines = []
        lock = True
        for line in self.lines:
            if line[:10] == "按此直接至聯絡人資料":
                lock = False
            if line == "注意事項":
                break
            if lock == True:
                continue
            newlines.append(line)
    
    def __check_url(self):
        for line in self.lines:
            if line[:6] == "  3. [":
                txt = line.split("(")[1]
                txt = txt.split(")")[0]
                self.result["url"] = txt + "/property-{}".format(self.id)
                txt = txt.split("www.28hse.com/")[1]
                self.result["ad_type"] = txt.split("/")[0]
                self.result["property_type"] = txt.split("/")[1]
                break

    def __is_number(self, txt: str):
        if txt in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "一", "二", "三", "四", "五", "六", "七", "八", "九", "兩"]:
            return True
        return False
    
    def __map_number(self, txt: str) -> str:
        if txt in ["一", "二", "三", "四", "五", "六", "七", "八", "九", "兩"]:
            mapping = {
                "一": 1,
                "二": 2,
                "兩": 2,
                "三": 3,
                "四": 4,
                "五": 5,
                "六": 6,
                "七": 7,
                "八": 8,
                "九": 9
            }
            return mapping[txt]
        return txt

    def __check_is_agent(self):
        for line in self.lines:
            if line[:5] == "物業編號:":
                if "代理" in line:
                    self.result["ad_type"] = "agent"
                    return
            if line[:8] == "地產公司資料":
                self.result["ad_type"] = "agent"
                return
        self.result["ad_type"] = "owner"
    
    def __check_room(self):
        for line in self.lines:
            if "房" in line:
                line = line.replace(" ", "")
                index = line.index("房")
                if self.__is_number(line[index-1]) == True:
                    txt = self.__map_number(line[index-1])
                    self.result["room"] = txt
                    break
    
    def __check_living(self):
        for line in self.lines:
            if "廳" in line:
                line = line.replace(" ", "")
                index = line.index("廳")
                if self.__is_number(line[index-1]) == True:
                    txt = self.__map_number(line[index-1])
                    self.result["living"] = txt
                    break
    
    def __check_bathroom(self):
        for line in self.lines:
            if "廁" in line:
                line = line.replace(" ", "")
                index = line.index("廁")
                if self.__is_number(line[index-1]) == True:
                    txt = self.__map_number(line[index-1])
                    self.result["bathroom"] = txt
                    break
    
    def __check_build_area(self):
        for i in range(len(self.lines)):
            if self.lines[i] == "建築面積 |":
                target = self.lines[i+2]
                txt = ""
                for t in target:
                    if self.__is_number(t) == True:
                        txt += t
                if not txt == "":
                    self.result["build_area"] = txt
                    break
    
    def __check_real_area(self):
        for i in range(len(self.lines)):
            if self.lines[i] == "實用面積 |":
                target = self.lines[i+2]
                txt = ""
                for t in target:
                    if self.__is_number(t) == True:
                        txt += t
                if not txt == "":
                    self.result["real_area"] = txt
                    break
    
    def __check_post_date(self):
        for line in self.lines:
            if "刊登:" in line:
                txts = line.split("刊登:")
                txt = txts[1][:10]
                if not " " in txt and not "|" in txt:
                    self.result["post_date"] = txt
                    break

    def __check_post_update(self):
        for line in self.lines:
            if "更新:" in line:
                txts = line.split("更新:")
                txt = txts[1][:10]
                if not " " in txt and not "|" in txt:
                    self.result["post_update"] = txt
                    break

    def __check_price(self):
        for line in self.lines:
            if "售 $" in line:
                txt = line.replace("售 $", "").replace(" ", "").replace("元", "").replace("萬", "0000").replace(",", "")
                self.result["price"] = txt
                break
            if "租 $" in line:
                txt = line.replace("租 $", "").replace(" ", "").replace("元", "").replace("萬", "0000").replace(",", "")
                self.result["price"] = txt
                break
    
    def __check_address(self):
        for i in range(len(self.lines)):
            if "物業地址 |" in self.lines[i]:
                i2 = i + 2
                address = ""
                while True:
                    txt = self.lines[i2]
                    txt = txt.replace(" ", "")
                    if not txt == "":
                        address += txt
                        i2 += 1
                    else:
                        break
                if not address == "":
                    self.result["address"] = address
                    break
    
    def __check_estate(self):
        for i in range(len(self.lines)):
            if "地區屋苑" in self.lines[i]:
                self.result["estate"] = self.lines[i+2]
                txt = self.lines[i+4]
                txts = txt.split(" ")
                self.result["region"] = txts[0]
                self.result["district"] = txts[1]
                break
    
    def __check_contact(self):
        for i in range(len(self.lines)):
            if self.lines[i] == "### 放盤聯絡人":
                for i2 in range(i, len(self.lines)):
                    if self.lines[i2][:4] == "####":
                        self.result["contact_person"] = self.lines[i2].replace("#### ", "").replace("  __卡片", "").replace("  代理個人簡介", "")
                    if self.lines[i2][:4] == "Tel:":
                        tel = ""
                        for t in reversed(self.lines[i2]):
                            if t in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-"]:
                                tel = t + tel
                            else:
                                break
                        if not tel == "":
                            self.result["contact_phone"] = tel
                            return