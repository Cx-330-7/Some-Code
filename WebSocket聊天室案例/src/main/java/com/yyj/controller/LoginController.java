package com.yyj.controller;

import com.yyj.pojo.Result;
import com.yyj.pojo.User;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpSession;


@Controller
public class LoginController {

    @Value("${login.test.password}")//在application.yml文件中
    private String password;

    /**
     * 处理用户登录请求.
     * @param user 用户登录数据
     * @param session session对象
     * @return com.yyj.pojo.Result
     */
    @PostMapping(value = "/login")
    @ResponseBody
    /**
     * @ResponseBody说明这个方法返回的东西会通过IO流的方式写入到浏览器。
     * 将java对象转为json格式的数据。
     */
    /**
     * @RequestBody:可以将index.js中的ajax里传来的数据「JSON.stringify(data)」绑定到相应的bean上，
     * 在这里就将 data['username'] = $('#uname').val();data['password'] = $('#pwd').val();绑定给User。
     */
    public Result login(@RequestBody User user, HttpSession session) {
        Result result = new Result();
        if (user!= null & password != null & password.equals(user.getPassword())) {
             result.setFlag(true);
             result.setMessage("登录成功！");
             session.setAttribute("username", user.getUsername());
         }else {
            result.setMessage("登录失败！");
            result.setFlag(false);
        }
        return result;
    }

    /**
     * 登录成功后跳转到聊天页面.
     */
    @GetMapping(value = "/toChatroom")
    public String toChatroom() {
        return "chat";
    }

    /**
     * 获取登录成功后存放在session域中的值.
     * @param session
     */
    @GetMapping("/getUsername")
    @ResponseBody
    public String getUsername(HttpSession session){
        return (String) session.getAttribute("username");
    }

}
