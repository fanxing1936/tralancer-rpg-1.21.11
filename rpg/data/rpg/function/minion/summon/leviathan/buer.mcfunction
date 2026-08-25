# 利维坦麾下处刑者：布耶尔。可独立、永久存活。
summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.demon.minion","rpg.demon.minion.new","rpg.demon.minion.lord2","rpg.demon.minion.role5"],CanJoinRaid:0b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:["",{"text":"[罪仆·处刑者] ","color":"#1B4F72","bold":true,"italic":false},{"text":"布耶尔","color":"#62D9E8","bold":false,"italic":false}],Health:108f,active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:108f},{id:"minecraft:attack_damage",base:11f},{id:"minecraft:armor",base:8f},{id:"minecraft:follow_range",base:36f},{id:"minecraft:movement_speed",base:0.33f},{id:"minecraft:knockback_resistance",base:0.35f}],equipment:{mainhand:{id:"minecraft:iron_axe",count:1}},drop_chances:{mainhand:0f},DeathLootTable:"rpg:minion/leviathan/buer"}
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_lord 2
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_role 5
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cd 37
tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] remove rpg.demon.minion.new
particle nautilus ~ ~1 ~ 0.55 0.75 0.55 0.035 18
particle soul ~ ~1 ~ 0.35 0.65 0.35 0.025 10
playsound minecraft:entity.guardian.attack hostile @a[distance=..28] ~ ~ ~ 0.55 0.9
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[罪群] ","color":"#1B4F72","bold":true,"italic":false},{"text":"利维坦 · ","color":"#1B4F72","bold":false,"italic":false},{"text":"处刑者 ","color":"gray","bold":false,"italic":false},{"text":"布耶尔","color":"#62D9E8","bold":false,"italic":false},{"text":"应召现身。","color":"dark_gray","bold":false,"italic":false}]
