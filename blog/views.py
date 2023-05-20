from django.shortcuts import render
from django.views.generic import TemplateView


class BlogHome(TemplateView):

    def get(self, errors=False, *args, **kwargs):
        context = {}
        return render(self.request, 'blog_home.html', context)
