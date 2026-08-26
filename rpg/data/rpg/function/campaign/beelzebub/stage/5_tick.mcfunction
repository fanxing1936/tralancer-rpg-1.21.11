execute as @e[type=minecraft:marker,tag=rpg.ch1.hyp1] at @s run function rpg:campaign/beelzebub/probe/hyp1
execute as @e[type=minecraft:marker,tag=rpg.ch1.hyp2] at @s run function rpg:campaign/beelzebub/probe/hyp2
execute as @e[type=minecraft:marker,tag=rpg.ch1.hyp3] at @s run function rpg:campaign/beelzebub/probe/hyp3
execute if score @s rpg_ch1_obj matches 3.. unless entity @s[tag=rpg.ch1.recap.hypothesis] run function rpg:campaign/beelzebub/recap/hypothesis
execute if score @s rpg_ch1_obj matches 3.. if entity @s[tag=rpg.ch1.recap.hypothesis] if score @s rpg_ch1_time matches 100.. run function rpg:campaign/beelzebub/advance
