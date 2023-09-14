import random
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation


COMPLIMENTS = [
    'Молодец!', 'Отлично!', 'Хорошо!',' Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
    'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Ты многое сделал, я это вижу!',
    'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!',
    'Талантливо!', 'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!',
    'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 
    'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!', 'Мы с тобой не зря поработали!',
    'С каждым разом у тебя получается всё лучше!', 'Теперь у тебя точно все получится!',
    'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Именно этого я давно ждал от тебя!',
    ]


def get_schoolkid_by_name(schoolkid_name):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print('Ученика с таким именем нет в базе данных.')
    except Schoolkid.MultipleObjectsReturned:
        print('Учеников с таким именем несколько.')


def fix_marks(schoolkid):
    child = get_schoolkid_by_name(schoolkid)

    if not child:
        return 'Проверьте вводимые значения и попробуйте еще раз.'

    bad_grades_by_child = Mark.objects.filter(schoolkid=child.id, points__in=[2, 3])
    
    for bad_grade in bad_grades_by_child:
        bad_grade.points = 5
        bad_grade.save()

    return 'Сделано!'


def remove_chastisements(schoolkid):
    child = get_schoolkid_by_name(schoolkid)

    if not child:
        return 'Проверьте вводимые значения и попробуйте еще раз.'

    сhastisemens_by_child = Chastisement.objects.filter(schoolkid=child.id)
    сhastisemens_by_child.delete()

    return 'Сделано!'


def create_commendation(schoolkid, subj):
    child = get_schoolkid_by_name(schoolkid)

    if not child:
        return 'Проверьте вводимые значения и попробуйте еще раз.'
        
    compliment_text = random.choice(COMPLIMENTS)

    last_lesson_by_subject = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title=subj
        ).order_by('date').last()

    Commendation.objects.create(text=compliment_text,
                                created=last_lesson_by_subject.date,
                                schoolkid=child,
                                subject=last_lesson_by_subject.subject,
                                teacher=last_lesson_by_subject.teacher
                                )

    return 'Сделано!'
