from django.urls import path

from .views import index, detail, results, vote

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('<int:question_id>/', detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', vote, name='vote'),
    
   
]