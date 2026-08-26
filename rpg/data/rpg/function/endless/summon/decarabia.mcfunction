# 第 69 柱 · 单卡拉比；游离魔神，职责为猎手，亲和贝利尔。
summon minecraft:pillager ~ ~ ~ {Tags:["rpg.demon.minion","rpg.demon.minion.new","rpg.demon.minion.roaming","rpg.demon.minion.lord6","rpg.demon.minion.role2"],CanJoinRaid:0b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:["",{"text":"[游柱·猎手] ","color":"#57256B","bold":true,"italic":false},{"text":"单卡拉比","color":"#C28BE0","bold":false,"italic":false}],Health:66f,active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:66f},{id:"minecraft:attack_damage",base:6f},{id:"minecraft:armor",base:5f},{id:"minecraft:follow_range",base:36f},{id:"minecraft:movement_speed",base:0.31f},{id:"minecraft:knockback_resistance",base:0.35f}],equipment:{mainhand:{id:"minecraft:crossbow",count:1}},drop_chances:{mainhand:0f},DeathLootTable:"minecraft:empty"}
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_lord 6
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_role 2
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_owner 0
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cd 44
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cast 0
tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] remove rpg.demon.minion.new
particle witch ~ ~1 ~ 0.45 0.65 0.45 0.025 8
