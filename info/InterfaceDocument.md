


#### 接口No.1

- 登陆接口

##### 请求URL
- ` /login/ `
##### 请求方式
- POST 

##### 请求参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|worknumber |是  |string |登陆工号   |
|password |是  |string |登陆密码   |

##### 返回示例 

###### 登陆成功
``` 
{
    "error": "0",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MjMzMTU1NTgsIndvcmtudW1iZXIiOiJGNzY5MTcxNyIsImlzX3JlZnJlc2giOnRydWV9.fQC0bL1axSgpQcv8L0bII0QIB2UiBeD3q208UORGIKs",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MjIxMTMxNTgsIndvcmtudW1iZXIiOiJGNzY5MTcxNyJ9.q7jFIuUqNWgUz853rJNhhJD-XphJO2UStVzc-AHPtfE"
}
```

###### 用户不存在(密码错误)
```
{
    "errmsg": "用户不存在",
    "error": "4001"
}
```

###### 查询用户对象异常

```
{
    "errmsg": "查询用户对象异常",
    "error": "4001"
}
```


###### 查询用户对象异常

```
{
    "errmsg": "參數不足",
    "error": "4003"
}
```


##### 