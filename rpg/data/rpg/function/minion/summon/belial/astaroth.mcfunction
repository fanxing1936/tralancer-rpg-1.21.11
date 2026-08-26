# 贝利尔麾下咒使：亚斯塔禄。可独立、永久存活。
summon minecraft:illusioner ~ ~ ~ {Tags:["rpg.demon.minion","rpg.demon.minion.new","rpg.demon.minion.lord6","rpg.demon.minion.role4"],CanJoinRaid:0b,PersistenceRequired:1b,CustomNameVisible:1b,NoAI:0b,CustomName:["",{"text":"[罪仆·咒使] ","color":"#57256B","bold":true,"italic":false},{"text":"亚斯塔禄","color":"#C28BE0","bold":false,"italic":false}],Health:70f,active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:70f},{id:"minecraft:attack_damage",base:6f},{id:"minecraft:armor",base:6f},{id:"minecraft:follow_range",base:36f},{id:"minecraft:movement_speed",base:0.29f},{id:"minecraft:knockback_resistance",base:0.35f}],equipment:{mainhand:{id:"minecraft:bow",count:1}},drop_chances:{mainhand:0f},DeathLootTable:"rpg:minion/belial/astaroth"}
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_lord 6
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_role 4
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_owner 0
execute if entity @s[type=minecraft:item_display,tag=rpg.rite.anchor] run scoreboard players operation @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_owner = @s rpg_rite_id
execute if entity @s[type=minecraft:item_display,tag=rpg.ch1.rite] run scoreboard players operation @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_ch1_id = @s rpg_ch1_id
execute if entity @s[type=minecraft:item_display,tag=rpg.ch1.rite] run tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] add rpg.ch1.minion
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cd 97
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cast 0
tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] remove rpg.demon.minion.new
particle witch ~ ~1 ~ 0.55 0.75 0.55 0.035 18
particle soul ~ ~1 ~ 0.35 0.65 0.35 0.025 10
playsound minecraft:entity.illusioner.prepare_blindness hostile @a[distance=..28] ~ ~ ~ 0.55 0.9
execute unless entity @s[tag=rpg.end.controller] run tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[罪群] ","color":"#57256B","bold":true,"italic":false},{"text":"贝利尔 · ","color":"#5B2C6F","bold":false,"italic":false},{"text":"咒使 ","color":"gray","bold":false,"italic":false},{"text":"亚斯塔禄","color":"#C28BE0","bold":false,"italic":false},{"text":"应召现身。","color":"dark_gray","bold":false,"italic":false}]
