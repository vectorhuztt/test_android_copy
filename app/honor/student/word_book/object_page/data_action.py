import datetime
from functools import reduce

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.user_center.object_page.user_Info_page import UserInfoPage
from app.honor.student.word_book.object_page.wordbook_sql import WordBookSql
from conf.base_page import BasePage
from conf.decorator import teststep


class WordBookDataHandle(BasePage):
    """数据操作类"""
    def __init__(self):
        self.mysql = WordBookSql()
        self.home = HomePage()
        self.user_info = UserInfoPage()


    @teststep
    def get_word_by_explain(self, explain):
        """根据翻译从数据库中获取单词
           若获取的单词可能为多个,则与数据库中的单词作比较
        """
        if ';' in explain:  # 解释拆分 对于有多个解释的单词，采用;前第一个解释
            explain = explain.split(';')[0]
        if '.' in explain:
            exp_list = explain.split('.')
            prop = exp_list[0] + '.'
            exp = exp_list[1].strip()
            english = self.mysql.find_word_by_explain(prop, exp)
        else:
            english = self.mysql.find_word_by_explain_no_prop(explain)
        word = [english[0][0]] if len(english) == 1 else [x[0] for x in english]
        return word

    @teststep
    def get_change_date(self, num):
        """为数据库提供修改日期"""
        now = datetime.datetime.now()
        word_date = (now + datetime.timedelta(days=-num)).strftime("%Y-%m-%d %H:%M:%S")
        record_date = (now + datetime.timedelta(days=-2)).strftime("%Y-%m-%d %H:%M:%S")
        print('单词时间：', word_date)
        print('去重时间：', record_date)
        return word_date, record_date

    @teststep
    def change_word_date(self, stu_id,  level, time_interval):
        date = self.get_change_date(time_interval)  # 获取修改的时间
        print("LEVEL：", level)
        self.mysql.update_word_date(str(date[0]), stu_id, level)
        self.mysql.update_word_record(str(date[1]), stu_id)  # 单词去重，更改record的create时间

    @teststep
    def get_all_word_homework_ids(self, stu_id):
        """获取标签id"""
        word_homework_list = self.mysql.find_book_label(stu_id)
        word_homework = [x[0] for x in word_homework_list]
        return word_homework

    @teststep
    def get_word_homework_name(self, word_homework_id):
        """获取标签名称"""
        name = self.mysql.find_word_homework_name(word_homework_id)
        return name[0][0]

    @teststep
    def get_word_homework_id_by_name(self, word_homework_name):
        """根据作业名称获取id"""
        homework_id = self.mysql.find_homework_id_by_name(word_homework_name)
        return homework_id[0][0]

    @teststep
    def get_student_label_id_by_homework_id(self, stu_id, homework_id):
        """根据作业id查找label id"""
        label_id = self.mysql.find_label_id_by_homework_id(stu_id, homework_id)
        return label_id[0][0]

    @teststep
    def get_wordbank_by_label_id(self, label_id):
        """根据label id 获取单词"""
        words = self.mysql.find_wordbank_by_label_id(label_id)
        word_list = words[0][0].split(',')
        return word_list

    @teststep
    def get_words_count(self, stu_id, word_homework_id):
        """获取单词总数 与一轮 三轮单词数"""
        result = self.mysql.find_word_by_label(stu_id, word_homework_id)
        first_count = []
        third_count = []
        for i in range(len(result)):
            if result[i][1] >= 1:
                first_count.append(i)
            if result[i][1] >= 3:
                third_count.append(i)
        return len(first_count), len(third_count)

    @teststep
    def get_word_by_sentence(self, sentence_exp):
        word = self.mysql.find_word_by_sentence_exp(sentence_exp)
        return [x[0] for x in word]

    @teststep
    def get_star_words(self, stu_id):
        """获取标星单词"""
        star_ids = self.mysql.find_star_word_id(stu_id)
        star_list = [self.mysql.find_word_by_id(s_id)[0][0] for s_id in star_ids]
        return star_list

    @teststep
    def get_familiar_words(self, stu_id):
        """获取标熟单词"""
        familiar_ids = self.mysql.find_familiar_word_id(stu_id)
        familiar_list = [self.mysql.find_word_by_id(f_id)[0][0] for f_id in familiar_ids]
        return familiar_list

    @teststep
    def get_word_level(self, stu_id, word):
        """获取单词的熟练度"""
        level = self.mysql.find_word_level(stu_id, word)
        return int(level)

    @teststep
    def change_play_times(self, stu_id):
        """更改练习次数"""
        self.mysql.update_play_times(stu_id)

    @teststep
    def change_today_word_count(self, stu_id):
        """更改今日练习词数"""
        self.mysql.update_today_word_count(stu_id)

    @teststep
    def change_today_new_count(self, stu_id):
        """更改今日新词数"""
        self.mysql.update_today_new_count(stu_id)

    @teststep
    def delete_all_word_data(self, stu_id):
        """删除所有star数据"""
        self.mysql.delete_all_star(stu_id)
        # 删除所有score数据
        self.mysql.delete_all_score(stu_id)
        # 删除用户所有单词数据
        self.mysql.delete_all_word(stu_id)
        # 删除所有去重记录
        self.mysql.delete_all_record(stu_id)
        # 删除所有标星标熟记录
        self.mysql.delete_fluency_flag(stu_id)


    @teststep
    def get_need_recite_count(self, stu_id, level):
        """获取需要复习的单词数"""
        words = self.mysql.find_range_fluency(stu_id, level)
        return len(words)

    @teststep
    def change_new_word_level(self, stu_id, before, after):
        """更改熟练度"""
        self.mysql.update_level_zero(stu_id, before, after)

    @teststep
    def get_different_level_words(self, stu_id, level):
        """获取新词个数"""
        words = self.mysql.find_word_different_level(stu_id, level)
        return len(words)

    @teststep
    def get_student_word(self, stu_id):
        """获取学生单词 单词按照布置时间逆序获取"""
        all_word = {}
        teacher_label_id = self.mysql.find_teacher_word_label_id(stu_id)  # 老师布置的单词作业id 按时间逆序排列
        system_label_id = self.mysql.find_system_word_label_id(stu_id)    # 系统单词id

        teacher_homework_bank = [self.mysql.find_word_by_label_id(x[0]) for x in teacher_label_id]  # 根据作业id获取label_id
        system_homework_bank = [self.mysql.find_word_by_label_id(x[0]) for x in system_label_id]

        all_word['老师'] = self.get_word_and_explain_by_group(teacher_homework_bank)
        all_word['系统'] = self.get_word_and_explain_by_group(system_homework_bank)
        return all_word

    @teststep
    def get_word_and_explain_by_group(self, stu_id, label_homework_bank):
        bank_id_list = [x[0][0].split(',') for x in label_homework_bank]  # 获取对用label下的单词id(content)
        for i in range(len(bank_id_list)):      # 单词去重
            B = []
            list(map(lambda x: B.extend(x), bank_id_list[:i]))    # 获取当前位置前面多个label的单词
            set_B = list(set(B))                                  # 去重
            similar = [x for x in bank_id_list[i] if x in set_B]  # 获取当前label与前面所有label相同的单词
            for y in similar:
                bank_id_list[i].remove(y)   # 移除相同单词

        student_word_list = []
        for x in bank_id_list:
            if len(x) == 1:
                student_word_list.append(self.mysql.find_student_not_set_word_eql_id(stu_id, x[0]))
            else:
                student_word_list.append(self.mysql.find_student_not_set_word_in_ids(stu_id, tuple(x)))

        word_explain_list = []
        for i in range(len(student_word_list)):
            group_word = {}
            for y in student_word_list[i]:
                explain = self.mysql.find_student_word_and_explain(y)[0][0]
                word = self.mysql.find_student_word_and_explain(y)[0][1]
                group_word[explain] = word
            word_explain_list.append(group_word)
        return word_explain_list

    @teststep
    def get_all_word_count(self, student_all_words):
        all_word = reduce(lambda x, y: x+y, [len(y.values()) for x in student_all_words for y in student_all_words[x]])
        return all_word

    @teststep
    def change_teacher_word_group(self, student_all_words):
        teacher_words = student_all_words['老师']
        system_words = student_all_words['系统']
        change_words = []
        while True:
            if len(teacher_words) > 1:
                if len(set(teacher_words[0].values())) < 10:
                    teacher_words[1] = dict(teacher_words[0], **teacher_words[1])
                    change_words.append(teacher_words[0])
                    teacher_words.remove(teacher_words[0])
                else:
                    break
            else:
                break

        if len(set(teacher_words[0].values())) < 3:
            system_words[0] = dict(teacher_words[0], ** system_words[0])
            change_words.append(teacher_words[0])
            teacher_words.remove(teacher_words[0])

        return change_words

    @teststep
    def remove_studied_word(self, after_game_new_words, student_all_words):
        """移除已学单词"""
        print(after_game_new_words)
        print(student_all_words)
        after_new_word_keys = [y for x in list(after_game_new_words.values()) for y in x]
        t_k = [(x, i, n) for x in student_all_words for i, j in enumerate(student_all_words[x])
               for m, n in enumerate(j) if n in after_new_word_keys]

        for x in t_k:
            print('移除已练单词：', x)
            del student_all_words[x[0]][x[1]][x[2]]
