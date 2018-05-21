// This script produces a bar graph of the gene pairs MI

// Getting x and y variables from Django views
// Will call this file where we want to display it in the html framework
x_val = JSON.parse('{{ gene_pairs | escapejs }}');
y_val = JSON.parse('{{ mi_value | escapejs }}');

var trace1 = {
  x: x_val.slice(0,31),
  y: y_val.slice(0,31),
  type: 'bar',
  marker: {
    color: 'rgb(44,127,124)'
  }
};

var data = [trace1];

var layout = {
  title: 'Mutual Information for Top XXX Gene Pairs',
  font:{
    family: 'Raleway, snas-serif'
  },
  showlegend: false,
  xaxis: {
    title: 'Gene Pairs',
    tickangle: -45
  },
  yaxis: {
    title: 'Mutual Information',
    zeroline: false,
    gridwidth: 2
  },
  bargap :0.05
};

Plotly.newPlot('myDiv', data, layout);
