<?php
/** 产品密钥ID，产品标识 */
define("SECRETID", "your_secret_id");
/** 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露 */
define("SECRETKEY", "your_secret_key");
/** 业务ID，易盾根据产品业务特点分配 */
define("BUSINESSID", "your_business_id");
/** 易盾短信服务发送接口地址 */
define("API_URL", "http://sms.dun.163.com/v2/sendsms");
/** api version */
define("VERSION", "v2");
/** API timeout*/
define("API_TIMEOUT", 2);
/** php内部使用的字符串编码 */
define("INTERNAL_STRING_CHARSET", "auto");
/**
 * 计算参数签名
 * $params 请求参数
 * $secretKey secretKey
 */
function gen_signature($secretKey, $params)
{
    ksort($params);
    $buff = "";
    foreach ($params as $key => $value) {
        if ($value !== null) {
            $buff .= $key;
            $buff .= $value;
        }
    }
    $buff .= $secretKey;
    return md5($buff);
}

/**
 * 将输入数据的编码统一转换成utf8
 * @params 输入的参数
 */
function toUtf8($params)
{
    $utf8s = array();
    foreach ($params as $key => $value) {
        $utf8s[$key] = is_string($value) ? mb_convert_encoding($value, "utf8", INTERNAL_STRING_CHARSET) : $value;
    }
    return $utf8s;
}

/**
 * 易盾短信发送在线检测请求接口简单封装
 * $params 请求参数
 */
function check($params)
{
    $params["secretId"] = SECRETID;
    $params["businessId"] = BUSINESSID;
    $params["version"] = VERSION;
    $params["timestamp"] = sprintf("%d", round(microtime(true) * 1000));// time in milliseconds
    $params["nonce"] = sprintf("%d", rand()); // random int
    $params = toUtf8($params);
    $params["signature"] = gen_signature(SECRETKEY, $params);
// var_dump($params);
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n",
            'method' => 'POST',
            'timeout' => API_TIMEOUT, // read timeout in seconds
            'content' => http_build_query($params),
        ),
    );
    $context = stream_context_create($options);
    $result = file_get_contents(API_URL, false, $context);
    if ($result === FALSE) {
        return array("code" => 500, "msg" => "file_get_contents failed.");
    } else {
        return json_decode($result, true);
    }
}

// 简单测试
function main()
{
    echo "mb_internal_encoding=" . mb_internal_encoding() . "\n";
	// 根据模板变量进行内容填充
	$json_param["code"] = "123";
    $params = array(
        "templateId" => "xx",
        "mobile" => "xxx",
		"paramType" => "json",
		// 转换成json字符串
        "params" => json_encode($json_param),
        // 国际短信对应的国际编码(非国际短信接入请注释掉该行代码)
        // "internationalCode" => "对应的国家编码",
    );
    $ret = check($params);
    var_dump($ret);
    if ($ret["code"] == 200) {

    } else {
        var_dump($ret); // error handler
    }
}

main();
?>