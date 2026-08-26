bossbar set rpg:chapter1 value 20
bossbar set rpg:chapter1 name ["",{"text":"五席未满｜第1轮 · 封路与追猎","color":"#5A6B1E","bold":true,"italic":false}]
scoreboard players set @s rpg_ch1_obj 0
scoreboard players set @s rpg_ch1_sub 1
scoreboard players set @s rpg_ch1_guard 0
execute unless entity @e[type=minecraft:villager,tag=rpg.ch1.mira,distance=..40,limit=1] positioned ^ ^ ^17 run summon minecraft:villager ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.actor","rpg.ch1.mira","rpg.vac.seen","rpg.ch1.new"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:["",{"text":"米拉 · 见证人","color":"#FFF2A8","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:villager,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..40] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:villager,tag=rpg.ch1.new] remove rpg.ch1.new
execute positioned ^ ^ ^17 run tp @e[type=minecraft:villager,tag=rpg.ch1.mira,distance=..72,sort=nearest,limit=1] ~ ~ ~
tellraw @a[tag=rpg.ch1.current] ["",{"text":"米拉：","color":"#FFF2A8","bold":true,"italic":false},{"text":"我偷下三页名册。它们追的不是我，是还能把死者叫回名字的人。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"桀派：","color":"#5A6B1E","bold":true,"italic":false},{"text":"宴席不接待没有登记的客人。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"布提斯：","color":"#5A6B1E","bold":true,"italic":false},{"text":"名册在他们身上。先封街，再取回。","color":"gray","bold":false,"italic":false}]
execute positioned ^8 ^ ^18 run function rpg:campaign/beelzebub/spawn/minion/zepar
execute positioned ^-8 ^ ^18 run function rpg:campaign/beelzebub/spawn/minion/botis
