from django.db import models

# Create your models here.
# Then activate them by including the app in settings.py under INSTALLED_APPS =

# Class to define the gene with gene name and go term
class Gene(models.Model):
    gene_id = models.CharField(max_length=20, unique=True)
    go_term = models.CharField(max_length=1000)

    def __str__(self):
        return self.gene_id


# Class to degine the cell name and the dataset that it comes from
# Dataset 1 = blood data; Dataset2 = neuronal data
class Sample(models.Model):
    name = models.CharField(max_length=1000)
    dataset = models.CharField(max_length=1000)


# Class to define the expression values
# Each gene and sample (cell) is given a foreign key which will be written to db table
class Expression(models.Model):
    # Implement foreignkey
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    value = models.FloatField()

# Class to define the mi values
# This must be created into a db table
# Foreign keys for gene1 gene2 must be obtained from plots_expression db table
# Define which dataset the pair and associated mi comes from
class MutualInformation(models.Model):
    gene1 = models.ForeignKey(Gene, on_delete=models.CASCADE,
                              related_name='gene1')
    gene2 = models.ForeignKey(Gene, on_delete=models.CASCADE,
                              related_name='gene2')
    value = models.FloatField()
    dataset = models.CharField(max_length=1000)
    # Can we create "pair" here which combines the two names with & for bar graph
    # columns?
