from flask import render_template, redirect, url_for
from flask.views import MethodView

import requests
import declxml as xml


class MedicationOpenAPI(MethodView):
    def __init__(self, template):
        self.template = template

    def get(self):
        med_processor = xml.dictionary('response', [
            xml.dictionary('header', [
                xml.string('resultCode'),
                xml.string('resultMsg')
            ]),
            xml.dictionary('body', [
                xml.integer('numOfRows'),
                xml.integer('pageNo'),
                xml.integer('totalCount'),
                xml.dictionary('items', [
                    xml.array(xml.dictionary('item', [
                        xml.string('INGR_ENG_NAME'),
                        xml.string('INGR_KOR_NAME'),
                        xml.string('ITEM_NAME_ENG'),
                        xml.string('ITEM_NAME_KOR'),
                        xml.string('SELLING_CORP'),
                        xml.string('DOSAGE_FORM'),
                        xml.string('STRENGTH'),
                        xml.string('GROUPING_NO'),
                        xml.string('PMS_EXP_DATE'),
                        xml.string('KOR_SUIT_YN')
                    ]))
                ])
            ])
        ])
        med_api = requests.get('http://apis.data.go.kr/1470000/'
                                'MdcinPatentInfoService/'
                                'getMdcinPatentInfoList?'
                                'serviceKey=j1p%2FEIuaPbMKsRuWzOMygNZKwyo2LYZzAWWBwZwxFLc%2BTzuRHN8ROyeJYje%2FPEvs7Hsp6OCVK1fQFt5UcaTocA%3D%3D&'
                                'pageNo=1&startPage=1&numOfRows=100&pageSize=100')
        med_xml = med_api.text
        med_dict = xml.parse_from_string(med_processor, med_xml)
        items = med_dict['body']['items']['item']
        return render_template(self.template, items=items)