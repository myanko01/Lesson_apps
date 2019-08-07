def calculate_account_billing(account_id, lesson_log_list, genre_dict):
    # 英語
    english_lesson = genre_dict["英語"]

    english_histories = []
    for lesson_log in lesson_log_list:
        if lesson_log.account.id == account_id and lesson_log.genre.name == "英語":
            english_histories.append(lesson_log)

    total_attending_hour = 0
    for english in english_histories:
        total_attending_hour += english.attending_hour
    if total_attending_hour:
        total_english_billing = english_lesson.basic_rate + total_attending_hour * 3500
    else:
        total_english_billing = 0

    # ファイナンス
    finance_lesson = genre_dict["ファイナンス"]
    finance_histories = []
    for lesson_log in lesson_log_list:
        if lesson_log.account.id == account_id and lesson_log.genre.name == "ファイナンス":
            finance_histories.append(lesson_log)

    total_attending_hour = 0
    for finance in finance_histories:
        total_attending_hour += finance.attending_hour
    if total_attending_hour:
        if 20 > total_attending_hour:
            total_finance_billing = finance_lesson.basic_rate + total_attending_hour * 3300

        elif 50 > total_attending_hour >= 20:
            total_finance_billing = 3300 * 20 + 2800 * (total_attending_hour - 20)
        elif total_attending_hour >= 50:
            total_finance_billing = 3300 * 20 + 2500 * 30 + 2500 * (total_attending_hour - 50)
    else:
        total_finance_billing = 0

    # プログラミング
    programming_lesson = genre_dict["プログラミング"]
    programming_histories = []
    for lesson_log in lesson_log_list:
        if lesson_log.account.id == account_id and lesson_log.genre.name == "プログラミング":
            programming_histories.append(lesson_log)

    total_attending_hour = 0
    for programming in programming_histories:
        total_attending_hour += programming.attending_hour
    if total_attending_hour:
        if total_attending_hour < 5:
            total_programming_billing = programming_lesson.basic_rate
        elif 20 > total_attending_hour >= 5:
            total_programming_billing = programming_lesson.basic_rate + 3500 * (total_attending_hour - 5)
        elif 35 > total_attending_hour >= 20:
            total_programming_billing = programming_lesson.basic_rate + 0 * 5 + 3500 * 15 + 3000 * (
                        total_attending_hour - 20)
        elif 50 > total_attending_hour >= 35:
            total_programming_billing = programming_lesson.basic_rate + 0 * 5 + 3500 * 15 + 2800 * 15 + 2800 * (
                        total_attending_hour - 35)
        elif total_attending_hour >= 50:
            total_programming_billing = programming_lesson.basic_rate + 0 * 5 + 3500 * 15 + 2800 * 15 + 2500 * 15 + 2500 * (
                        total_attending_hour - 50)
    else:
        total_programming_billing = 0

    return total_english_billing + total_finance_billing + total_programming_billing
