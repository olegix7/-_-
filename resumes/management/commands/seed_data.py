"""
Management command to populate the database with initial seed data.

Usage:
    python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from resumes.models import ResumeTemplate
from announcements.models import Announcement


TEMPLATES = [
    # ── Оригінальні 6 ─────────────────────────────────────────────────────────
    {
        'name': 'Класичний',
        'description': 'Чистий класичний дизайн у синіх тонах. Підходить для більшості галузей.',
        'css_class': 'template-classic',
    },
    {
        'name': 'Сучасний',
        'description': 'Свіжий зелений акцент. Ідеальний для IT та стартапів.',
        'css_class': 'template-modern',
    },
    {
        'name': 'Мінімалістичний',
        'description': 'Строгий темний стиль без зайвих елементів. Для топ-менеджменту.',
        'css_class': 'template-minimal',
    },
    {
        'name': 'Креативний',
        'description': 'Яскравий фіолетовий акцент. Для дизайнерів та творчих спеціальностей.',
        'css_class': 'template-creative',
    },
    {
        'name': 'Елегантний',
        'description': 'Рожево-малиновий стиль. Вишуканий та привабливий вигляд.',
        'css_class': 'template-elegant',
    },
    {
        'name': 'Корпоративний',
        'description': 'Теплий золотисто-коричневий дизайн. Для фінансів та бізнесу.',
        'css_class': 'template-corporate',
    },
    # ── Нові 46 ───────────────────────────────────────────────────────────────
    {
        'name': 'Океан',
        'description': 'Глибокий морський синій з бірюзовими акцентами. Для морських та екологічних галузей.',
        'css_class': 'template-ocean',
    },
    {
        'name': 'Захід сонця',
        'description': 'Тепла градієнтна палітра від помаранчевого до рожевого. Для маркетингу та реклами.',
        'css_class': 'template-sunset',
    },
    {
        'name': 'Лісовий',
        'description': 'Насичений темно-зелений з природними відтінками. Для екологів та агрономів.',
        'css_class': 'template-forest',
    },
    {
        'name': 'Нічне небо',
        'description': 'Темно-синій з сріблястими акцентами. Для астрономів, IT та нічних проектів.',
        'css_class': 'template-night',
    },
    {
        'name': 'Рубіновий',
        'description': 'Насичений червоний з золотими деталями. Для юристів та державних службовців.',
        'css_class': 'template-ruby',
    },
    {
        'name': 'Лавандовий',
        'description': 'Ніжний ліловий градієнт. Для психологів, педагогів та соціальних працівників.',
        'css_class': 'template-lavender',
    },
    {
        'name': 'Металевий',
        'description': 'Сірий металік з темними акцентами. Для інженерів та технічних спеціалістів.',
        'css_class': 'template-steel',
    },
    {
        'name': 'Весняний',
        'description': 'Свіжа зелено-жовта палітра. Для молодих спеціалістів та стажерів.',
        'css_class': 'template-spring',
    },
    {
        'name': 'Осінній',
        'description': 'Теплі коричнево-помаранчеві тони. Для освітян та гуманітарних спеціалістів.',
        'css_class': 'template-autumn',
    },
    {
        'name': 'Арктичний',
        'description': 'Холодний блакитний з білими відтінками. Для медиків та фармацевтів.',
        'css_class': 'template-arctic',
    },
    {
        'name': 'Шоколадний',
        'description': 'Глибокий коричневий з кремовими акцентами. Для ресторанної та харчової галузі.',
        'css_class': 'template-chocolate',
    },
    {
        'name': 'Неонові вогні',
        'description': 'Яскравий кіберпанк-стиль з неоново-рожевим. Для геймерів та стримерів.',
        'css_class': 'template-neon',
    },
    {
        'name': 'Пастельний',
        'description': 'М\'які пастельні тони для делікатного враження. Для HR та психологів.',
        'css_class': 'template-pastel',
    },
    {
        'name': 'Золотий стандарт',
        'description': 'Чорний з золотими акцентами. Для топ-менеджерів та executive-рівня.',
        'css_class': 'template-gold',
    },
    {
        'name': 'Морозний',
        'description': 'Льодяний блакитно-сірий градієнт. Для аналітиків та фінансистів.',
        'css_class': 'template-frost',
    },
    {
        'name': 'Тропічний',
        'description': 'Яскравий бірюзово-зелений. Для туристичного бізнесу та event-менеджерів.',
        'css_class': 'template-tropical',
    },
    {
        'name': 'Мінт',
        'description': 'Свіжий м\'ятно-зелений. Для медсестер, дієтологів та велнес-спеціалістів.',
        'css_class': 'template-mint',
    },
    {
        'name': 'Вишневий',
        'description': 'Насичений вишневий з рожевими тонами. Для fashion та beauty індустрії.',
        'css_class': 'template-cherry',
    },
    {
        'name': 'Космічний',
        'description': 'Темно-фіолетовий із зірчастим ефектом. Для наукових та дослідницьких позицій.',
        'css_class': 'template-cosmic',
    },
    {
        'name': 'Кораловий',
        'description': 'Жвавий кораловий колір. Для творчих маркетологів та SMM-спеціалістів.',
        'css_class': 'template-coral',
    },
    {
        'name': 'Графітовий',
        'description': 'Темний сірий з яскраво-жовтим акцентом. Для архітекторів та дизайнерів.',
        'css_class': 'template-graphite',
    },
    {
        'name': 'Сапфіровий',
        'description': 'Глибокий синьо-індиго. Для юристів, банкірів та консультантів.',
        'css_class': 'template-sapphire',
    },
    {
        'name': 'Оливковий',
        'description': 'Стриманий оливково-зелений. Для військових та держструктур.',
        'css_class': 'template-olive',
    },
    {
        'name': 'Аквамарин',
        'description': 'Яскравий морський бірюзовий. Для журналістів та медіа-спеціалістів.',
        'css_class': 'template-aquamarine',
    },
    {
        'name': 'Бордовий',
        'description': 'Класичний бордовий з кремовим. Для академіків та викладачів.',
        'css_class': 'template-burgundy',
    },
    {
        'name': 'Піщаний',
        'description': 'Теплий беж та пісочний. Для архітекторів та інтер\'єрних дизайнерів.',
        'css_class': 'template-sand',
    },
    {
        'name': 'Електрик',
        'description': 'Яскравий електро-синій. Для електронщиків та DevOps спеціалістів.',
        'css_class': 'template-electric',
    },
    {
        'name': 'Персиковий',
        'description': 'Ніжний персиковий з рожевим. Для вихователів та дитячих психологів.',
        'css_class': 'template-peach',
    },
    {
        'name': 'Сланцевий',
        'description': 'Холодний синьо-сірий. Для бухгалтерів та аудиторів.',
        'css_class': 'template-slate',
    },
    {
        'name': 'Індіго',
        'description': 'Глибокий індиго з фіолетовим. Для UX/UI дизайнерів.',
        'css_class': 'template-indigo',
    },
    {
        'name': 'Бронзовий',
        'description': 'Теплий бронзовий з коричневим. Для музикантів та арт-директорів.',
        'css_class': 'template-bronze',
    },
    {
        'name': 'Льодяний',
        'description': 'Чистий білий з ніжним блакитним обрамленням. Для лікарів та стоматологів.',
        'css_class': 'template-ice',
    },
    {
        'name': 'Медовий',
        'description': 'Золотисто-жовтий теплий градієнт. Для педагогів та дитячих тренерів.',
        'css_class': 'template-honey',
    },
    {
        'name': 'Магнолія',
        'description': 'Ніжний кремово-рожевий. Для косметологів та нутриціологів.',
        'css_class': 'template-magnolia',
    },
    {
        'name': 'Чорний лід',
        'description': 'Чорний з холодним синім підсвіченням. Для Security та пентестерів.',
        'css_class': 'template-blackice',
    },
    {
        'name': 'Смарагдовий',
        'description': 'Глибокий смарагдово-зелений. Для фінансових директорів та CFO.',
        'css_class': 'template-emerald',
    },
    {
        'name': 'Рожевий кварц',
        'description': 'Ніжний рожевий з білим. Для психотерапевтів та коучів.',
        'css_class': 'template-quartz',
    },
    {
        'name': 'Вугільний',
        'description': 'Темний вугільний з яскраво-помаранчевим. Для продакт-менеджерів.',
        'css_class': 'template-charcoal',
    },
    {
        'name': 'Морська хвиля',
        'description': 'Плавний синьо-зелений градієнт. Для логістів та морського транспорту.',
        'css_class': 'template-wave',
    },
    {
        'name': 'Шафрановий',
        'description': 'Яскравий шафраново-помаранчевий. Для шеф-кухарів та кулінарів.',
        'css_class': 'template-saffron',
    },
    {
        'name': 'Мармуровий',
        'description': 'Елегантний білий з сірими розводами. Для нотаріусів та адвокатів.',
        'css_class': 'template-marble',
    },
    {
        'name': 'Ультрафіолет',
        'description': 'Темний фіолетово-синій. Для Data Scientists та ML-інженерів.',
        'css_class': 'template-ultraviolet',
    },
    {
        'name': 'Полуниця',
        'description': 'Яскравий червоно-рожевий. Для event-планувальників та організаторів.',
        'css_class': 'template-strawberry',
    },
    {
        'name': 'Туман',
        'description': 'М\'який сіро-блакитний. Для письменників та контент-мейкерів.',
        'css_class': 'template-fog',
    },
    {
        'name': 'Цегляний',
        'description': 'Теплий цегляно-теракотовий. Для будівельників та прорабів.',
        'css_class': 'template-brick',
    },
    {
        'name': 'Нефрит',
        'description': 'Глибокий нефритово-зелений. Для екологів та природоохоронців.',
        'css_class': 'template-jade',
    },
    {
        'name': 'Платиновий',
        'description': 'Срібло-сірий преміум стиль. Для топ-рекрутерів та HR-директорів.',
        'css_class': 'template-platinum',
    },
]

ANNOUNCEMENTS = [
    {
        'type': 'news',
        'title': 'Вітаємо на платформі Резюме-білдер!',
        'content': (
            'Ми раді вітати вас на нашій платформі для створення професійних резюме.\n\n'
            'Тут ви можете:\n'
            '• Обрати красивий шаблон\n'
            '• Заповнити свої дані\n'
            '• Додати досвід роботи, освіту та навички\n'
            '• Завантажити готове резюме у форматах PDF або DOCX\n\n'
            'Бажаємо успіху у пошуку роботи!'
        ),
    },
    {
        'type': 'announcement',
        'title': 'Нові шаблони резюме вже доступні',
        'content': (
            'Додано 6 нових шаблонів резюме на вибір:\n\n'
            '• Класичний — для будь-якої галузі\n'
            '• Сучасний — для IT та технологій\n'
            '• Мінімалістичний — суворий та діловий\n'
            '• Креативний — для творчих спеціальностей\n'
            '• Елегантний — вишуканий стиль\n'
            '• Корпоративний — для бізнесу та фінансів\n\n'
            'Переходьте до каталогу шаблонів та обирайте!'
        ),
    },
    {
        'type': 'news',
        'title': 'Поради щодо створення успішного резюме',
        'content': (
            'Кілька порад для створення резюме, яке привертає увагу:\n\n'
            '1. Адаптуйте резюме під кожну вакансію — використовуйте функцію клонування\n'
            '2. Вказуйте конкретні досягнення з цифрами\n'
            '3. Не перевантажуйте резюме — тримайтесь 1-2 сторінок\n'
            '4. Перевіряйте граматику та орфографію\n'
            '5. Додайте фото — це підвищує довіру\n\n'
            'Удачі у пошуку роботи!'
        ),
    },
]


class Command(BaseCommand):
    help = 'Заповнює базу даних початковими даними (шаблони, оголошення)'

    def handle(self, *args, **options):
        self.stdout.write('Починаємо заповнення бази даних...\n')

        # ── Templates ────────────────────────────────────────────
        created_count = 0
        for tmpl_data in TEMPLATES:
            obj, created = ResumeTemplate.objects.get_or_create(
                name=tmpl_data['name'],
                defaults={
                    'description': tmpl_data['description'],
                    'css_class': tmpl_data['css_class'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Шаблон: {obj.name}')
            else:
                self.stdout.write(f'  — Шаблон вже існує: {obj.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nШаблони: {created_count} створено, {len(TEMPLATES) - created_count} вже існували.'
        ))

        # ── Announcements (need an author — first superuser or skip) ──
        author = User.objects.filter(is_superuser=True).first()

        ann_created = 0
        for ann_data in ANNOUNCEMENTS:
            obj, created = Announcement.objects.get_or_create(
                title=ann_data['title'],
                defaults={
                    'announcement_type': ann_data['type'],
                    'content': ann_data['content'],
                    'author': author,
                    'is_published': True,
                }
            )
            if created:
                ann_created += 1
                self.stdout.write(f'  ✓ Оголошення: {obj.title}')
            else:
                self.stdout.write(f'  — Оголошення вже існує: {obj.title}')

        self.stdout.write(self.style.SUCCESS(
            f'\nОголошення: {ann_created} створено, {len(ANNOUNCEMENTS) - ann_created} вже існували.'
        ))

        # ── Demo user (optional, only in DEBUG) ──────────────────
        from django.conf import settings
        if settings.DEBUG and not User.objects.filter(username='demo').exists():
            demo = User.objects.create_user(
                username='demo',
                password='demo1234',
                first_name='Демо',
                last_name='Користувач',
                email='demo@example.com',
            )
            Profile.objects.get_or_create(user=demo)
            self.stdout.write(self.style.SUCCESS(
                '\n  ✓ Демо-користувач створено: demo / demo1234'
            ))

        self.stdout.write(self.style.SUCCESS('\n✅ База даних успішно заповнена!\n'))
