scoreboard players set #channel rpg_ex_tmp 0
scoreboard players set #page_used rpg_ex_tmp 0
execute if score @s rpg_dm_lord matches 1 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:1}] run scoreboard players set #page_used rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 2 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:2}] run scoreboard players set #page_used rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 3 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:3}] run scoreboard players set #page_used rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 4 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:4}] run scoreboard players set #page_used rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 5 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:5}] run scoreboard players set #page_used rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 6 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:6}] run scoreboard players set #page_used rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 7 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:7}] run scoreboard players set #page_used rpg_ex_tmp 1
execute if score #page_used rpg_ex_tmp matches 1 unless entity @e[type=minecraft:item_display,tag=rpg.rite.prop.page,distance=..6] run function rpg:inquest/tool/place/page
execute if score @s rpg_dm_lord matches 1 if entity @a[tag=rpg.name.1,distance=..6,gamemode=!spectator] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 1 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:1}] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 2 if entity @a[tag=rpg.name.2,distance=..6,gamemode=!spectator] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 2 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:2}] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 3 if entity @a[tag=rpg.name.3,distance=..6,gamemode=!spectator] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 3 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:3}] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 4 if entity @a[tag=rpg.name.4,distance=..6,gamemode=!spectator] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 4 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:4}] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 5 if entity @a[tag=rpg.name.5,distance=..6,gamemode=!spectator] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 5 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:5}] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 6 if entity @a[tag=rpg.name.6,distance=..6,gamemode=!spectator] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 6 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:6}] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 7 if entity @a[tag=rpg.name.7,distance=..6,gamemode=!spectator] run scoreboard players set #channel rpg_ex_tmp 1
execute if score @s rpg_dm_lord matches 7 as @a[distance=..6,gamemode=!spectator] if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:7}] run scoreboard players set #channel rpg_ex_tmp 1
execute if score #channel rpg_ex_tmp matches 0 run scoreboard players set @s rpg_ex_time 100
execute if score #channel rpg_ex_tmp matches 1 run scoreboard players remove @s rpg_ex_time 1
execute if score #channel rpg_ex_tmp matches 1 if entity @s[tag=rpg.layout.haste] run scoreboard players remove @s rpg_ex_time 1
execute if score #channel rpg_ex_tmp matches 1 if entity @a[distance=..6,gamemode=!spectator,scores={rpg_ex_path=3,rpg_ex_lvl=4..}] run scoreboard players remove @s rpg_ex_time 1
execute if score @s rpg_ex_time matches 80 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 0.9
execute if score @s rpg_ex_time matches 60 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 1.05
execute if score @s rpg_ex_time matches 40 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 1.2
execute if score @s rpg_ex_time matches 20 run playsound minecraft:block.amethyst_block.chime player @a[distance=..14] ~ ~ ~ 0.8 1.4
execute if score #channel rpg_ex_tmp matches 1 run particle end_rod ~ ~0.8 ~ 0.45 0.35 0.45 0.025 3 normal
execute if score @s rpg_ex_time matches ..0 run return run function rpg:inquest/start_verdict
tag @s remove rpg.rite.anchor.active
