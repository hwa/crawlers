null;
function injectJqueryUnderscore(page) {
    page.injectJs('./js-libs/jquery.min.js');
    return page.injectJs('./js-libs/underscore.js');
};
var webpage = require('webpage');
var system = require('system');
var fs = require('fs');
function openLoginPage(callback) {
    var page = webpage.create();
    page.onConsoleMessage = function (msg) {
        var g11286 = new Date;
        var g11287 = g11286.getFullYear() + '-' + ((g11286.getMonth() + 1 < 10 ? '0' : '') + (g11286.getMonth() + 1)) + '-' + ((g11286.getDate() < 10 ? '0' : '') + g11286.getDate()) + ' ' + ((g11286.getHours() < 10 ? '0' : '') + g11286.getHours()) + ':' + ((g11286.getMinutes() < 10 ? '0' : '') + g11286.getMinutes()) + ':' + ((g11286.getSeconds() < 10 ? '0' : '') + g11286.getSeconds()) + ':';
        return fs.write('phantom-crawler.log', g11287 + ' ' + ('Page Console >> ' + msg) + '\n', 'a');
    };
    page.settings.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17';
    return page.open('http://weibo.com/', function (status) {
        if (status === 'fail') {
            var g11290 = new Date;
            var g11291 = g11290.getFullYear() + '-' + ((g11290.getMonth() + 1 < 10 ? '0' : '') + (g11290.getMonth() + 1)) + '-' + ((g11290.getDate() < 10 ? '0' : '') + g11290.getDate()) + ' ' + ((g11290.getHours() < 10 ? '0' : '') + g11290.getHours()) + ':' + ((g11290.getMinutes() < 10 ? '0' : '') + g11290.getMinutes()) + ':' + ((g11290.getSeconds() < 10 ? '0' : '') + g11290.getSeconds()) + ':';
            return fs.write('phantom-crawler.log', g11291 + ' ' + 'failed to open page' + '\n', 'a');
        } else {
            var g11292 = new Date;
            var g11293 = g11292.getFullYear() + '-' + ((g11292.getMonth() + 1 < 10 ? '0' : '') + (g11292.getMonth() + 1)) + '-' + ((g11292.getDate() < 10 ? '0' : '') + g11292.getDate()) + ' ' + ((g11292.getHours() < 10 ? '0' : '') + g11292.getHours()) + ':' + ((g11292.getMinutes() < 10 ? '0' : '') + g11292.getMinutes()) + ':' + ((g11292.getSeconds() < 10 ? '0' : '') + g11292.getSeconds()) + ':';
            fs.write('phantom-crawler.log', g11293 + ' ' + 'Opened login page.' + '\n', 'a');
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
            var g11294 = new Date;
            var g11295 = g11294.getFullYear() + '-' + ((g11294.getMonth() + 1 < 10 ? '0' : '') + (g11294.getMonth() + 1)) + '-' + ((g11294.getDate() < 10 ? '0' : '') + g11294.getDate()) + ' ' + ((g11294.getHours() < 10 ? '0' : '') + g11294.getHours()) + ':' + ((g11294.getMinutes() < 10 ? '0' : '') + g11294.getMinutes()) + ':' + ((g11294.getSeconds() < 10 ? '0' : '') + g11294.getSeconds()) + ':';
            fs.write('phantom-crawler.log', g11295 + ' ' + ('Login as user: ' + username) + '\n', 'a');
            return callback(page);
        };
    };
    injectJqueryUnderscore(page);
    page.render('page.png');
    return page.evaluate(function (username, password) {
        jQuery.noConflict();
        return window.setTimeout(function () {
            jQuery('input[name=username]').val(username);
            jQuery('input[name=password]').val(password);
            var g11298 = document.createEvent('HTMLEvents');
            g11298.initEvent('click', true, true);
            document.querySelector('a[action-type=btn_submit] span').dispatchEvent(g11298);
            var g11296 = new Date;
            var g11297 = g11296.getFullYear() + '-' + ((g11296.getMonth() + 1 < 10 ? '0' : '') + (g11296.getMonth() + 1)) + '-' + ((g11296.getDate() < 10 ? '0' : '') + g11296.getDate()) + ' ' + ((g11296.getHours() < 10 ? '0' : '') + g11296.getHours()) + ':' + ((g11296.getMinutes() < 10 ? '0' : '') + g11296.getMinutes()) + ':' + ((g11296.getSeconds() < 10 ? '0' : '') + g11296.getSeconds()) + ':';
            var g11299 = g11297 + ' ' + 'Clicked login button.';
            console.log(g11299);
            return g11299;
        }, 300);
    }, username, password);
};
function login(username, password, userId, callback) {
    return openLoginPage(function (page) {
        return postLogin(page, username, password, userId, callback);
    });
};
function getReposts(page, url, outfile) {
    function getPosts(reposts, callback) {
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
            var reposts314 = jQuery('div[node-type=feed_list]').not('div.comment_lists').find('dl.comment_list dd').map(getPost);
            var g11300 = new Date;
            var g11301 = g11300.getFullYear() + '-' + ((g11300.getMonth() + 1 < 10 ? '0' : '') + (g11300.getMonth() + 1)) + '-' + ((g11300.getDate() < 10 ? '0' : '') + g11300.getDate()) + ' ' + ((g11300.getHours() < 10 ? '0' : '') + g11300.getHours()) + ':' + ((g11300.getMinutes() < 10 ? '0' : '') + g11300.getMinutes()) + ':' + ((g11300.getSeconds() < 10 ? '0' : '') + g11300.getSeconds()) + ':';
            var g11302 = g11301 + ' ' + ('got ' + reposts314.length + ' reposts.');
            console.log(g11302);
            g11302;
            return reposts314.toArray();
        };
        var hasNextPagewhat = function () {
            if (0 !== jQuery('a.btn_page_next').length) {
                return jQuery('a.btn_page_next span').last()[0];
            } else if ('\u4E0B\u4E00\u9875' === jQuery('span[action-type=feed_list_page]').last().text().trim()) {
                return jQuery('span[action-type=feed_list_page]').last()[0];
            } else {
                return false;
            };
        };
        var clickNextPage = function () {
            var g11303 = document.createEvent('HTMLEvents');
            g11303.initEvent('click', true, true);
            return hasNextPagewhat().dispatchEvent(g11303);
        };
        var printPost = function (c) {
            var g11304 = c.username + '\t' + c.repostNum;
            console.log(g11304);
            return g11304;
        };
        var getPostsstar = function () {
            var repostsstar = reposts.concat(getPagePosts());
            if (hasNextPagewhat()) {
                clickNextPage();
                return window.setTimeout(function (getPosts) {
                    var g11305 = window.location.href;
                    console.log(g11305);
                    g11305;
                    return getPosts(repostsstar, callback);
                }, 1500, getPosts);
            } else {
                return callback(repostsstar);
            };
        };
        return window.setTimeout(getPostsstar, 1500);
    };
    var goFirstPage = function (url) {
        return window.location.href = url;
    };
    page.onLoadFinished = function () {
        injectJqueryUnderscore(page);
        page.evaluate(getPosts, [], function (reposts) {
            var g11306 = 'Got total ' + reposts.length + ' reposts';
            console.log(g11306);
            g11306;
            window.callPhantom(reposts);
            return window.reposts = reposts;
        });
        return page.onLoadFinished = null;
    };
    page.onCallback = function (reposts) {
        fs.write(outfile, JSON.stringify(reposts));
        var g11307 = page.url;
        console.log(g11307);
        g11307;
        page.render('page.png');
        return phantom.exit();
    };
    return page.evaluate(goFirstPage, url);
};
function openDirectly(userId, onsuccess, onfailed) {
    var page = webpage.create();
    page.onResourceRequested = function (rq, nd) {
        if ('http://weibo.com/aj/mblog/info/big' === rq.url.slice(0, 34)) {
            var g11309 = rq.url;
            console.log(g11309);
            g11309;
            return phantom.exit();
        };
    };
    page.onConsoleMessage = function (msg) {
        var g11310 = new Date;
        var g11311 = g11310.getFullYear() + '-' + ((g11310.getMonth() + 1 < 10 ? '0' : '') + (g11310.getMonth() + 1)) + '-' + ((g11310.getDate() < 10 ? '0' : '') + g11310.getDate()) + ' ' + ((g11310.getHours() < 10 ? '0' : '') + g11310.getHours()) + ':' + ((g11310.getMinutes() < 10 ? '0' : '') + g11310.getMinutes()) + ':' + ((g11310.getSeconds() < 10 ? '0' : '') + g11310.getSeconds()) + ':';
        return fs.write('phantom-crawler.log', g11311 + ' ' + ('Page Console >> ' + msg) + '\n', 'a');
    };
    page.settings.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17';
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
    var g11312 = new Date;
    var g11313 = g11312.getFullYear() + '-' + ((g11312.getMonth() + 1 < 10 ? '0' : '') + (g11312.getMonth() + 1)) + '-' + ((g11312.getDate() < 10 ? '0' : '') + g11312.getDate()) + ' ' + ((g11312.getHours() < 10 ? '0' : '') + g11312.getHours()) + ':' + ((g11312.getMinutes() < 10 ? '0' : '') + g11312.getMinutes()) + ':' + ((g11312.getSeconds() < 10 ? '0' : '') + g11312.getSeconds()) + ':';
    fs.write('phantom-crawler.log', g11313 + ' ' + ('Crawling reposts of weibo: ' + url) + '\n', 'a');
    return openDirectly(userid, function (page) {
        var g11314 = new Date;
        var g11315 = g11314.getFullYear() + '-' + ((g11314.getMonth() + 1 < 10 ? '0' : '') + (g11314.getMonth() + 1)) + '-' + ((g11314.getDate() < 10 ? '0' : '') + g11314.getDate()) + ' ' + ((g11314.getHours() < 10 ? '0' : '') + g11314.getHours()) + ':' + ((g11314.getMinutes() < 10 ? '0' : '') + g11314.getMinutes()) + ':' + ((g11314.getSeconds() < 10 ? '0' : '') + g11314.getSeconds()) + ':';
        fs.write('phantom-crawler.log', g11315 + ' ' + ('Auto login directly, url now: ' + page.url) + '\n', 'a');
        page.onLoadFinished = null;
        return getReposts(page, url, outfile);
    }, function (page) {
        var g11316 = new Date;
        var g11317 = g11316.getFullYear() + '-' + ((g11316.getMonth() + 1 < 10 ? '0' : '') + (g11316.getMonth() + 1)) + '-' + ((g11316.getDate() < 10 ? '0' : '') + g11316.getDate()) + ' ' + ((g11316.getHours() < 10 ? '0' : '') + g11316.getHours()) + ':' + ((g11316.getMinutes() < 10 ? '0' : '') + g11316.getMinutes()) + ':' + ((g11316.getSeconds() < 10 ? '0' : '') + g11316.getSeconds()) + ':';
        fs.write('phantom-crawler.log', g11317 + ' ' + ('Failed to auto login, url now: ' + page.url) + '\n', 'a');
        page.render('page.png');
        page.onLoadFinished = null;
        var g11318 = new Date;
        var g11319 = g11318.getFullYear() + '-' + ((g11318.getMonth() + 1 < 10 ? '0' : '') + (g11318.getMonth() + 1)) + '-' + ((g11318.getDate() < 10 ? '0' : '') + g11318.getDate()) + ' ' + ((g11318.getHours() < 10 ? '0' : '') + g11318.getHours()) + ':' + ((g11318.getMinutes() < 10 ? '0' : '') + g11318.getMinutes()) + ':' + ((g11318.getSeconds() < 10 ? '0' : '') + g11318.getSeconds()) + ':';
        fs.write('phantom-crawler.log', g11319 + ' ' + 'Try relogin.' + '\n', 'a');
        return login(username, password, userid, function (page2) {
            return getReposts(page2, url, outfile);
        });
    });
};
crawl_repost(system.args[1], system.args[2]);
