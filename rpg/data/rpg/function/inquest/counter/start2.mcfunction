scoreboard players set @s rpg_ex_kind 2
scoreboard players set @s rpg_ex_ctime 200
summon minecraft:husk ~2 ~ ~ {Tags:["rpg.counter.clone"],PersistenceRequired:1b,CanPickUpLoot:0b,CustomNameVisible:1b,CustomName:[{"text":"妒影","color":"#3DA9E8","bold":true,"italic":false}],Health:60f,attributes:[{id:"max_health",base:60f},{id:"attack_damage",base:9f},{id:"movement_speed",base:0.31f}],drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f,legs:0f,feet:0f}}
scoreboard players operation @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] rpg_rite_id = @s rpg_rite_id
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] weapon.mainhand from entity @p[distance=..14] weapon.mainhand
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] weapon.offhand from entity @p[distance=..14] weapon.offhand
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] armor.head from entity @p[distance=..14] armor.head
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] armor.chest from entity @p[distance=..14] armor.chest
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] armor.legs from entity @p[distance=..14] armor.legs
item replace entity @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..4,limit=1,sort=nearest] armor.feet from entity @p[distance=..14] armor.feet
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[反仪式·嫉妒] ","color":"#3DA9E8","bold":true,"italic":false},{"text":"利维坦复制了最近驱魔者的装备；十秒内击破妒影。","color":"gray","italic":false}]
playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..20] ~ ~ ~ 1 0.75
