// Phantomjs odoo helper
// jshint evil: true, loopfunc: true

var system = require('system');

// function waitFor (condition, callback, timeout, timeoutMessageCallback) {
//     timeout = timeout || 10000;
//     var start = new Date();

//     (function waitLoop() {
//         if(new Date() - start > timeout) {
//             console.log('error', timeoutMessageCallback ? timeoutMessageCallback() : "Timeout after "+timeout+" ms");
//             phantom.exit(1);
//         } else if (condition()) {
//             callback();
//         } else {
//             setTimeout(waitLoop, 250);
//         }
//     }());
// }
function waitFor(testFx, onReady, timeOutMillis) {
    var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 3000, //< Default Max Timout is 3s
        start = new Date().getTime(),
        condition = false,
        interval = setInterval(function() {
            if ( (new Date().getTime() - start < maxtimeOutMillis) && !condition ) {
                // If not time-out yet and condition not yet fulfilled
                condition = (typeof(testFx) === "string" ? eval(testFx) : testFx()); //< defensive code
            } else {
                if(!condition) {
                    // If condition still not fulfilled (timeout but condition is 'false')
                    console.log("'waitFor()' timeout");
                    phantom.exit(1);
                } else {
                    // Condition fulfilled (timeout and/or condition is 'true')
                    console.log("'waitFor()' finished in " + (new Date().getTime() - start) + "ms.");
                    typeof(onReady) === "string" ? eval(onReady) : onReady(); //< Do what it's supposed to do once the condition is fulfilled
                    clearInterval(interval); //< Stop this interval
                }
            }
        }, 250); //< repeat check every 250ms
};

function PhantomTest() {
    var self = this;
    this.options = JSON.parse(system.args[system.args.length-1]);
    this.inject = this.options.inject || [];
    this.timeout = this.options.timeout ? Math.round(parseFloat(this.options.timeout)*1000 - 5000) : 10000;
    this.origin = 'http://localhost';
    this.origin += this.options.port ? ':' + this.options.port : '';

    // ----------------------------------------------------
    // configure phantom and page
    // ----------------------------------------------------
    phantom.addCookie({
        'domain': 'localhost',
        'name': 'session_id',
        'value': this.options.session_id,
    });
    this.page = require('webpage').create();
    this.page.viewportSize = { width: 1366, height: 768 };
    this.page.onError = function(message, trace) {
        var msg = [message];
        if (trace && trace.length) {
            msg.push.apply(msg, trace.map(function (frame) {
                var result = [' at ', frame.file, ':', frame.line];
                if (frame.function) {
                    result.push(' (in ', frame.function, ')');
                }
                return result.join('');
            }));
            msg.push('(leaf frame on top)');
        }
        console.log('error', JSON.stringify(msg.join('\n')));
        phantom.exit(1);
    };
    this.page.onAlert = function(message) {
        console.log('error', message);
        phantom.exit(1);
    };
    this.page.onConsoleMessage = function(message) {
        console.log(message);
    };
    this.page.onLoadFinished = function(status) {
        if (status === "success") {
            for (var k in self.inject) {
                var found = false;
                var v = self.inject[k];
                var need = v;
                var src = v;
                if (v[0]) {
                    need = v[0];
                    src = v[1];
                    found = self.page.evaluate(function(code) {
                        try {
                            return !!eval(code);
                        } catch (e) {
                            return false;
                        }
                    }, need);
                }
                if(!found) {
                    console.log('Injecting', src, 'needed for', need);
                    if(!self.page.injectJs(src)) {
                        console.log('error', "Cannot inject " + src);
                        phantom.exit(1);
                    }
                }
            }
        }
    };
    setTimeout(function () {
        self.page.evaluate(function () {
            var message = ("Timeout\nhref: " + window.location.href +
                           "\nreferrer: " + document.referrer +
                           "\n\n" + (document.body && document.body.innerHTML)).replace(/[^a-z0-9\s~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gi, "*");
            console.log('error', message);
        });
        phantom.exit(1);
    }, self.timeout);

    // ----------------------------------------------------
    // run test
    // ----------------------------------------------------
    this.run = function(url_path, code, ready) {
        if(self.options.login) {
            var qp = [];
            qp.push('db=' + self.options.db);
            qp.push('login=' + self.options.login);
            qp.push('key=' + self.options.password);
            qp.push('redirect=' + encodeURIComponent(url_path));
            url_path = "/login?" + qp.join('&');
        }
        var url = self.origin + url_path;
        code = code || "true";
        ready = ready || "true";
        self.page.open(url, function(status) {
            if (status !== 'success') {
                console.log('error', "failed to load " + url);
                phantom.exit(1);
            } else {
                console.log('loaded', url, status);
                // clear localstorage leftovers
                self.page.evaluate(function () { localStorage.clear() });
                // process ready
                waitFor(function() {
                    console.log("PhantomTest.run: wait for condition:", ready);
                    return self.page.evaluate(function (ready) {
                        var r = false;
                        try {
                            console.log("page.evaluate eval expr:", ready);
                            r = !!eval(ready);
                        } catch(ex) {
                        }
                        console.log("page.evaluate eval result:", r);
                        return r;
                    }, ready);
                // run test
                }, function() {
                    console.log("PhantomTest.run: condition statified, executing: " + code);
                    self.page.evaluate(function (code) { return eval(code); }, code);
                    console.log("PhantomTest.run: execution launched, waiting for console.log('ok')...");
                });
            }
        });
    };
}

// js mode or jsfile mode
if(system.args.length === 2) {
    pt = new PhantomTest();
    pt.run(pt.options.url_path, pt.options.code, pt.options.ready);
}

// vim:et:
