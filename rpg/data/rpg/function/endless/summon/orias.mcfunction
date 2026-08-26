# 第 59 柱 · 欧利亚斯；游离魔神，职责为咒使，亲和亚巴顿。
summon minecraft:illusioner ~ ~ ~ {Tags:["rpg.demon.minion","rpg.demon.minion.new","rpg.demon.minion.roaming","rpg.demon.minion.lord3","rpg.demon.minion.role4"],CanJoinRaid:0b,PersistenceRequired:1b,CustomNameVisible:1b,NoAI:0b,CustomName:["",{"text":"[游柱·咒使] ","color":"#5B5B62","bold":true,"italic":false},{"text":"欧利亚斯","color":"#C2C2CC","bold":false,"italic":false}],Health:70f,active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:70f},{id:"minecraft:attack_damage",base:6f},{id:"minecraft:armor",base:6f},{id:"minecraft:follow_range",base:36f},{id:"minecraft:movement_speed",base:0.29f},{id:"minecraft:knockback_resistance",base:0.35f}],equipment:{mainhand:{id:"minecraft:bow",count:1}},drop_chances:{mainhand:0f},DeathLootTable:"minecraft:empty"}
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_lord 3
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_role 4
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_owner 0
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cd 73
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cast 0
tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] remove rpg.demon.minion.new
particle sculk_soul ~ ~1 ~ 0.45 0.65 0.45 0.025 8
