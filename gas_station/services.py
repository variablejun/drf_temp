from rest_framework.common.entity import FileDTO
from rest_framework.common.services import Reader, Printer, Scraper
import pandas as pd
import numpy as np
from sklearn import preprocessing
import folium
from glob import glob
import re

class Service():

    def __init__(self):
        self.file = FileDTO()
        self.reader = Reader()
        self.printer = Printer()
        self.scraper = Scraper()

    def get_url(self):
        file = self.file
        reader = self.reader
        printer = self.printer
        scraper = self.scraper
        file.url = 'https://www.opinet.co.kr/searRgSelect.do'
        driver = scraper.driver()
        print(driver.get(file.url))

        gu_list_raw = driver.find_element_by_xpath("""//*[@id="coolbeat"]""")
        gu_list = gu_list_raw.find_elements_by_tag_name("option")
        gu_names = [option.get_attribute("value") for option in gu_list]
        gu_names.remove("")
        print(gu_names)

    def gas_station_price_info(self):
        file = self.file
        reader = self.reader
        printer = self.printer
        # print(glob('./data/지역_위치별*xls'))
        station_files = glob('./data/지역_위치별*xls')
        tmp_raw = []
        for i in station_files:
            t = pd.read_excel(i, header=2)
            tmp_raw.append(t)
        station_raw = pd.concat(tmp_raw)
        station_raw.info()
        '''
        print("*"*100)
        print(station_raw.head(2))
        print(station_raw.tail(2))
        '''
        stations = pd.DataFrame({'Oil_store': station_raw['상호'],
                                 '주소': station_raw['주소'],
                                 '가격': station_raw['휘발유'],
                                 '셀프': station_raw['셀프여부'],
                                 '상표': station_raw['상표']})

        # print(stations.head())
        stations['구'] = [i.split()[1] for i in stations['주소']]
        stations['구'].unique()
        # print(stations[stations['구']=='서울특별시'])
        # 12  SK네트웍스(주)효진주유소  1 서울특별시 성동구 동일로 129 (성수동2가)  1654  N  SK에너지  서울특별시
        stations[stations['구'] == '서울특별시'] = '성동구'
        stations['구'].unique()
        # print(stations[stations['구'] == '특별시'])
        # 10     서현주유소  서울 특별시 도봉구 방학로 142 (방학동)  1524  Y  S-OIL  특별시
        stations[stations['구'] == '특별시'] = '도봉구'
        stations['구'].unique()
        # print(stations[stations['가격'] == '-'])
        '''
        18  명진석유(주)동서울주유소  서울특별시 강동구  천호대로 1456 (상일동)  -  Y  GS칼텍스   강동구
        33          하나주유소   서울특별시 영등포구  도림로 236 (신길동)  -  N  S-OIL  영등포구
        12   (주)에이앤이청담주유소    서울특별시 강북구 도봉로 155  (미아동)  -  Y  SK에너지   강북구
        13          송정주유소    서울특별시 강북구 인수봉로 185 (수유동)  -  N   자가상표   강북구
        '''
        stations = stations[stations['가격'] != '-']
        # print(stations[stations['가격'] == '성동구'])
        # 12       성동구  성동구  성동구  성동구  성동구  성동구
        p = re.compile('^[0-9]+$')
        temp_stations = []
        for i in stations:
            if p.match(stations['가격'][i]):
                temp_stations.append(stations['가격'][i])
        stations['가격'] = [float(i) for i in temp_stations]
        stations.reset_index(inplace=True)
        del stations['index']
        printer.dframe(stations)


if __name__ == '__main__':
    s = Service()
    s.gas_station_price_info()


