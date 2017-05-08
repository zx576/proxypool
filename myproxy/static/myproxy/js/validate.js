/**
 * Created by ZX on 2016/12/13.
 */

$(document).ready(function(){
// 用户名判断
        $('#user_name').blur(function () {
            var un = $(this).val();
            if (un == '' || un == null){
                $('#userdiv').addClass('has-error');
                $('#usere').removeClass('hidden');
                return;
            } else {
                $('#userdiv').removeClass('has-error');
                 $('#usere').addClass('hidden')
            }
            // console.log(un);

            $.post('/register/verifyname/',
                    {
                        csrfmiddlewaretoken: '{{ csrf_token }}',
                        'name':un
                    },
                    function (data) {
// {#                console.log(data);#}

                if (data.data == 'T' || un.length == 0){
                    $('#userdiv').addClass('has-success');
                    $('#info').text('');
                    $('#users').removeClass('hidden')
                }else {
                    $('#userdiv').addClass('has-error');
                    $('#info').text('用户名已存在')
                }
                    });
        });
// {#        密码判断#}
        $('#password').blur(function () {
            var pw1 = $(this).val();
            // console.log(pw1);
            if (pw1.length == 0 || pw1 == null){
             // console.log('e');
                $('#pw1div').addClass('has-error');
                $('#pw1s2').removeClass('hidden');
                $('#pw1s1').addClass('hidden');
            } else {
                $('#pw1div').removeClass('has-error').addClass('has-success');
                $('#pw1s2').addClass('hidden');
                $('#pw1s1').removeClass('hidden')
            }
        });

        $('#pw2').blur(function(){
            var pw2 = $(this).val();
            var pw1 = $('#password').val();
           // console.log(pw2);
            if (pw2 != pw1 || pw2.length == 0){
               // console.log(pw1);
                $('#pw2div').addClass('has-error');
                $('#pw2s2').removeClass('hidden');
                $('#pw2s1').addClass('hidden');
            } else{
                $('#pw2div').removeClass('has-error').addClass('has-success');
                $('#pw2s2').addClass('hidden');
                $('#pw2s1').removeClass('hidden')
            }
        });
// {#         提交表单#}
        $('#submitbtn').click(function () {
            // console.log($('#userdiv').hasClass('has-success'));
            // console.log($('#pw1div').hasClass('has-success'));
            // console.log($('#pw2div').hasClass('has-success'));
            if ($('#userdiv').hasClass('has-success') && $('#pw1div').hasClass('has-success') && $('#pw2div').hasClass('has-success')){
                console.log('s');
                $("#form1").unbind().submit();
            } else {
                $('#form1').submit(function () {
                    console.log('e');
                    return false;
                })
            }
        })


    });