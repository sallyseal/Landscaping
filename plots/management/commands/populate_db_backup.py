# This script reads the expression data and mi data from respective csv files
# and populates the Django database tables according to models.py

import os
from django.core.management.base import BaseCommand
from plots.models import Gene, Sample, Expression, MutualInformation
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

dir_name = os.path.dirname(os.path.abspath(__file__))
database_name = settings.DATABASES['default']['NAME']
database_url = 'sqlite:///{database_name}'.format(
    database_name=database_name,
)
engine = create_engine(database_url, echo=False)


class Command(BaseCommand):
    help = 'Fills the database with info from the expression CSV file.'

    def handle(self, *args, **kwargs):
        exp_df = pd.read_csv(os.path.join(dir_name, '..', '..', 'database',
                                          'database_exp_input.csv'))
        genes = exp_df.axes[1]
        melted = pd.melt(exp_df, id_vars='Gene ID')
        melted.rename(columns={'Gene ID': 'sample_id', 'variable': 'gene_id'},
                      inplace=True)

        gene_map = {}
        for gene_id in melted['gene_id'].unique():
            new_gene = Gene(gene_id=gene_id)
            new_gene.save()
            gene_map[gene_id] = new_gene.id

        sample_map = {}
        for sample in melted['sample_id'].unique():
            new_sample = Sample(name=sample, dataset='1')
            new_sample.save()
            sample_map[sample] = new_sample.id

        melted['gene_id'] = melted['gene_id'].map(gene_map)
        melted['sample_id'] = melted['sample_id'].map(sample_map)

        # Using sqlalchemy writes the pandas df to database df
        melted.to_sql('plots_expression', engine, if_exists='append',
                      index=False)

        mi_df = pd.read_csv(os.path.join(dir_name, '..', '..', 'database',
                                         'database_mi_input.csv'))
        # Rename df columns to match model names
        mi_renamed = mi_df.rename(columns={'Gene_1': 'gene1_id', 'Gene_2':
                                           'gene2_id', 'MI': 'value'})

        # Query the database to get gene name and associated id
        gene_id_list = []
        for gene in Gene.objects.all():
            gene_id_list.append(gene.gene_id)

        gene_val_list = []
        for gene in Gene.objects.all():
            p = Gene.objects.get(gene_id=gene)
            gene_val_list.append(p.id)

        # Add genes and associated id to a dictionary
        dictionary = dict(zip(gene_id_list, gene_val_list))

        # Iterate through gene1 and gene2 columns of mi_renamed and replace
        # gene1 & gene2 with associated ids from dictionary

        mi_renamed['gene1_id'] = mi_renamed['gene1_id'].map(dictionary) \
                .astype(int)
        mi_renamed['gene2_id'] = mi_renamed['gene2_id'].map(dictionary) \
                .astype(int)

        # Need to say which dataset it comes from
        mi_renamed['dataset'] = '1'

        # Using sqlalchemy writes the pandas df to database df
        mi_renamed.to_sql('plots_mutualinformation', engine, if_exists='append',
                          index=False)
