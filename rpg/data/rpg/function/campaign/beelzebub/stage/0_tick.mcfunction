execute if score @s rpg_ch1_time matches 45 run playsound minecraft:block.bell.resonate master @a[tag=rpg.ch1.current] ~ ~ ~ 0.8 0.62
execute if score @s rpg_ch1_time matches 45 run tellraw @a[tag=rpg.ch1.current] ["",{"text":"旁白：","color":"#706B5E","bold":true,"italic":false},{"text":"粮册写着满仓，街边却摆着无人领取的空碗。","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_ch1_time matches 105 run tellraw @a[tag=rpg.ch1.current] ["",{"text":"旁白：","color":"#706B5E","bold":true,"italic":false},{"text":"墓地每天添新土；入夜后，死者仍会回家。","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_ch1_time matches 165 run playsound minecraft:entity.bee.loop_aggressive master @a[tag=rpg.ch1.current] ~ ~ ~ 0.18 0.45
execute if score @s rpg_ch1_time matches 165 run tellraw @a[tag=rpg.ch1.current] ["",{"text":"书记员 伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"你听见十三下了吗？司钟人三天前就死了。","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_ch1_time matches 225 run tellraw @a[tag=rpg.ch1.current] ["",{"text":"伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"教廷说绳索自己落下，也说你没有听见。","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_ch1_time matches 285 run tellraw @a[tag=rpg.ch1.current] ["",{"text":"伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"驱魔官处理得太快、太干净。我需要一个还相信自己眼睛的人。","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_ch1_time matches 345 run tellraw @a[tag=rpg.ch1.current] ["",{"text":"[调查原则] ","color":"#B8A98B","bold":true,"italic":false},{"text":"先记录事实，再比较解释。一个异常不能证明恶魔。","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_ch1_time matches 400.. run function rpg:campaign/beelzebub/advance
