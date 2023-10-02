from news.models import *

#создаем двух пользователей с помощью метода User.objects.create_user()
userPetrovich = User.objects.create_user(username = 'Иван Петрович')
userKoshkin = User.objects.create_user(username = 'Петр Кошкин')

#создаем два объекта модели Author, связанные с пользователями
authorPetrovich = Author.objects.create(userModel = userPetrovich)
authorKoshkin = Author.objects.create(userModel = userKoshkin)

#добавляем 4 категории в модель Category
catEdu = Category.objects.create(categoryName = 'Образование')
catIT = Category.objects.create(categoryName = 'IT')
catTech = Category.objects.create(categoryName = 'Технологии')
catRobots = Category.objects.create(categoryName = 'Робототехника')

#добавляем 2 статьи и 1 новость
traficRulesNews = Post.objects.create(
    postAuthor = authorPetrovich,
    postType = Post.news,
    postTitle = '«Лаборатория безопасности»: как юные москвичи изучают правила дорожного движения летом',
    postBody = 'В дни летних каникул столичные школьники знакомятся с правилами дорожного движения. \
 О том, как управлять транспортными средствами и избегать происшествий, они узнают на занятиях «Лаборатории безопасности». \
 Дети посещают интерактивные уроки, организованные в мобильном автогородке, который доставляют в образовательные организации. \
 Сотрудники Госавтоинспекции ведут с учащимися профилактические беседы и дают им пользоваться специальными техническими средствами \
 дорожно-патрульной службы.'
    )

KvantTheoryPost = Post.objects.create(
    postAuthor = authorKoshkin,
    postType = Post.article,
    postTitle = 'Квантовые вычисления',
    postBody = 'Квантовые вычисления представляют собой новую парадигму в области информационных технологий,\
 основанную на принципах квантовой механики. В отличие от классических вычислений, которые основаны на использовании двоичной системы счисления \
 и логических операций над битами (единицами и нулями), квантовые вычисления оперируют с квантовыми системами и используют кубиты,\
 которые могут находиться в состоянии суперпозиции и обладать квантовой взаимосвязью между собой — квантовой запутанностью.'
)

RobotPost = Post.objects.create(
    postAuthor = authorKoshkin,
    postType = Post.article,
    postTitle = 'Рука об руку с человеком',
    postBody = 'Гуманоидные роботы — это человекоподобные роботы, которые, как правило, имеют две руки, две ноги и определенной формы голову.\
 Но, в отличие от андроидов, они необязательно должны полностью копировать внешность человека.\
 Хотя, безусловно, некоторые гуманоидные роботы имеют лицо, у них проработана мимика, и они умеют имитировать человеческие эмоции.\
 Кстати, в прошлом году миру представили гуманоидного робота Ameca, который демонстрирует эмоции с пугающей правдоподобностью. \
 Создатели не раскрывают секрета успеха, но некоторые уверены в том, что они использовали технологию захвата движений.\
 В первую очередь роботов используют для тестирования и разнообразных исследований. Благодаря высокому сходству с человеком,\
 роботы могут быть наглядными пособиями для изучения разных функций. \
 Например, японские ученые создали робота Кенгоро, мышцы которого имитируют человеческие.'
)

#создаем связи многие-ко-многим с промежуточной таблицей PostCategory
#присваиваем созданным постам категории(в одной из статей должно быть не менее 2х категорий)
PostCategory.objects.create(post = traficRulesNews, category = catEdu)
PostCategory.objects.create(post = KvantTheoryPost, category = catTech)
PostCategory.objects.create(post = RobotPost, category = catRobots)
PostCategory.objects.create(post = RobotPost, category = catIT)

#создать минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть минимум 1 комментарий)
Comment.objects.create(
    toPost = traficRulesNews, 
    fromUser = userKoshkin,
    commentBody = 'Коллега, напишите лучше про роботов! Роботы должны управлять транспортом, тогда дорожное движение станет безопаснее.'
    )

Comment.objects.create(
    toPost = traficRulesNews, 
    fromUser = userPetrovich,
    commentBody = 'Коллега, я в ваших роботах не разбираюсь. Если Вы так хотите, напишите сами.'
    )

Comment.objects.create(
    toPost = KvantTheoryPost, 
    fromUser = userPetrovich,
    commentBody = 'я запутался, какая запутанность лучше - квантовая или логическая?'
    )

Comment.objects.create(
    toPost = RobotPost, 
    fromUser = userPetrovich,
    commentBody = 'мечтают ли андроиды об электроовцах?'
    )

Comment.objects.create(
    toPost = RobotPost, 
    fromUser = userKoshkin,
    commentBody = 'почитайте Филипа Киндреда Дика'
    )

#применяя методы like() и dislike() скорректировать рейтинги статей/новостей/комментариев
traficRulesNews.like()
KvantTheoryPost.like()
KvantTheoryPost.like()
RobotPost.like()
RobotPost.like()
RobotPost.like()

for comment in Comment.objects.filter(fromUser = userKoshkin):
    comment.dislike()

for comment in Comment.objects.filter(fromUser = userPetrovich):
    comment.like()

#обновить рейтинг пользователей
authorPetrovich.update_rating()
authorKoshkin.update_rating()

#вывести username и рейтинг лучшего пользователя
bestAuth = Author.objects.all().order_by('-userRate').values('userModel__username', 'userRate')[0]
print(f'Наш лучший автор: {bestAuth["userModel__username"]} с рейтингом: {bestAuth["userRate"]} ')

#вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи основываясь на лайках/дизлайках этой статьи
bestArticleObj = Post.objects.filter(postType = Post.article).order_by('-postRate')[0]
bestArticle = Post.objects.filter(postType = Post.article).order_by('-postRate').values('postDateTime', 'postAuthor__userModel__username', 'postRate', 'postTitle')[0]
bestArticlePreview = bestArticleObj.preview()
print(f'Лучшая статья: добавлена {str(bestArticle["postDateTime"])[:19]} автором {bestArticle["postAuthor__userModel__username"]}\n Рейтинг: {bestArticle["postRate"]} \n\
 {bestArticle["postTitle"]}\n {bestArticlePreview}')

#вывести все комментарии к этой статье (дата, пользовтель, рейтинг, текст)
comments = Comment.objects.filter(toPost=bestArticleObj).values('commentDateTime', 'fromUser__username', 'commentRate', 'commentBody')
print('Комментарии:')
for comment in comments:
    print ( f'{str(comment["commentDateTime"])[:19] }) # - {comment["fromUser__username"]} - [{comment["commentRate"]}]\n {comment["commentBody"]}')
