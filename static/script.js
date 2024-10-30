var Cookie = new Object();

Cookie.set = function(name, value, expires) {
        document.cookie = name + "=" + escape(value) +
                        "; expires=" + expires +
                        "; domain=" + document.domain +
                        "; secure";
    }
Cookie.get = function(name) {
        var prefix = name + "=";
        var cookieStartIndex = document.cookie.indexOf(prefix);
        if (cookieStartIndex == -1) return null;
        var cookieEndIndex = document.cookie.indexOf(";", cookieStartIndex + prefix.length);
        if (cookieEndIndex == -1) cookieEndIndex = document.cookie.length;
        return unescape(document.cookie.substring(cookieStartIndex + prefix.length, cookieEndIndex));
    }

var main = document.getElementById('main');
var alarm = document.getElementById('alarm');

var myVar = null;
myVar = Cookie.get("WratixorAdult");

const initFunc = () => {
        main = document.getElementById('main');
        alarm = document.getElementById('alarm');
        if (myVar != "1") {
            alarm.style.setProperty('display', 'block');
            main.style.setProperty('display', 'none');
        }
    }

const clickYes = () => {
        Cookie.set("WratixorAdult", "1", new Date(new Date().getTime()+30*24*60*60*1000));
        alarm.style.setProperty('display', 'none');
        main.style.setProperty('display', 'block');
    }

const clickNo = () => {
        alarm.style.setProperty('display', 'none');
        main.style.setProperty('display', 'block');
        location.href = "/";
    }
