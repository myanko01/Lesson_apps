from .calc import calculate_account_billing

""" 仕様書の請求一覧の請求金額を計算するファイル。
    集計したデータをリストに格納して返す。
"""


class Billing:
    def __init__(self, account_id, account_name):  # 引数 Accountの account.id, account.name
        self.account_id = account_id
        self.account_name = account_name
        self.genre_name_set = set()
        self.genre_names = ""
        self.genre_num = 0
        self.attend_num = 0
        self.total_billing = 0

    def add_lesson(self, lesson):
        self.attend_num += 1
        if lesson.genre.name not in self.genre_name_set:
            self.genre_num += 1
        self.genre_name_set.add(lesson.genre.name)


class Aggregator:
    def __init__(self):
        self.result_list = []

    def get_monthly_billings(self, accounts, lesson_log_list, lesson_dict):  # accounts=Account.objects.all()
        for account in accounts:
            billing = Billing(account.id, account.name)
            self.result_list.append(billing)  # Billing格納

        # .values_listでタプルのリストとして返すがTrueにより、一つの値、つまりリストとして返される。.distinct()重複避け
        # 年月、account,genre(Lessonモデル)が入っている(lesson_log_lis)
        # ①
        target_account_ids = lesson_log_list.values_list("account", flat=True).distinct()

        # 一人{1(id): lesson_log}
        target_account_dict = {}
        for lesson_log in lesson_log_list:
            target_account_dict.setdefault(lesson_log.account.id, [])
            target_account_dict[lesson_log.account.id].append(lesson_log)

        # ①
        for account_id in target_account_ids:
            for billing in self.result_list:
                # Account,Lessonモデルのidを比較
                if billing.account_id == account_id:
                    for lesson_log in target_account_dict[account_id]:
                        billing.add_lesson(lesson_log)
                    # account_id には idが入っている ①(2つ)でidになった？
                    billing.total_billing = calculate_account_billing(account_id, lesson_log_list, lesson_dict)

        return self.result_list
