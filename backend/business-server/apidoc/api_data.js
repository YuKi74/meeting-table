define({ "api": [
  {
    "type": "patch",
    "url": "/user/",
    "title": "用户修改个人信息",
    "name": "update_information",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String[1..32]",
            "optional": true,
            "field": "name",
            "description": "<p>用户名</p>"
          },
          {
            "group": "Parameter",
            "type": "String[1..128]",
            "optional": true,
            "field": "password",
            "description": "<p>用户密码</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<p>后续发请求都要携带</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "user/views.py",
    "groupTitle": "User"
  },
  {
    "type": "get",
    "url": "/user/",
    "title": "用户个人信息",
    "name": "update_information",
    "group": "User",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "information",
            "description": "<p>用户个人信息</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "user/views.py",
    "groupTitle": "User"
  },
  {
    "type": "get",
    "url": "/user/:id",
    "title": "用户获取其他用户信息",
    "examples": [
      {
        "title": "请求路径示例",
        "content": "http://localhost/user/1",
        "type": "json"
      }
    ],
    "name": "user_information",
    "group": "User",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "user_information",
            "description": "<p>用户信息</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "user/views.py",
    "groupTitle": "User"
  },
  {
    "type": "post",
    "url": "/user/login/",
    "title": "用户登录",
    "name": "user_login",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>用户邮箱</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>用户密码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"email\":\"test@qq.com\",\n    \"password\":\"123456\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<p>后续发请求都要携带</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "user/views.py",
    "groupTitle": "User"
  },
  {
    "type": "post",
    "url": "/user/register/",
    "title": "用户注册",
    "name": "user_register",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>用户名</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>用户邮箱</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>用户密码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"name\":\"gan\",\n    \"email\":\"test@qq.com\",\n    \"password\":\"123456\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<p>后续发请求都要携带</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "user/views.py",
    "groupTitle": "User"
  }
] });
