from django.core.management.base import BaseCommand, CommandError
import logging

def test():
    loggers = [
        'django',
        'django.request',
        'django.server',
        'django.template',
        'django.db_backends',
        'django.security',
        ]
    for l_name in loggers:
        
        logger = logging.getLogger(l_name)

        #test DEBUG:
        logger.debug('[%s]_This is DEBUG message!', l_name)   
        #test INFO:
        logger.info('[%s]_This is INFO message!', l_name) 
        #test WARNING:
        logger.warning('[%s]__This is WARNING message!', l_name) 
        #test ERROR:
        logger.error('[%s]_This is ERROR message!', l_name) 
        #test CRITICAL:
        logger.critical('[%s]_This is CRITICAL message!', l_name) 



class Command(BaseCommand):
    help = 'Тестирование настроек логгирования Django' # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    # missing_args_message = 'Недостаточно аргументов'
    # requires_migrations_checks = True # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)
 
    # def add_arguments(self, parser):
    #     # Positional arguments
    #     parser.add_argument('argument', nargs='+', type=int)
 
    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        # self.stdout.write(str(options['argument']))
        self.stdout.write('Тестируем логгирование:')
        test()
