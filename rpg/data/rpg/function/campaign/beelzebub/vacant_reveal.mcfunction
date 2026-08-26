tag @s remove rpg.vacant
tag @s add rpg.vac.torn
effect give @s minecraft:glowing 10 0 true
particle minecraft:sculk_soul ~ ~1.3 ~ 0.35 0.6 0.35 0.03 25 force
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"空缺者母亲：","color":"#706B5E","bold":true,"italic":false},{"text":"今天是祷告日。每个人都有一份。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"她知道自己是谁，却不知道‘自己’是什么意思。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"米拉：","color":"#FFF2A8","bold":true,"italic":false},{"text":"她昨天把整份口粮送进第七粮仓，却一口也没有吃。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[交叉验证] ","color":"#B8A98B","bold":true,"italic":false},{"text":"不是失忆，也不是普通复生：姓名仍在，人的主体已经空缺。","color":"gray","bold":false,"italic":false}]
scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_obj 1
