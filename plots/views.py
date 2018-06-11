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
from django.conf import settings
from django.db.models import Q

from .models import Gene, Sample, Expression, MutualInformation, Pca

import pandas as pd
import numpy as np
import json
import math


# Create your views here.

# Home page - static
class HomeView(generic.base.TemplateView):
    template_name = 'plots/home.html'

# About page - static
class AboutView(generic.base.TemplateView):
    template_name = 'plots/about.html'

# Background page - static
class ContactView(generic.base.TemplateView):
    template_name = 'plots/contact.html'

class ReferenceView(generic.base.TemplateView):
    template_name = 'plots/reference.html'

# Heterogeneity page
class HeteroView(generic.base.TemplateView):
    template_name = 'plots/hetero.html'
    context_object_name = 'this_hetero'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pc1 = []
        pc2 = []
        for i in Pca.objects.all():
            pc1.append(i.pc1)
            pc2.append(i.pc2)
        context['pc1'] = json.dumps(pc1)
        context['pc2'] = json.dumps(pc2)

        # Need expression values for these cells for the coloring
        # Depending on which gene the user selects those expression values must
        # be overlayed onto the PCA plot
        gene = self.request.GET.get('gene')
        exp = Expression.objects \
            .filter(gene__id=gene, sample__cell_type='MEP').values()

        query = str(exp.query)
        df = pd.DataFrame(list(exp))
        df = pd.pivot_table(df, values='value', index='gene_id', columns='sample_id')
        gene_exp = df.iloc[0, :]

        cmax = gene_exp.max()
        cmin = gene_exp.min()

        context['gene_exp'] = json.dumps(gene_exp.tolist())
        context['cmax'] = json.dumps(cmax)
        context['cmin'] = json.dumps(cmin)

        genes = []
        summary = []
        for i in Gene.objects.all():
            genes.append(i.gene_id)
            summary.append(i.summary)

        objects = Gene.objects.all()

        context['objects'] = objects
        context['genes'] = genes
        context['summary'] = summary

        gene_obj = Gene.objects.get(id=gene)
        context['gene'] = gene_obj

        return context


# Mi1 page
class Mi1View(generic.base.TemplateView):
    template_name = 'plots/mi1.html'
    context_object_name = 'mi_compare'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get list of gene1 and gene2 and corresponding mi value
        gene1_id = []
        gene2_id = []
        mi_value = []
        for i in MutualInformation.objects.all():
            gene1_id.append(i.gene1.gene_id)
            gene2_id.append(i.gene2.gene_id)
            mi_value.append(i.value)
        # Combined gene1 and gene2 with + to give gene pairs
        gene_pairs = []
        for i in range(len(gene1_id)):
            gene_pair = gene1_id[i] + ' + ' + gene2_id[i]
            gene_pairs.append(gene_pair)
        # Return this information
        context['gene_pairs'] = json.dumps(gene_pairs)
        context['gene1_id'] = gene1_id
        context['gene2_id'] = gene2_id
        context['mi_value'] = json.dumps(mi_value)

        # Code to produce Z values for mi heatmap plots
        # Also need a list of gene1 and gene2 as X and Y

        genes = Gene.objects.all()
        gene_map = {}
        gene_self = []
        for gene in genes:
            gene_map[gene.id] = gene.gene_id
            # When 2 genes are same give a value of 1 - this is the diagonal in
            # the heatmap
            gene_self.append({
                'id': 0,
                'gene1_id': gene.id,
                'gene2_id': gene.id,
                'value': 1,
                'dataset': '1'
            })

        mis = MutualInformation.objects.values()
        query = str(mis.query)
        # Add gene_self to get full matrix including self comparisons
        df = pd.DataFrame(list(mis) + gene_self)
        df = pd.pivot_table(df, values='value', index='gene1_id', columns='gene2_id')
        df.rename(columns=gene_map, index=gene_map, inplace=True)
        # Mirror transpose the matrix accross the diagonal line
        for gene1 in df.axes[1]:
            for gene2 in df.index:
                if np.isnan(df.loc[gene1][gene2]):
                    df.loc[gene1][gene2] = df.loc[gene2][gene1]

        # Remove nans replace with 0 as precaution
        df = df.fillna(0)

        x = df.index
        y = df.columns
        z = df.values

        context['gene_map'] = json.dumps({v: k for k, v in gene_map.items()})
        context['x'] = json.dumps(x.tolist())
        context['y'] = json.dumps(y.tolist())
        context['z'] = json.dumps(z.tolist())
        return context

# Landscape page
class LandscapeView(generic.TemplateView):
    template_name = 'plots/landscape.html'
    context_object_name = 'this_land'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        gene1 = self.request.GET.get('gene1')
        gene2 = self.request.GET.get('gene2')

        gene1_obj = Gene.objects.get(id=gene1)
        gene2_obj = Gene.objects.get(id=gene2)

        exp = Expression.objects \
            .filter(Q(gene__id=gene1) | Q(gene__id=gene2)) \
            .values()

        query = str(exp.query)
        df = pd.DataFrame(list(exp))
        df = pd.pivot_table(df, values='value', index='gene_id',
                            columns='sample_id')
        g1_exp = df.iloc[0, :]
        g2_exp = df.iloc[1, :]

        xmin = g1_exp.min()
        xmax = g1_exp.max()
        ymin = g2_exp.min()
        ymax = g2_exp.max()

        X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([X.ravel(), Y.ravel()])
        # values already stacked correctly due to pd.pivot_table
        kernel = stats.gaussian_kde(df.values, 'silverman')
        # This is the bandwidth as calculated by Silverman method
        k_factor = kernel.factor

        Z = np.reshape(kernel(positions).T, X.shape)
        Z = np.log(Z)
        Z = -(Z)

        context['k_factor'] = k_factor
        context['Z'] = json.dumps(Z.tolist())

        objects = Gene.objects.all()
        context['objects'] = objects
        context['gene1'] = gene1_obj
        context['gene2'] = gene2_obj

        return context
