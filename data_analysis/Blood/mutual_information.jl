# This script computes the MI for all possible pairs of genes in a given input
# file

# Initialize the functions necessary for this script
using DataFrames;
using InformationMeasures;

# Read in the csv file of interest
df = readtable("combined_data_no_HK_v3.csv")

# Define the df2array function which we call in the function mutual_information
function df2array(df)
    data_array = convert(Array, df)
    data_array = reshape(data_array,(nrow(df), ncol(df)))
    return data_array
end

# Function to calculate mutual information for all pairs of genes
function mutual_information(df)

    # Call the df2array function to convert the df to a data_array to iterate
    # through
    data_array = df2array(df)

    # genes = 25 and cells = 808 (but should be 807 as it's counting 1st column)
    (genes, cells) = size(data_array)

    # Need to call this on dataframe and not on the goi_names otherwise can't
    # access the data
    data = Array{Any}[]
    for i in 1:length(data_array[:,1])
            for j in i+1:length(data_array[:,1])
                goi_1 = convert(Array{Float64,1}, data_array[i,2:end][:])
                goi_2 = convert(Array{Float64,1}, data_array[j,2:end][:])
            push!(data, [data_array[i], data_array[j], get_mutual_information(goi_1, goi_2)])
        end
    end

    # Create a new datafrae containing each gene name and mi measure
    doi = DataFrame( Gene_1 = String[], Gene_2 = String[], MI = Float64[])
    for i in data
        push!(doi, i)
    end
    # Sort from highest mi to lowest
    doi_sorted = sort!(doi, cols = [:MI], rev = true)
    return doi_sorted
end

# Calling the function and assign output to a variable called data
data = mutual_information(df)

# Write the data to a csv file called mi.csv
writetable("mi_no_HK_sorted_v3.csv", data)
