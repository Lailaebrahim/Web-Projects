$(document).ready(function () {
    console.log('Document ready');

    $('#schedule-btn').click(function () {
        
        var datetime = $('#datetimepicker input').val();
        var title = $('#main-form input[name="title"]').val();
        var content = $('#main-form textarea[name="content"]').val();
        if (title != '' || content != '')
        {
            $.ajax({
                url: '/new/scheduled/post',
                method: 'POST',
                data: { datetime: datetime, title: title, content: content },
                success: function (status) {
                    console.log('Success:', status);
                    if (status == 'True') {
                        $('#myModal').modal('hide');
                        alert('Your post has been scheduled successfully!')
                        location.reload();
                    }
                    else {
                        alert('Scheduled date and time cannot be in the past')
                    }
                }
            });

        
    }
    else {
        alert("Both Fields are required");  
    }
    

    });
});