bossbar set rpg:chapter1 value 20
bossbar set rpg:chapter1 name ["",{"text":"见证人封锁线｜听完简报后迎战","color":"#FFF2A8","bold":true,"italic":false}]
scoreboard players set @s rpg_ch1_obj 0
scoreboard players set @s rpg_ch1_sub 0
scoreboard players set @s rpg_ch1_guard 0
execute unless entity @e[type=minecraft:villager,tag=rpg.ch1.mira,distance=..40,limit=1] positioned ^ ^ ^17 run summon minecraft:villager ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.actor","rpg.ch1.mira","rpg.vac.seen","rpg.ch1.new"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:["",{"text":"米拉 · 见证人","color":"#FFF2A8","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:villager,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..40] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:villager,tag=rpg.ch1.new] remove rpg.ch1.new
execute positioned ^ ^ ^17 run tp @e[type=minecraft:villager,tag=rpg.ch1.mira,distance=..72,sort=nearest,limit=1] ~ ~ ~
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[安全对白] ","color":"#B8A98B","bold":true,"italic":false},{"text":"敌人尚未入场；阅读简报后会有明确的战斗提示。","color":"gray","bold":false,"italic":false}]
