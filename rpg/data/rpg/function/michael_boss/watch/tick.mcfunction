# 守望者每刻（as/at 它）：照原作，传送到你身边、挥臂或双臂下砸；挨打会传送走（watch/hurt）
scoreboard players add @s rpg_mk_wt 1
scoreboard players operation #m rpg_mk = @s rpg_mk_wt
scoreboard players set #k rpg_mk 4
scoreboard players operation #m rpg_mk %= #k rpg_mk
execute if score #m rpg_mk matches 0 unless score @s rpg_mk_ws matches 3..4 run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_mk_ws matches 0 if score @s rpg_mk_wt matches 30.. unless entity @e[tag=rpg.unit.f,distance=..3.2] run return run function rpg:michael_boss/watch/blink
execute if score @s rpg_mk_ws matches 0 if score @s rpg_mk_wt matches 30.. run return run function rpg:michael_boss/watch/attack
execute if score @s rpg_mk_ws matches 1 if score @s rpg_mk_wt matches 8.. run return run function rpg:michael_boss/watch/arrive
execute if score @s rpg_mk_ws matches 2 if score @s rpg_mk_wt matches 10.. run function rpg:michael_boss/watch/ready
execute if score @s rpg_mk_ws matches 3 if score @s rpg_mk_wt matches 8 run function rpg:michael_boss/watch/strike
execute if score @s rpg_mk_ws matches 3 if score @s rpg_mk_wt matches 24.. run function rpg:michael_boss/watch/rest
execute if score @s rpg_mk_ws matches 4 if score @s rpg_mk_wt matches 14 run function rpg:michael_boss/watch/heavyhit
execute if score @s rpg_mk_ws matches 4 if score @s rpg_mk_wt matches 32.. run function rpg:michael_boss/watch/rest
