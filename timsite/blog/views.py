from django.shortcuts import render
from django.utils import timezone
# from django.http import HttpResponse
# from django.template import loader


from .models import Post


def index(request):
    latest_post_list = Post.objects.filter(published=True).order_by('-pub_date')[:5]

    context = {
        'latest_post_list': latest_post_list,
    }
    return render(request, 'blog/index.html', context)


def archives(request):
    print("page was requested")
    post_list = Post.objects.filter(published=True).order_by('-pub_date')

    class YearPostIterator:
        def __init__(self, post_list):
            self.post_list = post_list
            self.counter = 0
            try:
                self.year_counter = post_list[0].pub_date.year
            except IndexError:
                self.year_counter = 2018
            self.year_range = iter(range(self.year_counter, 2018-1, -1))
            self.finished = False
            self.timeout = 0

        def __iter__(self):
            return self

        def post_generator(self):
            while True:
                try:
                    if self.post_list[self.counter].pub_date.year != self.year_counter:
                        self.year_counter = self.post_list[self.counter].pub_date.year
                        break
                except IndexError:
                    self.finished = True
                    break

                yield self.post_list[self.counter]
                self.counter += 1

        def __next__(self):
            if self.finished or (self.timeout > 10):
                raise StopIteration()
            else:
                self.timeout += 1
                next_year = next(self.year_range)
                # if next_year == 2018:
                #     self.finished = True
                return [next_year, self.post_generator()]

    context = {
        'year_post_iterator': YearPostIterator(post_list)
    }

    return render(request, 'blog/archives.html', context)

def page(request, slug):
    post = Post.objects.get(slug=slug)
    context = {'post': post}
    return render(request, 'blog/post.html', context)


def about(request):
    context = {'about': True}
    print("This is actually printed!")
    return render(request, 'blog/about.html', context)
