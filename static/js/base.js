layui.use(['element','layer'], function(){
    var element = layui.element
    ,layer = layui.layer
});
function refreshSwitch() {
    setTimeout(function (){
        $.get("/getSwitch",function(data){
            if (data.code){
                honeySwitch.showOn("#switch")
            }else {
                honeySwitch.showOff("#switch")
            }
        });
    }, 1000);
}
refreshSwitch();
$(function(){
    switchEvent("#switch",function(){
        layer.msg('�ָ�');
        $.get("/Switch/0");
        refreshSwitch();
    },function(){
        layer.msg('��ͣ');
        $.get("/Switch/1");
        refreshSwitch();
    });
});