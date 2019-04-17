# coding:utf-8
__author__ = 'xxj'

import execjs


def excu_js(func_name, wanplus_token):
    ctx = execjs.compile('''
                var getToken = function(a) {
                var a;
                return token = a ? time33(a) : "",
                token
            }
              , getCookie = function(a) {
                var b = new RegExp("(^| )" + a + "=([^;]*)(;|$)");
                return val = document.cookie.match(b),
                val ? unescape(val[2]) : null
            }
              , time33 = function(a) {
                a = a.slice(0, 7);
                for (var b = 0, c = a.length, d = 5381; c > b; ++b)
                    d += (d << 5) + a.charAt(b).charCodeAt();
                return 2147483647 & d
            };
    ''')
    csrf_token = ctx.call(func_name, wanplus_token)    # 参数一：函数名；其他参数为函数中的参数。
    print 'x-csrf-token的值：', csrf_token
    return csrf_token


def main():
    excu_js('getToken', '36119a190d033d01b3703134f1eca2f2')


if __name__ == '__main__':
    main()
