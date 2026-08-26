# 别西卜麾下处刑者：布松。可独立、永久存活。
summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.demon.minion","rpg.demon.minion.new","rpg.demon.minion.lord4","rpg.demon.minion.role5"],CanJoinRaid:0b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:["",{"text":"[罪仆·处刑者] ","color":"#596B18","bold":true,"italic":false},{"text":"布松","color":"#B5D957","bold":false,"italic":false}],Health:108f,active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:108f},{id:"minecraft:attack_damage",base:11f},{id:"minecraft:armor",base:8f},{id:"minecraft:follow_range",base:36f},{id:"minecraft:movement_speed",base:0.33f},{id:"minecraft:knockback_resistance",base:0.35f}],equipment:{mainhand:{id:"minecraft:iron_axe",count:1}},drop_chances:{mainhand:0f},DeathLootTable:"rpg:minion/beelzebub/purson"}
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_lord 4
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_role 5
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_owner 0
execute if entity @s[type=minecraft:item_display,tag=rpg.rite.anchor] run scoreboard players operation @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_owner = @s rpg_rite_id
execute if entity @s[type=minecraft:item_display,tag=rpg.ch1.rite] run scoreboard players operation @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_ch1_id = @s rpg_ch1_id
execute if entity @s[type=minecraft:item_display,tag=rpg.ch1.rite] run tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] add rpg.ch1.minion
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cd 73
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cast 0
tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] remove rpg.demon.minion.new
particle spore_blossom_air ~ ~1 ~ 0.55 0.75 0.55 0.035 18
particle soul ~ ~1 ~ 0.35 0.65 0.35 0.025 10
playsound minecraft:entity.spider.ambient hostile @a[distance=..28] ~ ~ ~ 0.55 0.9
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[罪群] ","color":"#596B18","bold":true,"italic":false},{"text":"别西卜 · ","color":"#5A6B1E","bold":false,"italic":false},{"text":"处刑者 ","color":"gray","bold":false,"italic":false},{"text":"布松","color":"#B5D957","bold":false,"italic":false},{"text":"应召现身。","color":"dark_gray","bold":false,"italic":false}]
