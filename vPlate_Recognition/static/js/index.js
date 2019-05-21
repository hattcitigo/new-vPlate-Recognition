document.onreadystatechange = function () {
    if (document.readyState === 'complete') {
        loadText();
        $(".input-file").before(
            function () {
                if (!$(this).prev().hasClass('input-ghost')) {
                    var element = $("<input type='file' id='file_load' class='input-ghost' accept='.jpg, .png' style='visibility:hidden; height:0'>");
                    element.attr("name", $(this).attr("name"));
                    element.change(function () {
                        element.next(element).find('input').val((element.val()).split('\\').pop());
                    });
                    $(this).find("button.btn-choose").click(function () {
                        element.click();
                    });
                    return element;
                }
            }
        );
    }
}
function loadText() {
    var btn_upfile = document.getElementById("btn_upfile");
    var txt_choose = document.getElementById("txt_choose");
    var btn_choose = document.getElementById("btn_choose");
    var txt_title = document.getElementById("txt_title");
    var txt_title_form = document.getElementById("txt_title_form");
    var txt_title_result = document.getElementById("txt_title_result");
    var img_upload = document.getElementById("img_upload");
    var img_1 = document.getElementById("img_1");
    var img_2 = document.getElementById("img_2");
    var img_3 = document.getElementById("img_3");
    var img_4 = document.getElementById("img_4");
    var txt_result_1 = document.getElementById("txt_result_1");
    var txt_result_2 = document.getElementById("txt_result_2");
    var txt_result_3 = document.getElementById("txt_result_3");
    var txt_result_4 = document.getElementById("txt_result_4");
    var txt_message = document.getElementById("txt_message");
    btn_upfile.innerHTML = "Tải lên";
    txt_choose.placeholder = "Vui lòng chọn file ảnh...";
    btn_choose.innerHTML = "Chọn tệp";
    txt_title.innerHTML = "NHẬN DIỆN BIỂN SỐ XE";
    txt_title_form.innerHTML = "NHẬN DIỆN BIỂN SỐ XE";
    txt_title_result.innerHTML = "KẾT QUẢ";
    txt_message.innerHTML = "VUI LÒNG CHỜ HỆ THỐNG ĐANG XỬ LÝ";
    txt_title_result.hidden = true;
    img_upload.hidden = true;
    img_1.hidden = true;
    img_2.hidden = true;
    img_3.hidden = true;
    img_4.hidden = true;
    txt_result_1.hidden = true;
    txt_result_2.hidden = true;
    txt_result_3.hidden = true;
    txt_result_4.hidden = true;
    txt_message.hidden = true;

}
function upLoad() {
    var file_load = document.getElementById("file_load").files[0];
    var txt_title_result = document.getElementById("txt_title_result");
    var img_upload = document.getElementById("img_upload");
    var img_1 = document.getElementById("img_1");
    var img_2 = document.getElementById("img_2");
    var img_3 = document.getElementById("img_3");
    var img_4 = document.getElementById("img_4");
    var txt_result_1 = document.getElementById("txt_result_1");
    var txt_result_2 = document.getElementById("txt_result_2");
    var txt_result_3 = document.getElementById("txt_result_3");
    var txt_result_4 = document.getElementById("txt_result_4");
    var txt_message = document.getElementById("txt_message");
    var formData = new FormData();
	txt_message.hidden = true;
	txt_title_result.hidden = true;
	img_upload.hidden = true;
    img_1.hidden = true;
    img_2.hidden = true;
    img_3.hidden = true;
    img_4.hidden = true;
    txt_result_1.hidden = true;
    txt_result_2.hidden = true;
    txt_result_3.hidden = true;
    txt_result_4.hidden = true;
    formData.append('file', file_load);
    $.ajax({
        xhr: function () {
            var xhr = new window.XMLHttpRequest();

            xhr.upload.addEventListener('progress', function (e) {

                if (e.lengthComputable) {

                    console.log('Bytes Loaded: ' + e.loaded);
                    console.log('Total Size: ' + e.total);
                    console.log('Percentage Uploaded: ' + (e.loaded / e.total))

                    var percent = Math.round((e.loaded / e.total) * 100);
                    if (percent >= 100)
                        $('#loadbar_upload').attr('aria-valuenow', percent).css('width', percent + '%').text('Upload Successfull !');
                    else
                        $('#loadbar_upload').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');

                }

            });

            return xhr;
        },
        url: "/upload",
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        dataType: 'json',
        success: function (data_upload) {
            txt_message.hidden = false;
            if (data_upload['status'] == 'success') {
                $.ajax({
                    url: "/predict/" + data_upload['name_file_up'],
                    type: 'GET',
                    success: function (data_predict) {
                        txt_message.hidden = true;
                        txt_title_result.hidden = false;
                        img_upload.hidden = false;
                        if (data_predict['status'] == "success") {
                            img_upload.src = data_predict['url_file'];
                            console.log(data_predict['result_text'])
                            for (i = 0; i < data_predict['result_text'].length; i++) {
								if (i==0){
									img_1.hidden = false;
									txt_result_1.hidden = false;
									img_1.src = data_predict['result_text'][i][0];
									txt_result_1.innerHTML = data_predict['result_text'][i][1];
								}
								if (i==1){
									img_2.hidden = false;
									txt_result_2.hidden = false;
									img_2.src = data_predict['result_text'][i][0];
									txt_result_2.innerHTML = data_predict['result_text'][i][1];
								}
								if (i==2){
									img_3.hidden = false;
									txt_result_3.hidden = false;
									img_3.src = data_predict['result_text'][i][0];
									txt_result_3.innerHTML = data_predict['result_text'][i][1];
								}
								if (i==3){
									img_4.hidden = false;
									txt_result_4.hidden = false;
									img_4.src = data_predict['result_text'][i][0];
									txt_result_4.innerHTML = data_predict['result_text'][i][1];
								}
                            }
                        }

                    }
                });

            }
        }
    });
}
