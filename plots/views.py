# This script renders the view for each url page
from html import escape
from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.templatetags.static import static
from django.views.generic import ListView
from scipy import stats

from .models import Gene, Sample, Expression, MutualInformation

import pandas as pd
import numpy as np
import json

from django.conf import settings
from django.db.models import Q


# import html.parser


def index(request):
    return HttpResponse("Hello, world. You're at the plots index.")

# Create your views here.

# Home page - static
class HomeView(generic.base.TemplateView):
    template_name = 'plots/home.html'

# About page - static
class AboutView(generic.base.TemplateView):
    template_name = 'plots/about.html'

# Contact page - static
class ContactView(generic.base.TemplateView):
    template_name = 'plots/contact.html'

# Mi1 page
class Mi1View(generic.base.TemplateView):
    template_name = 'plots/mi1.html'
    context_object_name = 'mi_compare'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gene1_id = []
        gene2_id = []
        mi_value = []
        for i in MutualInformation.objects.all():
            gene1_id.append(i.gene1.gene_id)
            gene2_id.append(i.gene2.gene_id)
            mi_value.append(i.value)

        gene_pairs = []
        for i in range(len(gene1_id)):
            gene_pair = gene1_id[i] + ' + ' + gene2_id[i]
            gene_pairs.append(gene_pair)

        context['gene_pairs'] = json.dumps(gene_pairs)
        context['gene1_id'] = gene1_id
        context['gene2_id'] = gene2_id
        context['mi_value'] = json.dumps(mi_value)
        return context

# Landscape page
class LandscapeView(generic.TemplateView):
    template_name = 'plots/landscape.html'
    context_object_name = 'this_land'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exp = Expression.objects \
            .filter(Q(gene__id=1) | Q(gene__id=2)) \
            .values()

        query = str(exp.query)
        print(query)
        df = pd.DataFrame(list(exp))
        df = pd.pivot_table(df, values='value', index='gene_id',
                            columns='sample_id')
        g1_exp = df.iloc[0, :]
        g2_exp = df.iloc[1, :]

        xmin = g1_exp.min()
        xmax = g1_exp.max()
        ymin = g2_exp.min()
        ymax = g2_exp.max()

        X, Y = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
        positions = np.vstack([X.ravel(), Y.ravel()])
        # values already stacked correctly due to pd.pivot_table
        kernel = stats.gaussian_kde(df.values, bw_method='silverman')
        Z = np.reshape(kernel(positions).T, X.shape)


        context['Z'] = json.dumps(Z.tolist())
        return context

    def landscape(request):
        query = request.GET.get('gene_id')
        message = "Gene evaluated: {}".format(query)
        template = "landscape.html"
        context = { 'message': message,
        }
        return render(request, template, context)
