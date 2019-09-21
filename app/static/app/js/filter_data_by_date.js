$(function() {
  const url = $("#data_url").attr('url');
  /*if (localStorage.getItem("gate_no") === null) {
    var gate_no = window.localStorage.getItem('gate_no');
  }else{
    gate_no = null;
  }*/

  $('input[name="daterange"]').daterangepicker({
    opens: 'left'
  }, function(start, end, label) {
    $.ajax({
      url: url,
      data:{
        'start': start.format('YYYY-MM-DD'),
        'end': end.format('YYYY-MM-DD'),
        //'gate_no': gate_no
      },

      beforeSend: ()=>{
        $('.loader').removeAttr('hidden');
      },

      complete: ()=>{
        $('.loader').attr('hidden', true);
      },

      success: (data)=>{
        if (data == 'NoData'){
          alert('No data within the selected date range')
        }else{
          total = data.total
          html_detail = data.q
          setData(total, html_detail);

          labels = data.labels
          values = data.values
          setGraph(labels, values);
        }
      }
    });
  });
});