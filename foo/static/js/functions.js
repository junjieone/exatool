function create_conf(){
    var conf_textarea = document.getElementById("conf_textarea");
    vpn_conf = conf_textarea.value;
    $.post(
        "/foo/create/",
        {vpn_conf:vpn_conf},
        function(res) {
            alert(res.msg);
        },
    );
}
function command(action, category, operation){
    data = {};
    if(action == 'modify'){
        if(category == 'normal'){
            var nm_nb_addr = document.getElementById("nm_nb_addr").value;
            var nm_pref = document.getElementById("nm_pref").value;
            var nm_nh = document.getElementById("nm_nh").value;
            data = {
                'nm_nb_addr':nm_nb_addr,
                'nm_pref':nm_pref,
                'nm_nh':nm_nh
            }
        }
        if(category == 'label'){
            var lb_nb_addr = document.getElementById("lb_nb_addr").value;
            var lb_pref = document.getElementById("lb_pref").value;
            var lb_nh = document.getElementById("lb_nh").value;
            var lb_lb = document.getElementById("lb_lb").value;
            data = {
                'lb_nb_addr':lb_nb_addr,
                'lb_pref':lb_pref,
                'lb_nh':lb_nh,
                'lb_lb':lb_lb
            }
        }
        if(category == 'flowspec'){
            var fs_nb_addr = document.getElementById("fs_nb_addr").value;
            var fs_sr_pref = document.getElementById("fs_sr_pref").value;
            var fs_dt_nh = document.getElementById("fs_dt_nh").value;
            var fs_act = document.getElementById("fs_act").value;
            data = {
                'fs_nb_addr':fs_nb_addr,
                'fs_sr_pref':fs_sr_pref,
                'fs_dt_nh':fs_dt_nh,
                'fs_act':fs_act
            }
        }
    }
    $.post(
        "/foo/command/" + action + "/" + (category==''?'':category + "/") + (operation==''?'':operation + "/"),
        data,
        function(res) {
            var result_textarea = document.getElementById("result_textarea");
            if(res.action == 'start'){
                result_textarea.innerHTML += "--------------------Start--------------------\n";
            }
            if(res.action == 'modify'){
                result_textarea.innerHTML += "--------------------Modify--------------------\n";
                result_textarea.innerHTML += "PID: " + res.pid + "\n";
            }
            if(res.action == 'terminate'){
                result_textarea.innerHTML += "--------------------Terminate--------------------\n";
            }
            result_textarea.innerHTML += "Command: " + res.cmd + "\n\n";
            result_textarea.innerHTML += res.result + '\n\n';
        },
    );
}
function clean(){
    var result_textarea = document.getElementById("result_textarea");
    result_textarea.innerHTML = "";
}