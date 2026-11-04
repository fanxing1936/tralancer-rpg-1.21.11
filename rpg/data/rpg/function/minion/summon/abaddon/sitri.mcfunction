# 亚巴顿麾下猎手：西迪。可独立、永久存活。
summon minecraft:pillager ~ ~ ~ {Tags:["rpg.demon.minion","rpg.demon.minion.new","rpg.demon.minion.lord3","rpg.demon.minion.role2"],CanJoinRaid:0b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:["",{"text":"[罪仆·猎手] ","color":"#A7AFC9","bold":true,"italic":false},{"text":"西迪","color":"#FFFFFF","bold":false,"italic":false}],Health:66f,active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:66f},{id:"minecraft:attack_damage",base:6f},{id:"minecraft:armor",base:5f},{id:"minecraft:follow_range",base:36f},{id:"minecraft:movement_speed",base:0.31f},{id:"minecraft:knockback_resistance",base:0.35f}],equipment:{mainhand:{id:"minecraft:crossbow",count:1}},drop_chances:{mainhand:0f},DeathLootTable:"rpg:minion/abaddon/sitri"}
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_lord 3
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_role 2
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_owner 0
execute if entity @s[type=minecraft:item_display,tag=rpg.rite.anchor] run scoreboard players operation @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_owner = @s rpg_rite_id
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cd 62
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cast 0
tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] remove rpg.demon.minion.new
particle sculk_soul ~ ~1 ~ 0.55 0.75 0.55 0.035 18
particle soul ~ ~1 ~ 0.35 0.65 0.35 0.025 10
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..28] ~ ~ ~ 0.55 0.9
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"〖罪群〗","color":"#8C90A1","bold":true,"italic":false},{"text":" 𝔏𝔢𝔤𝔦𝔬𝔫","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"亚巴顿 · ","color":"#8C90A1","bold":false,"italic":false},{"text":"猎手 ","color":"#9C9A94","bold":false,"italic":false},{"text":"西迪","color":"#E6DFCF","bold":false,"italic":false},{"text":"应召现身。","color":"#9C9A94","bold":false,"italic":false}]
