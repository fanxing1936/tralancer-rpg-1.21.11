bossbar set rpg:chapter1 value 13
bossbar set rpg:chapter1 name ["",{"text":"会回家的死者｜以圣器照见空缺","color":"#B8A98B","bold":true,"italic":false}]
execute positioned ^ ^ ^19 run summon minecraft:villager ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.vacant","rpg.ch1.vacant.safe","rpg.vac.seen","rpg.vacant","rpg.ch1.new"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,CustomName:["",{"text":"回家的母亲","color":"gray","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:villager,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..40] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:villager,tag=rpg.ch1.new] remove rpg.ch1.new
scoreboard players set @e[type=minecraft:villager,tag=rpg.ch1.vacant,sort=nearest,limit=1,distance=..40] rpg_vac_x -100
tellraw @a[tag=rpg.ch1.current] ["",{"text":"目标更新　","color":"#B8A98B","bold":true,"italic":false},{"text":"手持驱魔图腾，靠近‘回家的母亲’。","color":"gray","bold":false,"italic":false}]
