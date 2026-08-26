execute as @e[type=minecraft:marker,tag=rpg.ch1.trail1] at @s run function rpg:campaign/beelzebub/probe/trail1
execute as @e[type=minecraft:marker,tag=rpg.ch1.trail2] at @s run function rpg:campaign/beelzebub/probe/trail2
execute as @e[type=minecraft:marker,tag=rpg.ch1.trail3] at @s run function rpg:campaign/beelzebub/probe/trail3
execute as @e[type=minecraft:marker,tag=rpg.ch1.trail4] at @s run function rpg:campaign/beelzebub/probe/trail4
function rpg:campaign/beelzebub/puzzle/refresh_enemies
execute if score @s rpg_ch1_obj matches 4.. if score @s rpg_ch1_sub matches 0 run function rpg:campaign/beelzebub/route/activate
execute if score @s rpg_ch1_sub matches 1 unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] as @e[type=minecraft:marker,tag=rpg.ch1.route1] at @s run function rpg:campaign/beelzebub/probe/route1
execute if score @s rpg_ch1_sub matches 1 unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] as @e[type=minecraft:marker,tag=rpg.ch1.route2] at @s run function rpg:campaign/beelzebub/probe/route2
execute if score @s rpg_ch1_sub matches 1 unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] as @e[type=minecraft:marker,tag=rpg.ch1.route3] at @s run function rpg:campaign/beelzebub/probe/route3
execute if score @s rpg_ch1_sub matches 1 if entity @s[tag=rpg.ch1.puzzle.wait.route] unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] run function rpg:campaign/beelzebub/route/respawn
execute if score @s rpg_ch1_sub matches 2 unless entity @s[tag=rpg.ch1.recap.area] run function rpg:campaign/beelzebub/recap/area
execute if score @s rpg_ch1_sub matches 2 if entity @s[tag=rpg.ch1.recap.area] if score @s rpg_ch1_time matches 200.. run function rpg:campaign/beelzebub/advance
