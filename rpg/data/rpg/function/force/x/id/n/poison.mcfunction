tag @s add rpg.fo.p_poison
execute if entity @s[tag=rpg.fo.r_poison] run return 0
tag @s add rpg.fo.r_poison
$scoreboard players set #t rpg_fo $(duration)
execute unless score #t rpg_fo matches 21.. run return 0
data modify storage rpg:force r.e set value "poison"
$data modify storage rpg:force r.a set value $(amplifier)
execute unless score @s rpg_sef matches 5.. run scoreboard players operation #t rpg_fo *= #7 rpg_fo
execute if score @s rpg_sef matches 5.. run scoreboard players operation #t rpg_fo *= #4 rpg_fo
scoreboard players operation #t rpg_fo /= #10 rpg_fo
scoreboard players operation #t rpg_fo /= #20 rpg_fo
execute if score #t rpg_fo matches ..0 run scoreboard players set #t rpg_fo 1
execute store result storage rpg:force r.s int 1 run scoreboard players get #t rpg_fo
effect clear @s minecraft:poison
function rpg:force/x/id/regive with storage rpg:force r
