from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from market.apps.models import App
from market.apps.forms import SubmitAppForm, AppForm, ReviewForm

# TODO: Does this library verify certs? Do we care?
# NOTE: httplib2 used so compression/caching/redirecting is supported
import httplib2

# NOTE: Used to protect against malicious xml
from defusedxml.minidom import parseString

# Create your views here.

def app(request, pk):
    app = get_object_or_404(App, pk=pk)
    reviewform = ReviewForm()
    reviewform.helper.form_action = reverse('app', args=[str(app.pk)])
    return render(request, "apps/app.html", {
        'app': app,
        'reviewform': reviewform,
    })

class LatestView(generic.ListView):
    template_name = 'apps/latest.html'
    context_object_name = 'latest_app_list'

    def get_queryset(self):
        """Return the last five published apps."""
        return App.objects.order_by('-pub_date')[:5]

class CategoryView(generic.ListView):
    template_name = 'apps/apps_by_category.html'
    context_object_name = 'applist'

    def get_queryset(self):
        # get short name for category
        cat = lng = self.args[0]
        if lng == "AudioVideo":
            lng = "Audio/Video"
        for category in App.CATEGORY_OPTIONS:
            s, l = category
            if l == lng:
                cat = s
        return App.objects.filter(category=cat)

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = self.args[0]
        return context

@login_required
def submitview(request):
    if request.method == 'POST':
        form = SubmitAppForm(request.POST)
        if form.is_valid():
            h = httplib2.Http(".cache")
            #try:
            resp, content = h.request(form.cleaned_data['xml'], "GET")
            xml = parseString(content)
            #except:
            # FIXME: Give the user notice and reason
            # return HttpResponseRedirect("/")

            if(xml.documentElement.localName == 'interface' and
               xml.documentElement.namespaceURI ==
               "http://zero-install.sourceforge.net/2004/injector/interface" ):
                # Woohoo Zero Install feed, now extract data
                # FIXME: Extract data only in English, for now
                short = lng = xml.documentElement.\
                      getElementsByTagName("category")[0].firstChild.nodeValue
                for category in App.CATEGORY_OPTIONS:
                    s, l = category
                    if l == lng:
                        short = s

                appform = AppForm({
                    "name": xml.documentElement.\
                            getElementsByTagName("name")[0].firstChild.nodeValue,
                    "description": xml.documentElement.\
                                   getElementsByTagName("description")[0].firstChild.nodeValue,
                    "xml": form.cleaned_data['xml'],
                    "homepage": xml.documentElement.\
                                getElementsByTagName("homepage")[0].firstChild.nodeValue,
                    "uploader": request.user.id,
                    "category": short,
                })
                if appform.is_valid():
                    appform.save()
                    return render(request, 'apps/submit.html', {
                        "message": "Success!",
                        "form": SubmitAppForm(),
                    })
                else:
                    return render(request, 'apps/invalid-coded-form')
            else:
                # Not a Zero Install feed
                return render(request, 'apps/nope')
        else:
            return render(request, 'apps/submit.html', {
                "form": form,
            })
    else:
        form = SubmitAppForm()
        return render(request, 'apps/submit.html', {
            "form": form,
        })
