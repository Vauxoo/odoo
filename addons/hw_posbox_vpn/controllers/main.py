# -*- coding: utf-8 -*-
import logging
import subprocess

from os import path
from tempfile import NamedTemporaryFile
from base64 import b64decode

from openerp import http
from openerp.tools import config
from openerp.modules import get_module_path
from openerp.addons.hw_proxy.controllers import main as hw_proxy

_logger = logging.getLogger(__name__)

vpn_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VPN Configuration</title>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet"
  href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
<script src="http://code.jquery.com/jquery-1.9.1.js"></script>
<script
  src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js">
</script>
<script>
$(function () {
    function run_progressbar(bar, ms){
        var current = parseInt(bar.attr("aria-valuenow"));
        var valuemax = parseInt(bar.attr("aria-valuemax"));
        var progress = setInterval(function () {
            if (current>=valuemax) {
                clearInterval(progress);
                bar.removeClass('active');
                bar.addClass('progress-bar-success');
            } else {
                current +=1;
                bar.css('width', (current) +  "%");
            }
            bar.text((current) + "%");
        }, ms);

    }
    $('#uprogressbar').click(function(){
        $('#upload').tooltip('toggle');
    });
    $('#vprogressbar').click(function(){
        $('#restart').tooltip('toggle');
    });
    $('#config').change(function(event) {
        var self = $(this);
        var config_file = event.target.files[0];
        var filename = $('#config').val();
        var ext = filename.split('.').pop().toLowerCase();
        if(filename == ""){
            alert('Please select a file');
        }
        else if($.inArray(ext, ['conf']) == -1) {
            alert('Only .conf file can be uploaded!');
        }
        else {
            var password = $('#admin').val();
            var reader = new FileReader();
            reader.onload = function(readerEvt) {
                var binaryString = readerEvt.target.result;
                $.ajax({
                    url: '/vpn_upload',
                    data: {
                        'conf': btoa(binaryString),
                        'password': password,
                    },
                }).always(function (response) {
                    console.log(response);
                    if(response == 'ok') {
                        $('.progress').removeClass('hidden');
                        // progress bar
                        interval = 100;
                        on_hold = 40;
                        var ubar = $('#uprogressbar');
                        $('#upload').tooltip('show');
                        run_progressbar(ubar, interval);
                        setTimeout(function(){
                            var vbar = $('#vprogressbar');
                            $('#restart').tooltip('show');
                            run_progressbar(vbar, interval * 3);
                        }, interval * 100 + on_hold);
                    }
                    else {
                        self.val("").clone(true);
                        alert(response);
                    }
                });
            };
            reader.readAsBinaryString(config_file);
        }
    });
});
</script>
<style>
.btn-file {
    position: relative;
    overflow: hidden;
}
.btn-file input[type=file] {
    position: absolute;
    top: 0;
    right: 0;
    min-width: 100%;
    min-height: 100%;
    font-size: 100px;
    text-align: right;
    filter: alpha(opacity=0);
    opacity: 0;
    outline: none;
    background: white;
    cursor: inherit;
    display: block;

}
.posbox-template {
    width: 480px;
    text-align: center;
    padding: 60px 0px;
    margin: 0px auto;
    font-family: sans-serif;
}
</style>
</head>
<body>
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
            <a class="navbar-brand" href="/">PosBox</a>
        </div>
      </div>
    </nav>
    <div class='container'>
        <div class='posbox-template'>
            <h1>OpenVPN configuration file</h1>
            <p class='lead'>
              To connect the PosBox into a running OpenVPN server, you
              must have a client configuration file ready to upload and
              then connect to the server network.
            </p>
            <p>
              <div class="form-group">
                <label for="admin">Admin Password</label>
                <input id="admin" type="password" class="form-control"
                  placeholder="Password">
              </div>
            </p>
            <p>
              <span class="btn btn-success btn-lg btn-block btn-file">
                Choose a file... <input type="file" id="config" />
              </span>
            </p>
            <p id="upload" data-toggle="tooltip" data-placement="left"
              title="Uploading file">
              <div class="progress hidden">
                <div id="uprogressbar" role="progressbar" style="width: 0%"
                    aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"
                    class="progress-bar progress-bar-striped active">
                        0%
                </div>
              </div>
            </p>
            <p id="restart" data-toggle="tooltip" data-placement="left"
              title="Restarting vpn">
              <div class="progress hidden">
                <div id="vprogressbar" role="progressbar" style="width: 0%"
                    aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"
                    class="progress-bar progress-bar-striped active">
                        0%
                </div>
              </div>
            </p>
            <p>
              <a href="/vpn"> Try again! </a>
            </p>
        </div>
    </div>
</body>
</html>
"""


class PosboxVpnConfiguration(hw_proxy.Proxy):

    @http.route('/vpn', type='http', auth='none', cors='*')
    def vpn(self):
        return vpn_template

    @http.route('/vpn_upload', type='http', auth='none', cors='*')
    def upload_vpn_configuration(self, conf, password=False):
        if not password:
            return 'Please insert admin password to load file'
        if password != config.get('admin_passwd'):
            return 'Wrong password!'
        pos_path = get_module_path('point_of_sale')
        process = path.join(
            pos_path, 'tools/posbox/configuration/posbox_vpn_upload.sh')
        decoded = b64decode(conf)
        with NamedTemporaryFile(delete=False) as tmp:
            tmp.write(decoded)
            subprocess.call([process, tmp.name])
        return 'ok'
