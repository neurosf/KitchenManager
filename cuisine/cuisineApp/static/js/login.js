
(function() {
    $(document).ready(function() {
      var walkthrough;
      walkthrough = {
        passwordchecked: 0,
        ShowPassword: function() {
          if (walkthrough.passwordchecked === 0) {
            $('#loginPassword').prop('type', 'text');
            walkthrough.passwordchecked = 1;
          } else {
            $('#loginPassword').prop('type', 'password');
            walkthrough.passwordchecked = 0;
          }
        },
      };
      $('#showPasswordCheck').click(function() {
        walkthrough.ShowPassword();
      });
    });
  }).call(this);