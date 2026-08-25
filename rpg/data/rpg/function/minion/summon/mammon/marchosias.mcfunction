# 玛门麾下处刑者：马可西亚斯。可独立、永久存活。
summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.demon.minion","rpg.demon.minion.new","rpg.demon.minion.lord7","rpg.demon.minion.role5"],CanJoinRaid:0b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:["",{"text":"[罪仆·处刑者] ","color":"#987B08","bold":true,"italic":false},{"text":"马可西亚斯","color":"#FFD85A","bold":false,"italic":false}],Health:108f,active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:108f},{id:"minecraft:attack_damage",base:11f},{id:"minecraft:armor",base:8f},{id:"minecraft:follow_range",base:36f},{id:"minecraft:movement_speed",base:0.33f},{id:"minecraft:knockback_resistance",base:0.35f}],equipment:{mainhand:{id:"minecraft:iron_axe",count:1}},drop_chances:{mainhand:0f},DeathLootTable:"rpg:minion/mammon/marchosias"}
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_lord 7
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_role 5
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cd 37
tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] remove rpg.demon.minion.new
particle wax_on ~ ~1 ~ 0.55 0.75 0.55 0.035 18
particle soul ~ ~1 ~ 0.35 0.65 0.35 0.025 10
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..28] ~ ~ ~ 0.55 0.9
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[罪群] ","color":"#987B08","bold":true,"italic":false},{"text":"玛门 · ","color":"#B7950B","bold":false,"italic":false},{"text":"处刑者 ","color":"gray","bold":false,"italic":false},{"text":"马可西亚斯","color":"#FFD85A","bold":false,"italic":false},{"text":"应召现身。","color":"dark_gray","bold":false,"italic":false}]
