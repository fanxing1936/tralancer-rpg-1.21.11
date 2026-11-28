# 圆心标记（as/at）：绕着转，带着肋骨走
execute if score @s rpg_mk_life matches ..120 if entity @s[tag=rpg.mkb.orba] run tp @s ~ ~ ~ ~6 0
execute if score @s rpg_mk_life matches ..120 if entity @s[tag=rpg.mkb.orbb] run tp @s ~ ~ ~ ~-6 0
execute if entity @s[tag=rpg.mkb.orba] at @s positioned ^ ^1.2 ^10 as @e[tag=rpg.mkb.riba,distance=0..] run tp @s ~ ~ ~ ~25 0
execute if entity @s[tag=rpg.mkb.orbb] at @s positioned ^ ^1.2 ^10 as @e[tag=rpg.mkb.ribb,distance=0..] run tp @s ~ ~ ~ ~-25 0
execute if score @s rpg_mk_life matches ..120 if entity @s[tag=rpg.mkb.orba] at @s positioned ^ ^ ^10 run function rpg:michael_boss_i3/bones/cut
scoreboard players operation #m rpg_mk_i3 = @s rpg_mk_life
scoreboard players set #k rpg_mk_i3 2
scoreboard players operation #m rpg_mk_i3 %= #k rpg_mk_i3
execute if score #m rpg_mk_i3 matches 0 at @s positioned ^ ^1.2 ^10 run function rpg:michael_boss_i3/bones/trail
execute if score @s rpg_mk_life matches ..120 if entity @s[tag=rpg.mkb.orbb] at @s positioned ^ ^ ^10 run function rpg:michael_boss_i3/bones/cut
