# 相撞成功（as 影子）
tag @s remove rpg.dt.window
tag @s remove rpg.dt.clash
execute at @a[tag=rpg.dt.me,limit=1] positioned ~ ~ ~ run function rpg:daath_fight/clash/spark
kill @e[type=minecraft:interaction,tag=rpg.dt.clk,distance=..60]
scoreboard players set #s rpg_dt 80
function rpg:daath_fight/stun
