##just finish adding the templates, step #3 is complete
from autos.models import Auto, Comment
from autos.forms import CreateForm, CommentForm

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.uploadedfile import InMemoryUploadedFile

from autos.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class AutoListView(OwnerListView):
    model = Auto
    template_name = "autos/auto_list.html"

class AutoDetailView(OwnerDetailView):
    model = Auto
    template_name = "autos/auto_detail.html"
    def get(self, request, pk) :
        auto = Auto.objects.get(id=pk)
        comments = Comment.objects.filter(auto=auto).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'auto' : auto, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class AutoFormView(LoginRequiredMixin, View):
    template = "autos/auto_form.html"
    success_url = reverse_lazy("autos")
    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            pic = get_object_or_404(Auto, id=pk, owner=self.request.user)
            form = CreateForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            pic = get_object_or_404(Auto, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Adjust the model owner before saving
        auto = form.save(commit=False)
        auto.owner = self.request.user
        auto.save()
        return redirect(self.success_url)

class AutoDeleteView(OwnerDeleteView):
    model = Auto
    template_name = "autos/auto_delete.html"

def stream_file(request, pk) :
    pic = get_object_or_404(Auto, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Auto, id=pk)
        comment_form = CommentForm(request.POST)
        comment = Comment(text=request.POST['comment'], owner=request.user, auto=f)
        comment.save()
        return redirect(reverse_lazy('auto_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "autos/comment_delete.html"

    def get_success_url(self):
        auto = self.object.auto
        return reverse_lazy('auto_detail', args=[auto.id])

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
