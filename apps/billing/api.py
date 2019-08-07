from apps.lesson.models import Genre, Lesson
from apps.account.consts import CHOICE_GENDER


CHOICE_GENDER_dict = dict(CHOICE_GENDER)


def get_genre_data():
    get_genre = {}
    for genre in Genre.objects.all():
        get_genre[genre.name] = genre  # {id:あの塊のgenre}
    return get_genre


def create_target_queryset_dict(billing_year, billing_month):
    """ 事前にクエリを取得(事前に)"""
    target_query_dict = {}

    # 指定年月の受講履歴を取得
    lesson_log_list = Lesson.objects.filter(attending_date__year=billing_year, attending_date__month=billing_month).select_related('account', 'genre')

    # 全ジャンルを取得
    all_genre_name = Genre.objects.values_list("name", flat=True)

    # {ジャンル・性別:[]} 抽出条件:条件に該当するクエリを格納
    for genre_name in all_genre_name:
        for gender in CHOICE_GENDER_dict.keys():
            target_query_dict.setdefault((genre_name, gender), [])

    for lesson_log in lesson_log_list:
        target_query_dict[(lesson_log.genre.name, lesson_log.account.gender)].append(lesson_log)

    return target_query_dict



