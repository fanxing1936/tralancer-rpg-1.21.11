tag @e[tag=rpg.ch1.minion] remove rpg.ch1.minion.current
execute as @e[tag=rpg.ch1.minion] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.minion.current
tag @e[type=minecraft:villager,tag=rpg.ch1.mira] remove rpg.ch1.mira.current
execute as @e[type=minecraft:villager,tag=rpg.ch1.mira] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.mira.current
execute unless entity @s[tag=rpg.ch1.mira.captured] if entity @e[tag=rpg.ch1.minion.current,distance=..40,limit=1] at @e[type=minecraft:villager,tag=rpg.ch1.mira.current,limit=1] if entity @e[tag=rpg.ch1.minion.current,distance=..8,limit=1] unless entity @a[tag=rpg.ch1.current,distance=..10,limit=1] run scoreboard players add @s rpg_ch1_guard 1
execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_guard matches 120.. run function rpg:campaign/beelzebub/mira/capture
execute if entity @s[tag=rpg.ch1.mira.captured] run scoreboard players remove @s rpg_ch1_guard 1
execute if entity @s[tag=rpg.ch1.mira.captured] at @e[type=minecraft:villager,tag=rpg.ch1.mira.current,limit=1] if entity @a[tag=rpg.ch1.current,distance=..3,limit=1] run scoreboard players add @s rpg_ch1_rescue 1
execute if entity @s[tag=rpg.ch1.mira.captured] at @e[type=minecraft:villager,tag=rpg.ch1.mira.current,limit=1] unless entity @a[tag=rpg.ch1.current,distance=..3,limit=1] run scoreboard players set @s rpg_ch1_rescue 0
execute if entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_rescue matches 40.. run function rpg:campaign/beelzebub/mira/rescue_capture
execute if entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_guard matches ..0 run function rpg:campaign/beelzebub/recover_minions
execute if score @s rpg_ch1_sub matches 1 if score @s rpg_ch1_obj matches ..1 if score @s rpg_ch1_time matches 100.. run function rpg:campaign/beelzebub/recover_minions
execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_sub matches 1 if score @s rpg_ch1_obj matches 2.. unless entity @e[tag=rpg.ch1.minion.current,limit=1] run function rpg:campaign/beelzebub/minion/wave2
execute if score @s rpg_ch1_sub matches 2 if score @s rpg_ch1_obj matches ..3 if score @s rpg_ch1_time matches 100.. run function rpg:campaign/beelzebub/recover_minions
execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_sub matches 2 if score @s rpg_ch1_obj matches 4.. unless entity @e[tag=rpg.ch1.minion.current,limit=1] run function rpg:campaign/beelzebub/minion/wave3
execute if score @s rpg_ch1_sub matches 3 if score @s rpg_ch1_obj matches ..4 if score @s rpg_ch1_time matches 100.. run function rpg:campaign/beelzebub/recover_minions
execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_sub matches 3 if score @s rpg_ch1_obj matches 5.. unless entity @e[tag=rpg.ch1.minion.current,limit=1] unless entity @s[tag=rpg.ch1.recap.minions] run function rpg:campaign/beelzebub/recap/minions
execute unless entity @s[tag=rpg.ch1.mira.captured] if score @s rpg_ch1_sub matches 3 if score @s rpg_ch1_obj matches 5.. unless entity @e[tag=rpg.ch1.minion.current,limit=1] if entity @s[tag=rpg.ch1.recap.minions] if score @s rpg_ch1_time matches 100.. run function rpg:campaign/beelzebub/advance
