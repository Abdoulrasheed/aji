$(document).ready(()=>{
  $(".filter-by-gate").click(function(){
    const gate_no = $(this).data('gate');
    window.localStorage.setItem('gate_no', gate_no);
    const url = $("#data_url").attr('url');
    $.ajax({
      url: url,
      data: {'gate_no': gate_no},

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