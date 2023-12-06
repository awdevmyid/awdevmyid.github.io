const ASYNC_EVENT_ID = "AwdevAPIEvent";

//CHANGE THE FOLLOWING ID VARIABLES TO MATCH THE PROPER ID VALUES YOU HAVE
const DEV_ID = "DEV_ID";
const PUBLISHER_ID = "ca-pub-8796768128400226"; 

function init()
{
    console.log("AwdevAPI.js: init");
    AwdevAPI.init(DEV_ID, PUBLISHER_ID);    
}

//NOTE: pause the game and mute music before calling this
function showAd()
{
    AwdevAPI.APIAds.show(function() 
    {
        var map = {};
        map["id"] = ASYNC_EVENT_ID;
        map["event_type"] = "ad_watched";        
        GMS_API.send_async_event_social(map);

        //NOTE: Unpause the game and unmute the music after receving this callback
        
        console.log("AwdevAPI.js: ad watched");    
    });
}

function saveAchievement(awardId)
{
    var apiAwards = [];
    apiAwards.push(awardId); //NOTE: you can push more than one award at a time
    var map = {};
    map["id"] = ASYNC_EVENT_ID;
    
    AwdevAPI.Achievements.save(apiAwards, function(response) 
    {
        if(response.success) 
        {
            console.log("AwdevAPI.js: achievement " + awardId + " saved");      
            map["event_type"] = "achievement_save_success";
        }
        else 
        {
            console.log("AwdevAPI.js: "+ response.errormsg);
            map["event_type"] = "achievement_save_error";
        }
    
        GMS_API.send_async_event_social(map);
    });
}

function saveHighScore(highScoreBoardId, newHighScore)
{
    var boardinfo = {};
    boardinfo.score = newHighScore;
    boardinfo.board = highScoreBoardId;

    var map = {};
    map["id"] = ASYNC_EVENT_ID;

    AwdevAPI.Scores.save(boardinfo, function(response) 
    {
        if(response.success) 
        {
            map["event_type"] = "high_score_save_success";
            console.log("AwdevAPI.js: high score saved")
        }
        else 
        {
            map["event_type"] = "high_score_save_error";
            console.log("AwdevAPI.js: " + response.errormsg);
        }

        GMS_API.send_async_event_social(map);
    });
}

function prepareRewardedAd()
{    
    AwdevAPI.GEvents.reward(canShowReward, rewardSuccess);
}

//NOTE: prepareRewardedAd() must be called successfully before this method can be used to show the ad
function showRewardedAd()
{
    showAdFunction();
}

var showAdFunction;

var canShowReward = function(success, showAdFn)
{        
    var map = {};
    map["id"] = ASYNC_EVENT_ID;

    if(success)
    {            
        map["event_type"] = "rewarded_ad_available";
        showAdFunction = showAdFn;
        console.log("AwdevAPI.js: rewarded ad available");
    }
    else
    {
        map["event_type"] = "rewarded_ad_unavailable";
        console.log("AwdevAPI.js: rewarded ad unavailable");
    }
    
    GMS_API.send_async_event_social(map);
}

var rewardSuccess = function(success)
{
    var map = {};
    map["id"] = ASYNC_EVENT_ID;

    if (success)
    {
        map["event_type"] = "rewarded_ad_watched";
        console.log("AwdevAPI.js: rewarded ad watched");
    }
    else
    {
        map["event_type"] = "rewarded_ad_not_watched";
        console.log("AwdevAPI.js: rewarded ad not watched");
    }

    GMS_API.send_async_event_social(map);
}
