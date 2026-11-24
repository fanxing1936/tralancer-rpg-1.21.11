execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id
# 收起旁白：字幕血条、配音、旁白配乐
tag @s remove rpg.ob.intro
function rpg:onboard/intro/unbars with storage rpg:onboard tmp
stopsound @s voice
function rpg:onboard/music/stop
