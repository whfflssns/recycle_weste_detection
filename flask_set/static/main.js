$(document).ready(function()  {
    src="lodash.js";
    $(document).keyup(function(event){  // keyup 이벤트 처리 enter, backspace
          var keycode = (event.keyCode ? event.keyCode : event.which);
          if(keycode == '13') timer();
        });

        function timer() {
          setInterval(regist, 630);
          }
        var see_one = [];
        var count1 = 0;
        var count2 = 0;
        var size_0 = 0;
        var before_class = [];

        function regist() {
            $.ajax({
                url: "/getlabel",
                method: "GET"
                }).done(function(r, a) {
                $('#label').empty();
                var result = r.split('AAAA');
                var class_name = [];
                var confiden = [];
                result.pop();

                for (var i in result){
                    class_name.push(result[i].split(',')[0]);
                    confiden.push(result[i].split(',')[1]);
                }

                if (class_name.length == 0) {
                    count2 += 1;
                }
                else {
                    count2 = 0;
                }

                if (size_0 == result.length) {
                    same_value = before_class.length;
                    count_value = 0;
                    for (var i in before_class) {
                        if (before_class[i] == class_name[i])
                            count_value += 1;
                    }
                    if (same_value == count_value) count1 += 1;
                    else count1 = 0;
                }
                else {
                    size_0 = result.length;
                    before_class = class_name;
                    count1 = 0;
                }

                if (count1 > 35 || count2 > 20) {
                    location.href = "/";
                }
                console.log(count1);
                see_one = class_name[0];

                for (var i in result) {
                  $('#label').append( '<button style="outline: none; height: 40px; text-align: center; width: 130px; border-radius: 40px; background-color: #fff; border: 2px solid black;letter-spacing:1px;text-shadow:0;font-size: 12px;font-weight: bold;color: black; cursor: pointer;" type="button" name="result_check" value="label'+i+'">' + class_name[i] + '\n'+ confiden[i]+ '</button><br>');
                }
                if (see_one != undefined) {
                    if (see_one == 'plastic') {
                        pl();
                        gl_out();
                        pp_out();
                        nr_out();
                        mt_out();
                    }
                    else if (see_one == 'paper') {
                        pl_out();
                        gl_out();
                        pp();
                        nr_out();
                        mt_out();
                    }
                    else if (see_one == 'metal') {
                        pl_out();
                        gl_out();
                        pp_out();
                        nr_out();
                        mt();
                    }
                    else if (see_one == 'glass') {
                        pl_out();
                        gl();
                        pp_out();
                        nr_out();
                        mt_out();
                    }
                    else if (see_one == 'normal') {
                        pl_out();
                        gl_out();
                        pp_out();
                        nr();
                        mt_out();
                    }
                }
                else {
                        pl_out();
                        gl_out();
                        pp_out();
                        nr_out();
                        mt_out();
                }

                console.log("ajax-getLabel-success");

                }).fail(function() {
                console.log("ajax-getLabel-fail");
            });
        }

        // 불이 나가고 들어오는지 확인하기 위하여 hover부분 사용
		function pl(){
			document.getElementById("triangle_pl").style.borderTopColor = "rgb(0,0,255)"; // 플라스틱 색 변경 js code
		}

		function pl_out(){
			document.getElementById("triangle_pl").style.borderTopColor = "white"; // 플라스틱 색 원상복구
		}

		function gl(){
			document.getElementById("triangle_gl").style.borderTopColor = "rgb(255,255,0)"; // 유리 색 변경 js code
		}

		function gl_out(){
			document.getElementById("triangle_gl").style.borderTopColor = "white"; // 유리 색 원상복구
		}

		function nr(){
			document.getElementById("triangle_nr").style.borderTopColor = "rgb(255,0,255)"; // 일반쓰레기 색 변경 js code
		}

		function nr_out(){
			document.getElementById("triangle_nr").style.borderTopColor = "white"; // 일반쓰레기 색 원상복구
		}

		function pp(){
			document.getElementById("triangle_pp").style.borderTopColor = "rgb(0,255,0)"; // 종이 색 변경 js code
		}

		function pp_out(){
			document.getElementById("triangle_pp").style.borderTopColor = "white"; // 종이 색 원상복구
		}

		function mt(){
			document.getElementById("triangle_mt").style.borderTopColor = "rgb(255,0,0)"; // 금속 색 변경 js code
		}

		function mt_out(){
			document.getElementById("triangle_mt").style.borderTopColor = "white"; // 금속 색 원상복구
		}
});