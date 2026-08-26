execute as @e[type=minecraft:marker,tag=rpg.ch1.hyp1] at @s run function rpg:campaign/beelzebub/probe/hyp1
execute as @e[type=minecraft:marker,tag=rpg.ch1.hyp2] at @s run function rpg:campaign/beelzebub/probe/hyp2
execute as @e[type=minecraft:marker,tag=rpg.ch1.hyp3] at @s run function rpg:campaign/beelzebub/probe/hyp3
function rpg:campaign/beelzebub/puzzle/refresh_enemies
execute if score @s rpg_ch1_obj matches 3.. if score @s rpg_ch1_sub matches 0 run function rpg:campaign/beelzebub/hypothesis_board/activate
execute if score @s rpg_ch1_sub matches 1 unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] as @e[type=minecraft:marker,tag=rpg.ch1.theory1] at @s run function rpg:campaign/beelzebub/probe/theory1
execute if score @s rpg_ch1_sub matches 1 unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] as @e[type=minecraft:marker,tag=rpg.ch1.theory2] at @s run function rpg:campaign/beelzebub/probe/theory2
execute if score @s rpg_ch1_sub matches 1 unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] as @e[type=minecraft:marker,tag=rpg.ch1.theory3] at @s run function rpg:campaign/beelzebub/probe/theory3
execute if score @s rpg_ch1_sub matches 1 if entity @s[tag=rpg.ch1.puzzle.wait.theory] unless entity @e[tag=rpg.ch1.puzzle.enemy.current,limit=1] run function rpg:campaign/beelzebub/hypothesis_board/respawn
execute if score @s rpg_ch1_sub matches 2 unless entity @s[tag=rpg.ch1.recap.hypothesis] run function rpg:campaign/beelzebub/recap/hypothesis
execute if score @s rpg_ch1_sub matches 2 if entity @s[tag=rpg.ch1.recap.hypothesis] if score @s rpg_ch1_time matches 200.. run function rpg:campaign/beelzebub/advance
