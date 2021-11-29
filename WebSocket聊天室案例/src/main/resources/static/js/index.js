
function login() {
    var data = {};
    data['username'] = $('#uname').val();
    data['password'] = $('#pwd').val();
    $.ajaxSetup({contentType: "application/json; charset=utf-8"})
    /**
     * JSON.stringify() 方法用于将 JavaScript 值转换为 JSON 字符串。
     */
    $.post("login", JSON.stringify(data), function (res) {
        if (res.flag){
            location.href = 'toChatroom';  //location.href;当前页面打开URL页面
        }else {
            alert(JSON.stringify(res));
        }
    }, 'json');
}
/**
 *$.post中的res指的是LoginController的 public Result login(@RequestBody User user, HttpSession session)
 * 返回的result,Result类中有flag和message两个类。res.flag用于提取返回过来flag值。
 *
 */