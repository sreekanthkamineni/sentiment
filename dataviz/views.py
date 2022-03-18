from django.shortcuts import render
from .tweet_analysis import tweet_senti
from django.contrib import messages


# Create your views here.


def home(request):
    if request.method == 'POST':
        hash_tag_name = request.POST.get('hash_tag')
        print(hash_tag_name)
        print(tweet_senti(hash_tag_name))
    return render(request, 'index.html')


def viz(request):
    if request.method == 'POST':

        hash_tag_name = request.POST.get('hash_tag')
        data_dict = tweet_senti(hash_tag_name)

        # data_dict = {}
        # data_dict['2021-05-21'] = [5 , 6 ,0]
        # data_dict['2021-05-22'] = [6 , 9 ,6]
        # data_dict['2021-05-23'] = [8 , 2 ,9]
        # data_dict['2021-05-24'] = [2 , 3 ,2]

        if len(data_dict) < 1:
            messages.warning(request, 'Issues with Twitter API')
            return render(request, 'result.html', {'Hashtag': hash_tag_name})
        dates = list(data_dict.keys())
        positive = [val[0] for val in list(data_dict.values())]
        Negative = [val[1] for val in list(data_dict.values())]
        Nutral = [val[2] for val in list(data_dict.values())]
        context = {'Hashtag': hash_tag_name,
                   'totals': sum(positive+Negative+Nutral),
                   'dates': dates,
                   'Positive_data': positive,
                   'negative_data': Negative,
                   'Nutral_data': Nutral}
    return render(request, 'result.html', context)
