from apps.account.consts import CHOICE_GENDER
from apps.billing.calc import calculate_account_billing

""" 仕様書のレポートのジャンルと性別別に、選択年月のレッスン数・受講者数・売り上げ金額を計算、
    ジャンルと年齢層(性別)別に選択年月のレッスン数・受講者数・売り上げ金額を計算するファイル
    (集計)
"""


class ReportRow:
    def __init__(self):
        self.genre_name = ""
        self.gender = None
        self.lesson_num = 0
        self.account_num = 0
        self.sales = 0
        self.age_group = ""

    @property
    def gender_name(self):
        return dict(CHOICE_GENDER)[self.gender]



class ReportAggregator:
    def __init__(self):
        self.result_list = []

    def analye_genre_gender_trend(self, query_dict, genre_dict):
        """ ジャンルと性別別に、選択年月のレッスン数・受講者数・売り上げ金額を計算する関数
            顧客ごとの辞書でまとめて、リスト化して返す
        """

        for genre_name_gender, lesson_list in query_dict.items():
            account_id_set\
                = set()
            for genre_gender_query in lesson_list:
                account_id_set.add(genre_gender_query.account.id)

            report = ReportRow()
            report.genre_name, report.gender = genre_name_gender
            report.lesson_num = len(lesson_list)
            report.account_num = len(account_id_set)

            for account_id in account_id_set:
                report.sales += calculate_account_billing(account_id, lesson_list, genre_dict)

            self.result_list.append(report)
        return self.result_list

    def analye_age_group_gender_trend(self, query_dict, genre_dict):
        """ ジャンルと年齢層(性別)別に選択年月のレッスン数・受講者数・売り上げ金額を計算する関数
            顧客ごとの辞書でまとめて、リスト化して返す
        """

        for genre_name_gender, lesson_list in query_dict.items():

            age_group_dict = {}

            for choice_gender_num in range(1, 9):
                age_group_dict.setdefault(choice_gender_num, [])
                for genre_log in lesson_list:

                    if genre_log.account.age // 10 == choice_gender_num:
                        age_group_dict[choice_gender_num].append(genre_log)

            for choice_gender_num, age_genre_log in age_group_dict.items():
                age_group_id_set = set()

                report = ReportRow()
                report.genre_name, report.gender = genre_name_gender

                report.age_group = str(choice_gender_num) + "0代"

                for age_genre in age_genre_log:
                    age_group_id_set.add(age_genre.account.id)

                report.lesson_num = len(age_genre_log)
                report.account_num = len(age_group_id_set)

                for account_id in age_group_id_set:
                    report.sales += calculate_account_billing(account_id, lesson_list, genre_dict)
                self.result_list.append(report)
        return self.result_list
