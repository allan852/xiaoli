/**
 * Created by zouyingjun on 15/10/27.
 */

$(function(){
    var $keywordSelectElement = $(".admin-plan-form #plan-keywords");
    if ($keywordSelectElement.length > 0){
        $keywordSelectElement.select2();
    }
});
