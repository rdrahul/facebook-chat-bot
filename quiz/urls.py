from django.conf.urls import include,url
from views import QuizView
import views
urlpatterns=[
    #url(r'^$',views.testview),
    url(r'^13c75f6e354bdcc144d80728f295446edba02d8ae071272e05/?$',QuizView.as_view())
]