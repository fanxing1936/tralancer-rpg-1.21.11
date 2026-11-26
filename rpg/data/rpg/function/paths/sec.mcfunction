scoreboard players enable @s rpg_pa_do
execute if score @s rpg_pa_ct matches 1.. run scoreboard players remove @s rpg_pa_ct 1
execute if entity @s[tag=rpg.pa.any] run function rpg:paths/bless/sec
execute if score @s rpg_ps_20 matches 1 run function rpg:paths/hermit
execute if score @s rpg_ps_26 matches 1 if score #m2 rpg_sef matches 0 run function rpg:paths/taint
