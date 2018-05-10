using DataFrames;
using Plots;

function df2array(df)
    data_array = convert(Array, df)
    data_array = reshape(data_array,(nrow(df), ncol(df)))
    return data_array
end

# Import the file of interest
df = readtable("combined_data_1_0_T_noh.csv")

# Convert to data_array for plotting purposes
data_array = df2array(df)

# Plot a scatter of the data_array
x=collect(1.:1.:90)
y=collect(1.:1.:806)
Plots.scatter(x,y,data_array)
