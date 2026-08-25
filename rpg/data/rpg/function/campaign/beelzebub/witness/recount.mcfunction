scoreboard players set @s rpg_ch1_seen 0
execute if entity @s[tag=rpg.ch1.witness.skill.1] run scoreboard players add @s rpg_ch1_seen 1
execute if entity @s[tag=rpg.ch1.witness.skill.2] run scoreboard players add @s rpg_ch1_seen 1
execute if entity @s[tag=rpg.ch1.witness.skill.3] run scoreboard players add @s rpg_ch1_seen 1
execute if entity @s[tag=rpg.ch1.witness.skill.4] run scoreboard players add @s rpg_ch1_seen 1
execute if entity @s[tag=rpg.ch1.witness.skill.5] run scoreboard players add @s rpg_ch1_seen 1
execute if score @s rpg_ch1_seen matches 3.. unless entity @s[tag=rpg.ch1.witness.ready] run function rpg:campaign/beelzebub/witness/confirm
