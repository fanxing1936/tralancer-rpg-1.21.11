# 排一句（宏 f）：#due 到点的游戏刻、#sid 说给谁；位置取当前执行位置
data modify storage rpg:say e set value {f:0,due:0,sid:0,x:0,y:0,z:0}
$data modify storage rpg:say e.f set value $(f)
execute store result storage rpg:say e.due int 1 run scoreboard players get #due rpg_say
execute store result storage rpg:say e.sid int 1 run scoreboard players get #sid rpg_say
execute summon minecraft:marker run function rpg:town/say/pos
data modify storage rpg:say q append from storage rpg:say e
