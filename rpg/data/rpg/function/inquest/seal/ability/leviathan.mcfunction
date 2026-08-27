scoreboard players set @s rpg_rel_hold 31
execute if score @s rpg_rel_cd matches 1.. run return run tellraw @s ["",{"text":"[遗物冷却] ","color":"#62D9E8","bold":true,"italic":false},{"text":"压制余波仍在，尚不能动用反制。","color":"gray","italic":false}]
execute unless score @s rpg_rel_rec matches 1 run return run tellraw @s ["",{"text":"[利维坦] ","color":"#1B4F72","bold":true,"italic":false},{"text":"尚无可反制的术式","color":"gray","italic":false}]
tag @s add rpg.seal.cast
execute if score @s rpg_rel_src matches 2 run function rpg:inquest/seal/ability/reflect_drown
execute unless score @s rpg_rel_src matches 2 run function rpg:inquest/seal/ability/reflect_magic
tag @s remove rpg.seal.cast
scoreboard players set @s rpg_rel_rec 0
scoreboard players set @s rpg_rel_src 0
scoreboard players add @s rpg_agit 3
execute if score @s rpg_agit matches 101.. run scoreboard players set @s rpg_agit 100
tellraw @s ["",{"text":"[利维坦 · 反制] ","color":"#1B4F72","bold":true,"italic":false},{"text":"术式已同源返还；记录清空，躁动 +3。","color":"gray","italic":false}]
