# 第 61 柱 · 撒共；游离魔神，职责为司祭，亲和萨麦尔。
summon minecraft:evoker ~ ~ ~ {Tags:["rpg.demon.minion","rpg.demon.minion.new","rpg.demon.minion.roaming","rpg.demon.minion.lord5","rpg.demon.minion.role3"],CanJoinRaid:0b,PersistenceRequired:1b,CustomNameVisible:1b,NoAI:1b,CustomName:["",{"text":"[游柱·司祭] ","color":"#7B241C","bold":true,"italic":false},{"text":"撒共","color":"#FF665E","bold":false,"italic":false}],Health:76f,active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:76f},{id:"minecraft:attack_damage",base:4f},{id:"minecraft:armor",base:7f},{id:"minecraft:follow_range",base:36f},{id:"minecraft:movement_speed",base:0.0f},{id:"minecraft:knockback_resistance",base:0.35f}],equipment:{mainhand:{id:"minecraft:book",count:1}},drop_chances:{mainhand:0f},DeathLootTable:"minecraft:empty"}
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_lord 5
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_role 3
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_owner 0
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cd 87
scoreboard players set @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] rpg_mn_cast 0
tag @e[tag=rpg.demon.minion.new,distance=..3,limit=1,sort=nearest] remove rpg.demon.minion.new
particle soul_fire_flame ~ ~1 ~ 0.45 0.65 0.45 0.025 8
