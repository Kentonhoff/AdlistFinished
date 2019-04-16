##just finish adding the templates, step #3 is complete
from cats.models import Cat, Comment
from cats.forms import CreateForm, CommentForm

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.uploadedfile import InMemoryUploadedFile

from cats.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class CatListView(OwnerListView):
    model = Cat
    template_name = "cats/cat_list.html"

class CatDetailView(OwnerDetailView):
    model = Cat
    template_name = "cats/cat_detail.html"
    def get(self, request, pk) :
        cat = Cat.objects.get(id=pk)
        comments = Comment.objects.filter(cat=cat).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'cat' : cat, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class CatFormView(LoginRequiredMixin, View):
    template = "cats/cat_form.html"
    success_url = reverse_lazy("cats")
    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            pic = get_object_or_404(Cat, id=pk, owner=self.request.user)
            form = CreateForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            pic = get_object_or_404(Cat, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Adjust the model owner before saving
        cat = form.save(commit=False)
        cat.owner = self.request.user
        cat.save()
        return redirect(self.success_url)

class CatDeleteView(OwnerDeleteView):
    model = Cat
    template_name = "cats/cat_delete.html"

def stream_file(request, pk) :
    pic = get_object_or_404(Cat, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Cat, id=pk)
        comment_form = CommentForm(request.POST)
        comment = Comment(text=request.POST['comment'], owner=request.user, cat=f)
        comment.save()
        return redirect(reverse_lazy('cat_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "cats/comment_delete.html"

    def get_success_url(self):
        cat = self.object.cat
        return reverse_lazy('cat_detail', args=[cat.id])

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
