from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from main.models import Record, Tag


class RecordListView(ListView):
    model = Record
    template_name = 'main/home.html'
    ordering = '-date_created'


class SearchView(TemplateView):
    template_name = 'main/search_results.html'

    def get(self, request, *args, **kwargs):
        results = search_by = ''
        query = request.GET.get('query')
        tag = request.GET.get('tag')
        if tag:
            try:
                tag = Tag.objects.get(pk=tag)
            except (ValueError, TypeError, Tag.DoesNotExist):
                pass
            else:
                results = Record.objects.filter(tags=tag).order_by('-date_created')
                search_by = '%s "%s"' % (_('тегу'), tag.name)
        else:
            query = strip_tags(query)
            if query:
                results = Record.objects.filter(content__icontains=query).order_by('-date_created')
                search_by = '%s "%s"' % (_('содержимому'), query)

        kwargs['results'] = results
        kwargs['search_by'] = search_by

        return super().get(request, *args, **kwargs)


class RecordCreateView(CreateView):
    template_name_suffix = '_create_form'
    model = Record
    fields = ['title', 'content', 'tags']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.modified_by = self.request.user

        return super().form_valid(form)


class RecordUpdateView(UpdateView):
    template_name_suffix = '_update_form'
    model = Record
    fields = ['title', 'content', 'tags']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.date_modified = timezone.now()

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_simple_user and self.object.author != request.user:
            return HttpResponseForbidden(_('Изменить запись может только ее автор или модератор!'))

        return super().post(request, *args, **kwargs)


class RecordDeleteView(DeleteView):
    template_name_suffix = '_delete_form'
    model = Record
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_simple_user and self.object.author != request.user:
            return HttpResponseForbidden(_('Удалить запись может только ее автор или модератор!'))

        return super().post(request, *args, **kwargs)


class RecordDetailView(DetailView):
    model = Record
