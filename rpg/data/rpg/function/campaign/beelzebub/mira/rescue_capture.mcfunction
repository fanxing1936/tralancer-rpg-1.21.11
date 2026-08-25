tag @s remove rpg.ch1.mira.captured
scoreboard players set @s rpg_ch1_guard 0
scoreboard players set @s rpg_ch1_rescue 0
execute at @s positioned ^ ^ ^17 run tp @e[type=minecraft:villager,tag=rpg.ch1.mira.current,limit=1] ~ ~ ~
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[见证人救回] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"米拉重新回到队伍；街区战继续。","color":"gray","bold":false,"italic":false}]
