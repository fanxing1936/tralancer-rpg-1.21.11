tag @s add rpg.ch1.mira.captured
scoreboard players set @s rpg_ch1_guard 3600
scoreboard players set @s rpg_ch1_rescue 0
execute positioned ^ ^ ^35 run tp @e[type=minecraft:villager,tag=rpg.ch1.mira.current,limit=1] ~ ~ ~
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[见证人被捕] ","color":"#8B2500","bold":true,"italic":false},{"text":"在 03:00 内靠近米拉 3 格将她带回，否则整组罪仆重置。","color":"gray","bold":false,"italic":false}]
