# as 根：缩回地下，播完消亡动作再清掉。
execute if entity @s[tag=rpg.luv.dying] run return 0
tag @s add rpg.luv.dying
scoreboard players set @s rpg_luv_l 36
function rpg:lucifer_vine/anim/enter/death
