(function() {
    $(document).ready(function() {
      var walkthrough;
      walkthrough = {
        ShowDiv: function(id) {
        if ($('#destenceCheck').prop('checked')) {
            $(id).show();
        } else {
            $(id).hide();
        }
        },
      };
      $('#destenceCheck').click(function() {
        walkthrough.ShowDiv("#Fromdestence");
      });
      walkthrough.ShowDiv("#Fromdestence");
    });
  }).call(this);
