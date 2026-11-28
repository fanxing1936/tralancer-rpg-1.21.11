# 3 秒内没全打碎：眼轮合上复原
scoreboard players set #first rpg_pr_i1 0
kill @e[type=minecraft:slime,tag=rpg.pr.wheel,distance=0..]
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,distance=0..] at @s run function rpg:prologue_i1/throne/rewheel
function rpg:prologue_i1/sub/t07
