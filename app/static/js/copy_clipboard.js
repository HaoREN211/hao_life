/**
 * Created by hao.ren3 on 2020/10/22.
 */

// 获取id为input_id的输入框内容
function copy_content(input_id) {
    copy_text(document.getElementById(input_id).value); //传递文本
    alert("已复制好，可贴粘。")
}

// 将text的内容传递到剪切板中
function copy_text(text) {
    var copyDom = document.createElement('div');
    copyDom.innerText=text;
    copyDom.style.position='absolute';
    copyDom.style.top='0px';
    copyDom.style.right='-9999px';
    document.body.appendChild(copyDom);
    //创建选中范围
    var range = document.createRange();
    range.selectNode(copyDom);
    //移除剪切板中内容
    window.getSelection().removeAllRanges();
    //添加新的内容到剪切板
    window.getSelection().addRange(range);
    //复制
    document.execCommand('copy');
    copyDom.parentNode.removeChild(copyDom);
}
