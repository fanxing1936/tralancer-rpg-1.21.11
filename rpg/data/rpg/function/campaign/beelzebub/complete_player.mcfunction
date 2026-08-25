scoreboard players operation @s rpg_ch1_verdict = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice
execute if score @s rpg_ch1_reward matches 1.. run return 0
scoreboard players set @s rpg_ch1_reward 1
scoreboard players add @s rpg_ex_xp 60
function rpg:campaign/beelzebub/reward/dossier
execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 1 run function rpg:campaign/beelzebub/reward/eliminate
execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 2 run function rpg:campaign/beelzebub/reward/banish
execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 3 run function rpg:campaign/beelzebub/reward/seal
execute if score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_choice matches 4 run function rpg:campaign/beelzebub/reward/pact
scoreboard players set @s rpg_ch1_done 1
scoreboard players set @s rpg_ch1_next 1
tag @s add rpg.ch1.borderer
function rpg:inquest/career/sync
function rpg:inquest/career/claim
advancement grant @s only rpg:campaign/beelzebub
