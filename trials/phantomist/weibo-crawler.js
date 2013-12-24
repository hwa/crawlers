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
        var g12376 = new Date;
        var g12377 = g12376.getFullYear() + '-' + ((g12376.getMonth() + 1 < 10 ? '0' : '') + (g12376.getMonth() + 1)) + '-' + ((g12376.getDate() < 10 ? '0' : '') + g12376.getDate()) + ' ' + ((g12376.getHours() < 10 ? '0' : '') + g12376.getHours()) + ':' + ((g12376.getMinutes() < 10 ? '0' : '') + g12376.getMinutes()) + ':' + ((g12376.getSeconds() < 10 ? '0' : '') + g12376.getSeconds()) + ':';
        return fs.write('phantom-crawler.log', g12377 + ' ' + ('Page Console >> ' + msg) + '\n', 'a');
    };
    page.settings.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17';
    return page.open('http://weibo.com/', function (status) {
        if (status === 'fail') {
            var g12380 = new Date;
            var g12381 = g12380.getFullYear() + '-' + ((g12380.getMonth() + 1 < 10 ? '0' : '') + (g12380.getMonth() + 1)) + '-' + ((g12380.getDate() < 10 ? '0' : '') + g12380.getDate()) + ' ' + ((g12380.getHours() < 10 ? '0' : '') + g12380.getHours()) + ':' + ((g12380.getMinutes() < 10 ? '0' : '') + g12380.getMinutes()) + ':' + ((g12380.getSeconds() < 10 ? '0' : '') + g12380.getSeconds()) + ':';
            return fs.write('phantom-crawler.log', g12381 + ' ' + 'failed to open page' + '\n', 'a');
        } else {
            var g12382 = new Date;
            var g12383 = g12382.getFullYear() + '-' + ((g12382.getMonth() + 1 < 10 ? '0' : '') + (g12382.getMonth() + 1)) + '-' + ((g12382.getDate() < 10 ? '0' : '') + g12382.getDate()) + ' ' + ((g12382.getHours() < 10 ? '0' : '') + g12382.getHours()) + ':' + ((g12382.getMinutes() < 10 ? '0' : '') + g12382.getMinutes()) + ':' + ((g12382.getSeconds() < 10 ? '0' : '') + g12382.getSeconds()) + ':';
            fs.write('phantom-crawler.log', g12383 + ' ' + 'Opened login page.' + '\n', 'a');
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
            var g12384 = new Date;
            var g12385 = g12384.getFullYear() + '-' + ((g12384.getMonth() + 1 < 10 ? '0' : '') + (g12384.getMonth() + 1)) + '-' + ((g12384.getDate() < 10 ? '0' : '') + g12384.getDate()) + ' ' + ((g12384.getHours() < 10 ? '0' : '') + g12384.getHours()) + ':' + ((g12384.getMinutes() < 10 ? '0' : '') + g12384.getMinutes()) + ':' + ((g12384.getSeconds() < 10 ? '0' : '') + g12384.getSeconds()) + ':';
            fs.write('phantom-crawler.log', g12385 + ' ' + ('Login as user: ' + username) + '\n', 'a');
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
            var g12388 = document.createEvent('HTMLEvents');
            g12388.initEvent('click', true, true);
            document.querySelector('a[action-type=btn_submit] span').dispatchEvent(g12388);
            var g12386 = new Date;
            var g12387 = g12386.getFullYear() + '-' + ((g12386.getMonth() + 1 < 10 ? '0' : '') + (g12386.getMonth() + 1)) + '-' + ((g12386.getDate() < 10 ? '0' : '') + g12386.getDate()) + ' ' + ((g12386.getHours() < 10 ? '0' : '') + g12386.getHours()) + ':' + ((g12386.getMinutes() < 10 ? '0' : '') + g12386.getMinutes()) + ':' + ((g12386.getSeconds() < 10 ? '0' : '') + g12386.getSeconds()) + ':';
            var g12389 = g12387 + ' ' + 'Clicked login button.';
            console.log(g12389);
            return g12389;
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
                     'repost-url' : getRepostUrl(this)
                   };
        };
        var getPagePosts = function () {
            var reposts326 = jQuery('div[node-type=feed_list]').not('div.comment_lists').find('dl.comment_list dd').map(getPost);
            var g12390 = new Date;
            var g12391 = g12390.getFullYear() + '-' + ((g12390.getMonth() + 1 < 10 ? '0' : '') + (g12390.getMonth() + 1)) + '-' + ((g12390.getDate() < 10 ? '0' : '') + g12390.getDate()) + ' ' + ((g12390.getHours() < 10 ? '0' : '') + g12390.getHours()) + ':' + ((g12390.getMinutes() < 10 ? '0' : '') + g12390.getMinutes()) + ':' + ((g12390.getSeconds() < 10 ? '0' : '') + g12390.getSeconds()) + ':';
            var g12392 = g12391 + ' ' + ('got ' + reposts326.length + ' reposts.');
            console.log(g12392);
            g12392;
            return reposts326.toArray();
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
            var g12393 = document.createEvent('HTMLEvents');
            g12393.initEvent('click', true, true);
            return hasNextPagewhat().dispatchEvent(g12393);
        };
        var printPost = function (c) {
            var g12394 = c.username + '\t' + c.repostNum;
            console.log(g12394);
            return g12394;
        };
        var getPostsstar = function () {
            var repostsstar = reposts.concat(getPagePosts());
            if (hasNextPagewhat()) {
                clickNextPage();
                return window.setTimeout(function (getPosts) {
                    var g12395 = window.location.href;
                    console.log(g12395);
                    g12395;
                    return getPosts(repostsstar, callback);
                }, 3000, getPosts);
            } else {
                return callback(repostsstar);
            };
        };
        return window.setTimeout(getPostsstar, 3000);
    };
    var goFirstPage = function (url) {
        return window.location.href = url;
    };
    page.onLoadFinished = function () {
        injectJqueryUnderscore(page);
        page.evaluate(getPosts, [], function (reposts) {
            var g12396 = 'Got total ' + reposts.length + ' reposts';
            console.log(g12396);
            g12396;
            window.callPhantom(reposts);
            return window.reposts = reposts;
        });
        return page.onLoadFinished = null;
    };
    page.onCallback = function (reposts) {
        fs.write(outfile, JSON.stringify(reposts));
        var g12397 = page.url;
        console.log(g12397);
        g12397;
        page.render('page.png');
        return phantom.exit();
    };
    return page.evaluate(goFirstPage, url);
};
function openDirectly(userId, onsuccess, onfailed) {
    var page = webpage.create();
    page.onConsoleMessage = function (msg) {
        var g12398 = new Date;
        var g12399 = g12398.getFullYear() + '-' + ((g12398.getMonth() + 1 < 10 ? '0' : '') + (g12398.getMonth() + 1)) + '-' + ((g12398.getDate() < 10 ? '0' : '') + g12398.getDate()) + ' ' + ((g12398.getHours() < 10 ? '0' : '') + g12398.getHours()) + ':' + ((g12398.getMinutes() < 10 ? '0' : '') + g12398.getMinutes()) + ':' + ((g12398.getSeconds() < 10 ? '0' : '') + g12398.getSeconds()) + ':';
        return fs.write('phantom-crawler.log', g12399 + ' ' + ('Page Console >> ' + msg) + '\n', 'a');
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
        if ('http://weibo.com/signup/' === page.url.slice(0, 24)) {
            page.logging = null;
            return onfailed(page);
        };
    };
    return page.open('http://weibo.com/u/' + userId);
};
function crawl_repost(url, outfile) {
    var username = 'blueberry_234@163.com';
    var password = 'blueberry';
    var userid = '3305942100';
    var g12400 = new Date;
    var g12401 = g12400.getFullYear() + '-' + ((g12400.getMonth() + 1 < 10 ? '0' : '') + (g12400.getMonth() + 1)) + '-' + ((g12400.getDate() < 10 ? '0' : '') + g12400.getDate()) + ' ' + ((g12400.getHours() < 10 ? '0' : '') + g12400.getHours()) + ':' + ((g12400.getMinutes() < 10 ? '0' : '') + g12400.getMinutes()) + ':' + ((g12400.getSeconds() < 10 ? '0' : '') + g12400.getSeconds()) + ':';
    fs.write('phantom-crawler.log', g12401 + ' ' + ('Crawling reposts of weibo: ' + url) + '\n', 'a');
    return openDirectly(userid, function (page) {
        var g12402 = new Date;
        var g12403 = g12402.getFullYear() + '-' + ((g12402.getMonth() + 1 < 10 ? '0' : '') + (g12402.getMonth() + 1)) + '-' + ((g12402.getDate() < 10 ? '0' : '') + g12402.getDate()) + ' ' + ((g12402.getHours() < 10 ? '0' : '') + g12402.getHours()) + ':' + ((g12402.getMinutes() < 10 ? '0' : '') + g12402.getMinutes()) + ':' + ((g12402.getSeconds() < 10 ? '0' : '') + g12402.getSeconds()) + ':';
        fs.write('phantom-crawler.log', g12403 + ' ' + ('Auto login directly, url now: ' + page.url) + '\n', 'a');
        page.onLoadFinished = null;
        return getReposts(page, url, outfile);
    }, function (page) {
        var g12404 = new Date;
        var g12405 = g12404.getFullYear() + '-' + ((g12404.getMonth() + 1 < 10 ? '0' : '') + (g12404.getMonth() + 1)) + '-' + ((g12404.getDate() < 10 ? '0' : '') + g12404.getDate()) + ' ' + ((g12404.getHours() < 10 ? '0' : '') + g12404.getHours()) + ':' + ((g12404.getMinutes() < 10 ? '0' : '') + g12404.getMinutes()) + ':' + ((g12404.getSeconds() < 10 ? '0' : '') + g12404.getSeconds()) + ':';
        fs.write('phantom-crawler.log', g12405 + ' ' + ('Failed to auto login, url now: ' + page.url) + '\n', 'a');
        page.render('page.png');
        page.onLoadFinished = null;
        var g12406 = new Date;
        var g12407 = g12406.getFullYear() + '-' + ((g12406.getMonth() + 1 < 10 ? '0' : '') + (g12406.getMonth() + 1)) + '-' + ((g12406.getDate() < 10 ? '0' : '') + g12406.getDate()) + ' ' + ((g12406.getHours() < 10 ? '0' : '') + g12406.getHours()) + ':' + ((g12406.getMinutes() < 10 ? '0' : '') + g12406.getMinutes()) + ':' + ((g12406.getSeconds() < 10 ? '0' : '') + g12406.getSeconds()) + ':';
        fs.write('phantom-crawler.log', g12407 + ' ' + 'Try relogin.' + '\n', 'a');
        return login(username, password, userid, function (page2) {
            return getReposts(page2, url, outfile);
        });
    });
};
crawl_repost(system.args[1], system.args[2]);
