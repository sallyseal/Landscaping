# # Initialize the functions necessary for this script
using DataFrames;
using Plots;
using StatPlots;
#
# Read in the csv file that contains data for plotting
df = readtable("combined_no_HK_T.csv")

# Plot values of two genes against one another
# p1 = @df df scatter(:RUNX1, :TGFB1, colour = [:red :blue])
# display(p1)

p2 = @df df scatter(:CDK6, :MCL1, colour = [:red :blue])
display(p2)



# using DataFrames;
# df = DataFrame(a = 1:10, b = 10*rand(10), c = 10 * rand(10))
# @df df plot(:a, [:b :c], colour = [:red :blue])
# @df df scatter(:a, :b, markersize = 4 * log.(:c + 0.1))
# t = table(1:10, rand(10), names = [:a, :b]) # IndexedTable
# @df t scatter(2 * :b)


##########################################################
# # Pkg.add("StatPlots")
# using StatPlots # Required for the DataFrame user recipe
# # Now let's create the DataFrame
# using DataFrames
# df = DataFrame(a = 1:10, b = 10*rand(10), c = 10 * rand(10))
# # Plot the DataFrame by declaring the points by the column names
# p1 = @df df plot(:a, [:b :c]) # x = :a, y = [:b :c]. Notice this is two columns!
# display(p1)
