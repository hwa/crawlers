null;
function injectJqueryUnderscore(page) {
    page.injectJs('./js-libs/jquery.min.js');
    return page.injectJs('./js-libs/underscore.js');
};
var webpage = require('webpage');
var system = require('system');
var fs = require('fs');
var USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17';
function newPage() {
    var page = webpage.create();
    page.onConsoleMessage = function (msg) {
        var g14107 = new Date;
        var g14108 = g14107.getFullYear() + '-' + ((g14107.getMonth() + 1 < 10 ? '0' : '') + (g14107.getMonth() + 1)) + '-' + ((g14107.getDate() < 10 ? '0' : '') + g14107.getDate()) + ' ' + ((g14107.getHours() < 10 ? '0' : '') + g14107.getHours()) + ':' + ((g14107.getMinutes() < 10 ? '0' : '') + g14107.getMinutes()) + ':' + ((g14107.getSeconds() < 10 ? '0' : '') + g14107.getSeconds()) + ':';
        return fs.write('phantom-crawler.log', g14108 + ' ' + ('Page Console >> ' + msg) + '\n', 'a');
    };
    page.settings.userAgent = USERAGENT;
    return page;
};
function openLoginPage(callback) {
    var page = newPage();
    return page.open('http://weibo.com/', function (status) {
        if (status === 'fail') {
            var g14111 = new Date;
            var g14112 = g14111.getFullYear() + '-' + ((g14111.getMonth() + 1 < 10 ? '0' : '') + (g14111.getMonth() + 1)) + '-' + ((g14111.getDate() < 10 ? '0' : '') + g14111.getDate()) + ' ' + ((g14111.getHours() < 10 ? '0' : '') + g14111.getHours()) + ':' + ((g14111.getMinutes() < 10 ? '0' : '') + g14111.getMinutes()) + ':' + ((g14111.getSeconds() < 10 ? '0' : '') + g14111.getSeconds()) + ':';
            return fs.write('phantom-crawler.log', g14112 + ' ' + 'failed to open page' + '\n', 'a');
        } else {
            var g14113 = new Date;
            var g14114 = g14113.getFullYear() + '-' + ((g14113.getMonth() + 1 < 10 ? '0' : '') + (g14113.getMonth() + 1)) + '-' + ((g14113.getDate() < 10 ? '0' : '') + g14113.getDate()) + ' ' + ((g14113.getHours() < 10 ? '0' : '') + g14113.getHours()) + ':' + ((g14113.getMinutes() < 10 ? '0' : '') + g14113.getMinutes()) + ':' + ((g14113.getSeconds() < 10 ? '0' : '') + g14113.getSeconds()) + ':';
            fs.write('phantom-crawler.log', g14114 + ' ' + 'Opened login page.' + '\n', 'a');
            return callback(page);
        };
    });
};
function postLogin(page, username, password, userId, callback) {
    page.onLoadFinished = function () {
        var url = page.evaluate(function () {
            return window.location.href;
        });
        if ('http://weibo.com/u/' + userId === url.split('?')[0]) {
            page.onLoadFinished = null;
            var g14115 = new Date;
            var g14116 = g14115.getFullYear() + '-' + ((g14115.getMonth() + 1 < 10 ? '0' : '') + (g14115.getMonth() + 1)) + '-' + ((g14115.getDate() < 10 ? '0' : '') + g14115.getDate()) + ' ' + ((g14115.getHours() < 10 ? '0' : '') + g14115.getHours()) + ':' + ((g14115.getMinutes() < 10 ? '0' : '') + g14115.getMinutes()) + ':' + ((g14115.getSeconds() < 10 ? '0' : '') + g14115.getSeconds()) + ':';
            fs.write('phantom-crawler.log', g14116 + ' ' + ('Login as user: ' + username) + '\n', 'a');
            return callback(page);
        };
    };
    injectJqueryUnderscore(page);
    return page.evaluate(function (username, password) {
        jQuery.noConflict();
        return window.setTimeout(function () {
            jQuery('input[name=username]').val(username);
            jQuery('input[name=password]').val(password);
            var g14119 = document.createEvent('HTMLEvents');
            g14119.initEvent('click', true, true);
            document.querySelector('a[action-type=btn_submit] span').dispatchEvent(g14119);
            var g14117 = new Date;
            var g14118 = g14117.getFullYear() + '-' + ((g14117.getMonth() + 1 < 10 ? '0' : '') + (g14117.getMonth() + 1)) + '-' + ((g14117.getDate() < 10 ? '0' : '') + g14117.getDate()) + ' ' + ((g14117.getHours() < 10 ? '0' : '') + g14117.getHours()) + ':' + ((g14117.getMinutes() < 10 ? '0' : '') + g14117.getMinutes()) + ':' + ((g14117.getSeconds() < 10 ? '0' : '') + g14117.getSeconds()) + ':';
            var g14120 = g14118 + ' ' + 'Clicked login button.';
            console.log(g14120);
            return g14120;
        }, 300);
    }, username, password);
};
function login(username, password, userId, callback) {
    return openLoginPage(function (page) {
        return postLogin(page, username, password, userId, callback);
    });
};
function getReposts(page, url, outfile) {
    function getPosts() {
        var parseDate = function (str) {
            var fulldate = new RegExp('(\\d+)-(\\d+)-(\\d+) (\\d+):(\\d+)');
            var dateParts = fulldate.exec(str);
            var minutesAgo = new RegExp('(\\d+)\\u5206\\u949f\\u524d');
            var minutes = minutesAgo.exec(str);
            var today = new RegExp('\\u4eca\\u5929 (\\d+):(\\d+)');
            var hourMinute = today.exec(str);
            var now = new Date();
            if (dateParts) {
                return new Date(dateParts[1], dateParts[2] - 1, dateParts[3], dateParts[4], dateParts[5]);
            } else if (minutesAgo) {
                var time = new Date(now.getTime() - minutes);
                return new Date(time.getFullYear(), time.getMonth(), time.getDate(), time.getHours(), time.getMinutes());
            } else if (hourMinute) {
                return new Date(now.getFullYear(), now.getMonth(), now.getDate(), hourMinute[1], hourMinute[2]);
            };
        };
        var getTime = function (el) {
            var txt = jQuery('span', el).first().text();
            var dtxt = txt.slice(1, txt.length - 1);
            return parseDate(dtxt).getTime();
        };
        var getRepostNum = function (el) {
            var txt = jQuery('a[action-data]', el).text();
            return 2 < txt.length ? parseInt(txt.slice(3, txt.length - 1)) : 0;
        };
        var getRepostUrl = function (el) {
            var actionData = jQuery('a[action-type=feed_list_forward]', el).attr('action-data');
            var re = new RegExp('&url=([^&]+)');
            return re.exec(actionData)[1];
        };
        var getPost = function () {
            return { 'username' : jQuery('a', this).first().text(),
                     'msg' : jQuery('em', this).first().text(),
                     'time' : getTime(this),
                     'repost-num' : getRepostNum(this),
                     'repost-url' : getRepostUrl()
                   };
        };
        var getPagePosts = function () {
            var g14121 = jQuery('dd').length;
            console.log(g14121);
            g14121;
            var reposts = jQuery('div[node-type=feed_list]').not('div.comment_lists').find('dl.comment_list dd').map(getPost);
            var g14122 = new Date;
            var g14123 = g14122.getFullYear() + '-' + ((g14122.getMonth() + 1 < 10 ? '0' : '') + (g14122.getMonth() + 1)) + '-' + ((g14122.getDate() < 10 ? '0' : '') + g14122.getDate()) + ' ' + ((g14122.getHours() < 10 ? '0' : '') + g14122.getHours()) + ':' + ((g14122.getMinutes() < 10 ? '0' : '') + g14122.getMinutes()) + ':' + ((g14122.getSeconds() < 10 ? '0' : '') + g14122.getSeconds()) + ':';
            var g14124 = g14123 + ' ' + ('got ' + reposts.length + ' reposts.');
            console.log(g14124);
            g14124;
            return reposts.toArray();
        };
        return getPagePosts();
    };
    function hasNextPagewhat() {
        if (0 !== jQuery('a.btn_page_next').length) {
            return jQuery('a.btn_page_next span').last()[0];
        } else if ('\u4E0B\u4E00\u9875' === jQuery('span[action-type=feed_list_page]').last().text().trim()) {
            return jQuery('span[action-type=feed_list_page]').last()[0];
        } else {
            return false;
        };
    };
    function clickNextPage() {
        var hasNextPagewhat = function () {
            if (0 !== jQuery('a.btn_page_next').length) {
                return jQuery('a.btn_page_next span').last()[0];
            } else if ('\u4E0B\u4E00\u9875' === jQuery('span[action-type=feed_list_page]').last().text().trim()) {
                return jQuery('span[action-type=feed_list_page]').last()[0];
            } else {
                return false;
            };
        };
        var g14125 = document.createEvent('HTMLEvents');
        g14125.initEvent('click', true, true);
        return hasNextPagewhat().dispatchEvent(g14125);
    };
    var writeOut = function (data) {
        var g14126 = new Date;
        var g14127 = g14126.getFullYear() + '-' + ((g14126.getMonth() + 1 < 10 ? '0' : '') + (g14126.getMonth() + 1)) + '-' + ((g14126.getDate() < 10 ? '0' : '') + g14126.getDate()) + ' ' + ((g14126.getHours() < 10 ? '0' : '') + g14126.getHours()) + ':' + ((g14126.getMinutes() < 10 ? '0' : '') + g14126.getMinutes()) + ':' + ((g14126.getSeconds() < 10 ? '0' : '') + g14126.getSeconds()) + ':';
        fs.write('phantom-crawler.log', g14127 + ' ' + ('Got total ' + data.reposts.length + ' reposts') + '\n', 'a');
        fs.write(outfile, JSON.stringify(data));
        return phantom.exit();
    };
    page.onResourceRequested = function (rq, nd) {
        return 'http://weibo.com/aj/mblog/info/big' === rq.url.slice(0, 34) ? writeOut({ 'reposts' : [], 'next-page-url' : rq.url }) : null;
    };
    page.onLoadFinished = function () {
        injectJqueryUnderscore(page);
        return page.evaluate(clickNextPage);
    };
    return page.evaluate(function (url) {
        return window.location.href = url;
    }, url);
};
function openDirectly(userId, onsuccess, onfailed) {
    var page = newPage();
    page.onLoadFinished = function () {
        if (page.title === '') {
            page.reload();
        };
        if ('http://weibo.com/u' === page.url.slice(0, 18)) {
            page.logging = null;
            onsuccess(page);
        };
        return 'http://weibo.com/signup/' === page.url.slice(0, 24) ? onfailed(page) : null;
    };
    return page.open('http://weibo.com/u/' + userId);
};
function crawl_repost(url, outfile) {
    var username = 'cheng.zhang@gmail.com';
    var password = '1qa2ws';
    var userid = '3240189394';
    var g14128 = new Date;
    var g14129 = g14128.getFullYear() + '-' + ((g14128.getMonth() + 1 < 10 ? '0' : '') + (g14128.getMonth() + 1)) + '-' + ((g14128.getDate() < 10 ? '0' : '') + g14128.getDate()) + ' ' + ((g14128.getHours() < 10 ? '0' : '') + g14128.getHours()) + ':' + ((g14128.getMinutes() < 10 ? '0' : '') + g14128.getMinutes()) + ':' + ((g14128.getSeconds() < 10 ? '0' : '') + g14128.getSeconds()) + ':';
    fs.write('phantom-crawler.log', g14129 + ' ' + ('Crawling reposts of weibo: ' + url) + '\n', 'a');
    return openDirectly(userid, function (page) {
        var g14130 = new Date;
        var g14131 = g14130.getFullYear() + '-' + ((g14130.getMonth() + 1 < 10 ? '0' : '') + (g14130.getMonth() + 1)) + '-' + ((g14130.getDate() < 10 ? '0' : '') + g14130.getDate()) + ' ' + ((g14130.getHours() < 10 ? '0' : '') + g14130.getHours()) + ':' + ((g14130.getMinutes() < 10 ? '0' : '') + g14130.getMinutes()) + ':' + ((g14130.getSeconds() < 10 ? '0' : '') + g14130.getSeconds()) + ':';
        fs.write('phantom-crawler.log', g14131 + ' ' + ('Auto login directly, url now: ' + page.url) + '\n', 'a');
        page.onLoadFinished = null;
        return getReposts(page, url, outfile);
    }, function (page) {
        var g14132 = new Date;
        var g14133 = g14132.getFullYear() + '-' + ((g14132.getMonth() + 1 < 10 ? '0' : '') + (g14132.getMonth() + 1)) + '-' + ((g14132.getDate() < 10 ? '0' : '') + g14132.getDate()) + ' ' + ((g14132.getHours() < 10 ? '0' : '') + g14132.getHours()) + ':' + ((g14132.getMinutes() < 10 ? '0' : '') + g14132.getMinutes()) + ':' + ((g14132.getSeconds() < 10 ? '0' : '') + g14132.getSeconds()) + ':';
        fs.write('phantom-crawler.log', g14133 + ' ' + ('Failed to auto login, url now: ' + page.url) + '\n', 'a');
        page.onLoadFinished = null;
        var g14134 = new Date;
        var g14135 = g14134.getFullYear() + '-' + ((g14134.getMonth() + 1 < 10 ? '0' : '') + (g14134.getMonth() + 1)) + '-' + ((g14134.getDate() < 10 ? '0' : '') + g14134.getDate()) + ' ' + ((g14134.getHours() < 10 ? '0' : '') + g14134.getHours()) + ':' + ((g14134.getMinutes() < 10 ? '0' : '') + g14134.getMinutes()) + ':' + ((g14134.getSeconds() < 10 ? '0' : '') + g14134.getSeconds()) + ':';
        fs.write('phantom-crawler.log', g14135 + ' ' + 'Try relogin.' + '\n', 'a');
        return login(username, password, userid, function (page2) {
            return getReposts(page2, url, outfile);
        });
    });
};
crawl_repost(system.args[1], system.args[2]);
