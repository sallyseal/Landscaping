<!-- PLOTTING THE MI BAR GRAPH -->
<div id="myDiv"><!-- Plotly chart will be drawn inside this DIV --></div>
<!-- JS FOR MI PLOT -->

  <script>
  // {% with y_val=mi_value %}
  // {% with x_val=gene_pairs %}
  x_val = JSON.parse('{{ gene_pairs | escapejs }}');
  y_val = JSON.parse('{{ mi_value | escapejs }}');
  // console.log(y_val);
  // console.log(y_val);
  // var x_val = {{gene_pairs}};
  // var y_val = {{mi_value}};
  var trace1 = {
    x: x_val.slice(0,31),
    y: y_val.slice(0,31),
    type: 'bar',
    // text: ['4.17 below the mean', '4.17 below the mean', '0.17 below the mean', '0.17 below the mean', '0.83 above the mean', '7.83 above the mean'],
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

  </script>
