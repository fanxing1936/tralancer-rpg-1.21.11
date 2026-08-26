execute as @e[type=minecraft:marker,tag=rpg.ch1.cache1] at @s run function rpg:campaign/beelzebub/probe/cache1
execute as @e[type=minecraft:marker,tag=rpg.ch1.cache2] at @s run function rpg:campaign/beelzebub/probe/cache2
execute as @e[type=minecraft:marker,tag=rpg.ch1.cache3] at @s run function rpg:campaign/beelzebub/probe/cache3
function rpg:campaign/beelzebub/puzzle/refresh_enemies
execute if score @s rpg_ch1_obj matches 3.. if score @s rpg_ch1_sub matches 0 run function rpg:campaign/beelzebub/calibration/activate
execute if score @s rpg_ch1_sub matches 1 unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] as @e[type=minecraft:marker,tag=rpg.ch1.slot1] at @s run function rpg:campaign/beelzebub/probe/slot1
execute if score @s rpg_ch1_sub matches 1 unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] as @e[type=minecraft:marker,tag=rpg.ch1.slot2] at @s run function rpg:campaign/beelzebub/probe/slot2
execute if score @s rpg_ch1_sub matches 1 unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] as @e[type=minecraft:marker,tag=rpg.ch1.slot3] at @s run function rpg:campaign/beelzebub/probe/slot3
execute if score @s rpg_ch1_sub matches 1 if entity @s[tag=rpg.ch1.puzzle.wait.slot] unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] run function rpg:campaign/beelzebub/calibration/respawn
execute if score @s rpg_ch1_sub matches 2 unless entity @s[tag=rpg.ch1.recap.prep] run function rpg:campaign/beelzebub/recap/prep
execute if score @s rpg_ch1_sub matches 2 if entity @s[tag=rpg.ch1.recap.prep] if score @s rpg_ch1_time matches 200.. run function rpg:campaign/beelzebub/advance
