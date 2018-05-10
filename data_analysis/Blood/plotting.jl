# This script plots the landscape for two given pairs of genes and their data
# points

# Initialize the functions necessary for this script
using DataFrames;
using Plots;
using StatPlots;

# Read in the transformed csv containing the data
# Read in the csv containing the pairs of genes and mi measures
# Get the mi data to sort from highest to lowest mi gene pairs
df1 = readtable("combined_no_HK_T.csv")
df2 = readtable("mi_no_HK_sorted_v3.csv")

# Define the plotting function
# function plotting(df)

    # Look in the MI csv (df2) to see the names of pairs of genes to be plotted
    # Arrange to select numbers of pairs e.g. top 10 (2:11)
    for i in eachrow(df1)
    # Then get the data points of these genes in the df1
    # Define plots to call later as sub-plots
    p = @df scatter(:RUNX1, :TGFB1)
    # p2 = @df scatter(:ANK1, :GATA1)

    # Define the plot as variable p to call later
    # p = plot(p1, p2, layout=(1,1), legend=false)

    # Display the plot
    display(p)
    # savefig(p, "myplot.png")
