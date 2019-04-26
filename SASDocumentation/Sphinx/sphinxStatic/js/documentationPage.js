$(document).ready(function(){
    createNetworkGraph(window.flowChart);

    var textArea = $("#code");
    textArea.val(window.rawCode);
    textArea.text(function(index, text){
        return strip(text);
    });

    var cmConfig = {mode:"sas",lineNumbers:true,readOnly:true,gutter:true,lineWrapping:true,autoRefresh: true};
    window.codeMirror = CodeMirror.fromTextArea(document.getElementById("code"), cmConfig);
    window.codeMirror.setSize(null,500)

    $(".lineJump").each(function(){
        $(this).attr("href","javascript:jumpTo("+$(this).attr('startLine')+","+$(this).attr('endLine')+")");
    })
});

function jumpTo(startLine,endLine){
    $('.cm-searching').removeClass('cm-searching');
    window.codeMirror.scrollIntoView({line:startLine,char:0});
    window.codeMirror.markText({line:startLine-2,char:0},{line:endLine-1,char:0},{className:'cm-searching'});
}

function strip(html)
{
   var tmp = document.createElement("DIV");
   tmp.innerHTML = html;
 
   return tmp.textContent||tmp.innerText;
}