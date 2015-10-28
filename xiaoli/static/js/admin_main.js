/**
 * Created by zouyingjun on 15/10/27.
 */

$(function(){
    // 处理 select2
    var $keywordSelectElement = $(".admin-plan-form #plan-keywords");
    if ($keywordSelectElement.length > 0){
        $keywordSelectElement.select2();
    }

    //处理action-prompt，需要确认的操作
    var $actionPromptElement = $(".action-prompt");
    if ($actionPromptElement.length > 0){
        $actionPromptElement.on("click", function(e){
            e.preventDefault();
            var $element = $(e.currentTarget),
                promptText = $element.data('prompt'),
                href = $element.attr('href');
            if (!!promptText && !!href){
                if(window.confirm(promptText)){
                    window.location.href = href;
                }
            }
        })
    }
});
