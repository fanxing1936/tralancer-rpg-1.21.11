# 3 秒内没全打碎：眼轮合上复原
scoreboard players set #first rpg_pr 0
kill @e[type=minecraft:slime,tag=rpg.pr.wheel]
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s run function rpg:prologue/throne/rewheel
function rpg:prologue/sub/t07
