# -*- coding:utf-8 -*-
# author: lkz
# date: 2015/06/19 13:44

import datetime
from functools import partial
from bson import ObjectId

from flask import url_for

from xiaoli.models.account import Account
from xiaoli.models.translation_task import TranslationTask
from xiaoli.models.translation_result import TransSuggestion

from xiaoli.utils.format_data import format_time


def get_user_trans_lang_pair(user_id):
    if isinstance(user_id, Account):
        user_id = user_id._id

    if isinstance(user_id, str):
        user_id = ObjectId(user_id)

    user_id_str = str(user_id)

    tasks_user_in, _ = get_user_tasks(user_id)

    lang_pair_list = set()

    for task in tasks_user_in:
        for lang_pair in task.translators:

            translators = task.translators.get(lang_pair)
            translator = translators.get(user_id_str)

            if not translator:
                continue

            lang_pair_list.add(lang_pair)

        for lang_pair in task.proofreaders:
            proofreaders = task.proofreaders.get(lang_pair)
            proofreader = proofreaders.get(user_id_str)

            if not proofreader:
                continue

            lang_pair_list.add(lang_pair)

    return list(lang_pair_list)


def get_user_tasks(user_id, page=None, per_page=None, **kwargs):
    if isinstance(user_id, Account):
        user_id = user_id._id

    if isinstance(user_id, str):
        user_id = ObjectId(user_id)

    query_filter = {
        'member': user_id
    }

    kwargs and query_filter.update(kwargs)

    tasks_query = TranslationTask.m.find(query_filter).sort([("create_time", -1)])

    if page:
        offset = (page - 1) * per_page
        tasks_query = tasks_query.limit(per_page).skip(offset)

    total_count = tasks_query.count()
    tasks = tasks_query.all()

    return tasks, total_count


def get_user_step_tasks(user_id):
    """
    列出:今天，明天，本周，其他时间要完成的任务
    """
    if isinstance(user_id, Account):
        user_id = user_id._id

    if isinstance(user_id, str):
        user_id = ObjectId(user_id)

    # 构造查询条件
    extra_query_filter = {}

    user_id_str = str(user_id)
    lang_pair_list = get_user_trans_lang_pair(user_id)

    status_filter = {"$or": []}

    for lang_pair in lang_pair_list:
        translator_field = "translators.%s.%s.status" % (lang_pair, user_id_str)
        proofreader_field = "proofreaders.%s.%s.status" % (lang_pair, user_id_str)

        status_filter["$or"].extend([
            {translator_field: 0},
            {proofreader_field: 0}
        ])

    status_filter["$or"] and extra_query_filter.update(status_filter)

    tasks, _ = get_user_tasks(user_id, **extra_query_filter)

    now = datetime.datetime.now()

    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    today_weekday = now.weekday()

    has_tomorrow = today_weekday < 6

    tomorrow_start = today_start + datetime.timedelta(days=1)
    tomorrow_end = today_end + datetime.timedelta(days=1)

    this_week_start = tomorrow_start + datetime.timedelta(days=1)
    this_week_end = today_end + datetime.timedelta(days=6-today_weekday)

    after_this_week_start = this_week_end + datetime.timedelta(days=1)


    # 按完成时间把任务分成“今天要完成的任务”, “明天要完成的任务”, “本周要完成的任务”, "其他"
    task_list = []

    for task in tasks:
        for lang_pair in task.translators:
            translators = task.translators.get(lang_pair)
            translator = translators.get(user_id_str)

            if not translator:
                continue

            if translator.status != TranslationTask.TASK_TRANSLATE:
                continue

            completion_date = translator.completion_date

            if today_start <= completion_date <= today_end:
                tag = "today_task"
            elif has_tomorrow and (tomorrow_start <= completion_date <= tomorrow_end):
                tag = "tomorrow_task"
            elif has_tomorrow and this_week_start <= completion_date <= this_week_end:
                tag = "this_week_task"
            elif after_this_week_start <= completion_date:
                tag = "after_this_week_task"
            else:
                tag = "overdue_task"

            task_list.append(format_user_trans_task(
                user_id, task, lang_pair, translator, tag, TranslationTask.TASK_TRANSLATE
            ))

        for lang_pair in task.proofreaders:
            proofreaders = task.proofreaders.get(lang_pair)
            proofreader = proofreaders.get(user_id_str)

            if not proofreader:
                continue

            if proofreader.status != TranslationTask.TASK_TRANSLATE:
                continue

            completion_date = proofreader.completion_date

            if today_start <= completion_date <= today_end:
                tag = "today_task"
            elif has_tomorrow and (tomorrow_start <= completion_date <= tomorrow_end):
                tag = "tomorrow_task"
            elif has_tomorrow and this_week_start <= completion_date <= this_week_end:
                tag = "this_week_task"
            elif after_this_week_start <= completion_date:
                tag = "after_this_week_task"
            else:
                tag = "overdue_task"

            task_list.append(format_user_trans_task(
                user_id, task, lang_pair, proofreader, tag, TranslationTask.TASK_PROOFREAD
            ))

    task_list = sorted(task_list, key=lambda task: task['completion_date'], reverse=True)

    return task_list


