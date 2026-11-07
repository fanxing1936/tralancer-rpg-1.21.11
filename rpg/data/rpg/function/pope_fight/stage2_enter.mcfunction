# 第二阶段：教皇亲临。
scoreboard players set #stage rpg_pf 2
scoreboard players set #t rpg_pf 0
function rpg:pope_fight/bgm/play_2
scoreboard players set #sk rpg_pf 7
scoreboard players set #st rpg_pf 0
scoreboard players set #h rpg_pf 0
scoreboard players set #wave rpg_pf 1
scoreboard players set #next rpg_pf 750
scoreboard players set #cd rpg_pf 0
scoreboard players set #tp rpg_pf 0
scoreboard players set #blood rpg_pf 200
scoreboard players set #reclaim rpg_pf 600
scoreboard players set #enhance rpg_pf 100
scoreboard players set #pb rpg_pf 0
scoreboard players set #ultq rpg_pf 0
scoreboard players set #ulti rpg_pf 0
scoreboard players set #ultcd rpg_pf 900
scoreboard players set #ultl rpg_pf 625
bossbar set minecraft:pope name {"text":"","font":"rpg:pope_fx"}
scoreboard players set #hudl rpg_pf 20
bossbar set minecraft:pope max 1000
bossbar set minecraft:pope value 1000
function rpg:pope_fight/fx/pillar
execute positioned ~ ~2.4 ~ run function rpg:pope_fight/fx/halo
particle dust{color:[1.000f,0.949f,0.659f],scale:1.6} ~ ~1 ~ 0.8 1.2 0.8 0.08 64 force
particle flash{color:16773800} ~ ~1 ~ 0 0 0 0 1 force
tellraw @a[distance=..48] ["",{"text":"〖教皇〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔓𝔬𝔭𝔢","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"跪下。这片大地上的权柄，只有一个来源。","color":"#9C9A94","bold":false,"italic":false}]
function rpg:pope/summon
tag @e[type=minecraft:vindicator,tag=rpg.pope,tag=!rpg.pf.boss,distance=..2] add rpg.pf.boss
execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1] run function rpg:pope_fight/boss/init
