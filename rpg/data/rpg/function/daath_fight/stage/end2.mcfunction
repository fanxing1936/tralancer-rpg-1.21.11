# 二段打空：绝境没过就进绝境，过了就跪下
function rpg:daath_fight/sk/end
execute if entity @s[tag=rpg.dt.despdone] run return run function rpg:daath_fight/end/begin
function rpg:daath_fight/despair/begin