def get_tasks_finished(user_id):
    if isinstance(user_id, Account):
        user_id = user_id._id

    if isinstance(user_id, str):
        user_id = ObjectId(user_id)

    # 构造查询条件
    extra_query_filter = {}

    user_id_str = str(user_id)
    lang_pair_list = get_user_trans_lang_pair(user_id)

    status_filter = {"$or": []}

    for lang_pair in lang_pair_list:
        translator_field = "translators.%s.%s.status" % (lang_pair, user_id_str)
        proofreader_field = "proofreaders.%s.%s.status" % (lang_pair, user_id_str)

        status_filter["$or"].extend([
            {translator_field: 1},
            {proofreader_field: 1}
        ])

    status_filter["$or"] and extra_query_filter.update(status_filter)

    tasks, _ = get_user_tasks(user_id, **extra_query_filter)

    task_list = []

    for task in tasks:
        for lang_pair in task.translators:
            translators = task.translators.get(lang_pair)
            translator = translators.get(user_id_str)

            if not translator:
                continue

            if translator.status == TranslationTask.TASK_TRANSLATE:
                continue

            task_list.append(format_user_trans_task(
                user_id, task, lang_pair, translator, 'finished', True
            ))

        for lang_pair in task.proofreaders:
            proofreaders = task.proofreaders.get(lang_pair)
            proofreader = proofreaders.get(user_id_str)

            if not proofreader:
                continue

            if proofreader.status == TranslationTask.TASK_TRANSLATE:
                continue

            task_list.append(format_user_trans_task(
                user_id, task, lang_pair, proofreader, 'finished', False
            ))

    return task_list


def format_user_trans_task(user_id, task, lang_pair, translator, tag, task_type):
    user_id_str = str(user_id)

    src_lang, tar_lang = lang_pair.split('_')

    entry_count, word_count = task.get_entry_and_word_count(
        src_lang,
        tar_lang
    )

    trans_task = {
        'tag': tag,
        'name': task.name,
        'description': task.description,
        'task_type': task_type,
        'src_lang': src_lang,
        'tar_lang': tar_lang,
        'entry_count': entry_count,
        'word_count': word_count,
        'status': translator.get('status'),
        'completion_date': format_time(translator.get('completion_date')),
        'translate_url': url_for(
            'trans_tools.index',
            workspace_id=task.workspace_id,
            task_id=task._id,
            lang_pair=lang_pair,
            user_id=user_id_str,
            task_type=task_type,
            back_url=url_for('translator_task.index')
        ),
        'import_trans_url': url_for(
            'trans_task.import_task_result',
            workspace_id=task.workspace_id,
        ),
        'download_trans_url': url_for(
            'trans_task.export',
            workspace_id=task.workspace_id,
            task_id=task._id,
            lang_pair=lang_pair,
            user_id=user_id_str,
            task_type=task_type
        ),
        'get_progress_url': url_for(
            'trans_task.get_progress',
            workspace_id=task.workspace_id,
            task_id=task._id,
            lang_pair=lang_pair,
            user_id=user_id_str,
        ),
        'task_id': str(task._id),
        'user_id': user_id_str,
    }

    if task_type == TranslationTask.TASK_TRANSLATE:
        progress = task.translated_entry_progress(user_id, lang_pair)

        trans_task['progress'] = {
            'percent': progress[0],
            'word_count': progress[1]
        }
    else:
        _adopt_rate = 0
        all_suggestions, adopt_suggestions = TransSuggestion.get_suggest_adopt_detail(
            task.workspace_id, task._id, user_id, 1
        )

        if all_suggestions != 0:
            _adopt_rate = adopt_suggestions / all_suggestions

        adopt_rate = '%0.3f' % _adopt_rate

        trans_task.update({
            'all_suggestions': all_suggestions,
            'adopt_suggestions': adopt_suggestions,
            'adopt_rate': adopt_rate
        })

    return trans_task

if __name__ == '__main__':
    pass