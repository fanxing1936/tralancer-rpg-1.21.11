scoreboard players set @s rpg_ex_kind 1
scoreboard players set @s rpg_ex_ctime 140
summon minecraft:armor_stand ~2 ~ ~ {Tags:["rpg.counter.name","rpg.counter.false"],Invisible:1b,NoGravity:1b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:[{"text":"晨星之王","color":"#A8FFCB","bold":true,"italic":false}],Health:200f,attributes:[{id:"max_health",base:200f}]}
summon minecraft:armor_stand ~-2 ~ ~ {Tags:["rpg.counter.name","rpg.counter.true"],Invisible:1b,NoGravity:1b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:[{"text":"路西法","color":"#00491C","bold":true,"italic":false}],Health:200f,attributes:[{id:"max_health",base:200f}]}
summon minecraft:armor_stand ~ ~ ~2 {Tags:["rpg.counter.name","rpg.counter.false"],Invisible:1b,NoGravity:1b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:[{"text":"光耀者","color":"#A8FFCB","bold":true,"italic":false}],Health:200f,attributes:[{id:"max_health",base:200f}]}
scoreboard players operation @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..4] rpg_rite_id = @s rpg_rite_id
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[反仪式·傲慢] ","color":"#31D97C","bold":true,"italic":false},{"text":"王冠伪造了三个名号。攻击错误名字会撕裂法阵。","color":"gray","italic":false}]
playsound minecraft:entity.illusioner.prepare_mirror hostile @a[distance=..20] ~ ~ ~ 1 0.8
