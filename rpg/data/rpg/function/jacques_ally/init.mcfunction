tag @s remove rpg.jqa.new
tp @s ~ ~ ~ ~ 0
scoreboard players operation @s rpg_al_own = #own rpg_al
scoreboard players set @s rpg_al_t 0
scoreboard players set @s rpg_al_hp 100
scoreboard players set @s rpg_al_b 30
scoreboard players set @s rpg_al_cb 0
scoreboard players set @s rpg_al_sk 0
item replace entity @s weapon.offhand with minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]
scoreboard players set #fxt rpg_al 60
